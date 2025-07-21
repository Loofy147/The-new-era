import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from ..vector_search.vector_engine import VectorSearchEngine, SearchResult, PromptEntry

@dataclass
class ConversationContext:
    """Enhanced conversation context with vector search"""
    session_id: str
    agent_name: str
    conversation_history: List[Dict[str, Any]]
    related_prompts: List[str]  # IDs of related prompts
    semantic_context: Dict[str, Any]
    created_at: datetime
    last_updated: datetime

@dataclass
class PromptTemplate:
    """Prompt template with variables"""
    id: str
    name: str
    template: str
    variables: List[str]
    category: str
    description: str
    usage_examples: List[Dict[str, Any]]

class EnhancedPromptMemoryService:
    """Enhanced prompt memory service with vector search capabilities"""
    
    def __init__(self, data_dir: str = "data/prompt_memory"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.vector_engine = VectorSearchEngine(str(self.data_dir / "vector"))
        self.conversations: Dict[str, ConversationContext] = {}
        self.templates: Dict[str, PromptTemplate] = {}
        
        self.logger = logging.getLogger(__name__)
        
        # Load existing data
        self._load_conversations()
        self._load_templates()
    
    def _load_conversations(self):
        """Load existing conversations"""
        conversations_file = self.data_dir / "conversations.json"
        if conversations_file.exists():
            try:
                with open(conversations_file, 'r') as f:
                    data = json.load(f)
                
                for conv_data in data.get('conversations', []):
                    context = ConversationContext(
                        session_id=conv_data['session_id'],
                        agent_name=conv_data['agent_name'],
                        conversation_history=conv_data['conversation_history'],
                        related_prompts=conv_data.get('related_prompts', []),
                        semantic_context=conv_data.get('semantic_context', {}),
                        created_at=datetime.fromisoformat(conv_data['created_at']),
                        last_updated=datetime.fromisoformat(conv_data['last_updated'])
                    )
                    self.conversations[context.session_id] = context
                
                self.logger.info(f"Loaded {len(self.conversations)} conversations")
                
            except Exception as e:
                self.logger.error(f"Failed to load conversations: {e}")
    
    def _load_templates(self):
        """Load prompt templates"""
        templates_file = self.data_dir / "templates.json"
        if templates_file.exists():
            try:
                with open(templates_file, 'r') as f:
                    data = json.load(f)
                
                for template_data in data.get('templates', []):
                    template = PromptTemplate(**template_data)
                    self.templates[template.id] = template
                
                self.logger.info(f"Loaded {len(self.templates)} templates")
                
            except Exception as e:
                self.logger.error(f"Failed to load templates: {e}")
    
    async def store_prompt(self, prompt: str, response: str, agent_name: str, 
                          category: str = "", tags: List[str] = None, 
                          context: Dict[str, Any] = None, success: bool = True) -> str:
        """Store a prompt-response pair with metadata"""
        if tags is None:
            tags = []
        
        # Enhance context with response information
        enhanced_context = context or {}
        enhanced_context.update({
            'response': response,
            'response_length': len(response),
            'timestamp': datetime.now().isoformat(),
            'success': success
        })
        
        # Store in vector search engine
        prompt_id = await self.vector_engine.add_prompt(
            content=prompt,
            category=category,
            tags=tags + ['prompt'],
            agent_name=agent_name,
            context=enhanced_context
        )
        
        # Also store the response as a separate entry
        response_id = await self.vector_engine.add_prompt(
            content=response,
            category=category,
            tags=tags + ['response'],
            agent_name=agent_name,
            context={
                'prompt_id': prompt_id,
                'is_response': True,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Update success rate if needed
        if not success:
            await self.vector_engine.update_success_rate(prompt_id, False)
        
        return prompt_id
    
    async def find_similar_prompts(self, query: str, agent_name: str = None, 
                                 category: str = None, k: int = 5, 
                                 min_similarity: float = 0.3) -> List[SearchResult]:
        """Find similar prompts using vector search"""
        return await self.vector_engine.search_similar(
            query=query,
            k=k,
            category=category,
            agent_name=agent_name,
            min_similarity=min_similarity
        )
    
    async def get_contextual_prompts(self, session_id: str, current_prompt: str, 
                                   k: int = 3) -> List[SearchResult]:
        """Get contextually relevant prompts for a conversation"""
        if session_id not in self.conversations:
            # No conversation context, just do similarity search
            return await self.find_similar_prompts(current_prompt, k=k)
        
        context = self.conversations[session_id]
        
        # Combine current prompt with conversation history for better context
        conversation_text = " ".join([
            msg.get('content', '') for msg in context.conversation_history[-3:]
        ])
        
        combined_query = f"{conversation_text} {current_prompt}"
        
        # Search for similar prompts
        similar_prompts = await self.vector_engine.search_similar(
            query=combined_query,
            agent_name=context.agent_name,
            k=k * 2
        )
        
        # Filter out prompts that were already used in this conversation
        used_prompts = set(context.related_prompts)
        filtered_prompts = [
            result for result in similar_prompts 
            if result.entry.id not in used_prompts
        ]
        
        return filtered_prompts[:k]
    
    async def start_conversation(self, session_id: str, agent_name: str) -> ConversationContext:
        """Start a new conversation context"""
        context = ConversationContext(
            session_id=session_id,
            agent_name=agent_name,
            conversation_history=[],
            related_prompts=[],
            semantic_context={},
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        self.conversations[session_id] = context
        await self._save_conversations()
        
        return context
    
    async def add_to_conversation(self, session_id: str, message: Dict[str, Any], 
                                related_prompt_ids: List[str] = None):
        """Add a message to conversation context"""
        if session_id not in self.conversations:
            # Auto-create conversation context
            agent_name = message.get('agent', 'unknown')
            await self.start_conversation(session_id, agent_name)
        
        context = self.conversations[session_id]
        context.conversation_history.append(message)
        context.last_updated = datetime.now()
        
        if related_prompt_ids:
            context.related_prompts.extend(related_prompt_ids)
        
        # Keep conversation history manageable
        if len(context.conversation_history) > 100:
            context.conversation_history = context.conversation_history[-50:]
        
        await self._save_conversations()
    
    async def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get conversation summary with semantic insights"""
        if session_id not in self.conversations:
            return {}
        
        context = self.conversations[session_id]
        
        # Extract key information
        total_messages = len(context.conversation_history)
        unique_prompts = len(set(context.related_prompts))
        
        # Get recent topics (simplified)
        recent_messages = context.conversation_history[-10:]
        topics = set()
        for msg in recent_messages:
            content = msg.get('content', '')
            # Simple topic extraction (could be enhanced with NLP)
            words = content.split()
            topics.update([word.lower() for word in words if len(word) > 5])
        
        return {
            'session_id': session_id,
            'agent_name': context.agent_name,
            'total_messages': total_messages,
            'unique_prompts_used': unique_prompts,
            'duration_minutes': (context.last_updated - context.created_at).total_seconds() / 60,
            'recent_topics': list(topics)[:10],
            'last_updated': context.last_updated.isoformat()
        }
    
    async def create_template(self, name: str, template: str, variables: List[str], 
                            category: str, description: str, 
                            usage_examples: List[Dict[str, Any]] = None) -> str:
        """Create a new prompt template"""
        template_id = f"template_{len(self.templates)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if usage_examples is None:
            usage_examples = []
        
        prompt_template = PromptTemplate(
            id=template_id,
            name=name,
            template=template,
            variables=variables,
            category=category,
            description=description,
            usage_examples=usage_examples
        )
        
        self.templates[template_id] = prompt_template
        await self._save_templates()
        
        return template_id
    
    async def render_template(self, template_id: str, variables: Dict[str, Any]) -> str:
        """Render a template with provided variables"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        
        # Simple template rendering (could be enhanced with Jinja2)
        rendered = template.template
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            rendered = rendered.replace(placeholder, str(var_value))
        
        return rendered
    
    async def suggest_templates(self, query: str, k: int = 5) -> List[Tuple[PromptTemplate, float]]:
        """Suggest relevant templates based on query"""
        suggestions = []
        
        for template in self.templates.values():
            # Simple scoring based on keyword matching
            query_words = set(query.lower().split())
            template_words = set((template.name + " " + template.description).lower().split())
            
            overlap = len(query_words & template_words)
            if overlap > 0:
                score = overlap / len(query_words | template_words)
                suggestions.append((template, score))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:k]
    
    async def get_trending_prompts(self, agent_name: str = None, days: int = 7, 
                                 k: int = 10) -> List[SearchResult]:
        """Get trending prompts for an agent or globally"""
        return await self.vector_engine.get_trending_prompts(days=days, k=k)
    
    async def cluster_agent_prompts(self, agent_name: str) -> List[Dict[str, Any]]:
        """Cluster prompts for a specific agent to find patterns"""
        clusters = await self.vector_engine.cluster_prompts()
        
        # Filter clusters for specific agent
        agent_clusters = []
        for cluster in clusters:
            agent_prompts = []
            for prompt_id in cluster.prompts:
                if prompt_id in self.vector_engine.prompt_store:
                    prompt = self.vector_engine.prompt_store[prompt_id]
                    if prompt.agent_name == agent_name:
                        agent_prompts.append({
                            'id': prompt.id,
                            'content': prompt.content[:100] + "...",
                            'usage_count': prompt.usage_count,
                            'success_rate': prompt.success_rate
                        })
            
            if agent_prompts:
                agent_clusters.append({
                    'cluster_id': cluster.id,
                    'description': cluster.description,
                    'prompts': agent_prompts,
                    'size': len(agent_prompts)
                })
        
        return agent_clusters
    
    async def optimize_prompts(self, agent_name: str) -> Dict[str, Any]:
        """Analyze and suggest prompt optimizations for an agent"""
        # Get all prompts for the agent
        agent_prompts = [
            prompt for prompt in self.vector_engine.prompt_store.values()
            if prompt.agent_name == agent_name
        ]
        
        if not agent_prompts:
            return {'message': 'No prompts found for agent'}
        
        # Analyze performance
        total_prompts = len(agent_prompts)
        high_performers = [p for p in agent_prompts if p.success_rate > 0.8]
        low_performers = [p for p in agent_prompts if p.success_rate < 0.5]
        
        # Find patterns in high-performing prompts
        high_performer_patterns = {}
        for prompt in high_performers:
            words = prompt.content.split()
            for word in words:
                if len(word) > 3:
                    high_performer_patterns[word] = high_performer_patterns.get(word, 0) + 1
        
        # Sort patterns by frequency
        top_patterns = sorted(high_performer_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
        
        recommendations = []
        
        # Recommend replacing low-performing prompts
        for low_prompt in low_performers[:5]:
            similar_high = await self.find_similar_prompts(
                low_prompt.content, agent_name=agent_name, min_similarity=0.5
            )
            
            high_alternatives = [
                result for result in similar_high 
                if result.entry.success_rate > low_prompt.success_rate
            ]
            
            if high_alternatives:
                recommendations.append({
                    'type': 'replace',
                    'low_performing_prompt': low_prompt.content[:100] + "...",
                    'low_performance_rate': low_prompt.success_rate,
                    'suggested_alternative': high_alternatives[0].entry.content[:100] + "...",
                    'alternative_performance_rate': high_alternatives[0].entry.success_rate
                })
        
        return {
            'agent_name': agent_name,
            'total_prompts': total_prompts,
            'high_performers': len(high_performers),
            'low_performers': len(low_performers),
            'average_success_rate': sum(p.success_rate for p in agent_prompts) / total_prompts,
            'top_performing_patterns': top_patterns,
            'recommendations': recommendations
        }
    
    async def _save_conversations(self):
        """Save conversations to file"""
        conversations_data = {
            'conversations': [
                {
                    'session_id': context.session_id,
                    'agent_name': context.agent_name,
                    'conversation_history': context.conversation_history,
                    'related_prompts': context.related_prompts,
                    'semantic_context': context.semantic_context,
                    'created_at': context.created_at.isoformat(),
                    'last_updated': context.last_updated.isoformat()
                }
                for context in self.conversations.values()
            ]
        }
        
        conversations_file = self.data_dir / "conversations.json"
        with open(conversations_file, 'w') as f:
            json.dump(conversations_data, f, indent=2)
    
    async def _save_templates(self):
        """Save templates to file"""
        templates_data = {
            'templates': [asdict(template) for template in self.templates.values()]
        }
        
        templates_file = self.data_dir / "templates.json"
        with open(templates_file, 'w') as f:
            json.dump(templates_data, f, indent=2)
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive service statistics"""
        vector_stats = await self.vector_engine.get_statistics()
        
        return {
            'vector_search': vector_stats,
            'conversations': {
                'total_conversations': len(self.conversations),
                'active_conversations': len([
                    c for c in self.conversations.values()
                    if (datetime.now() - c.last_updated).days < 1
                ])
            },
            'templates': {
                'total_templates': len(self.templates),
                'categories': list(set(t.category for t in self.templates.values()))
            }
        }
    
    def create_flask_app(self) -> Flask:
        """Create Flask app for HTTP API"""
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
        
        @app.route('/api/prompts/store', methods=['POST'])
        def store_prompt_endpoint():
            data = request.json
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            prompt_id = loop.run_until_complete(
                self.store_prompt(
                    prompt=data['prompt'],
                    response=data['response'],
                    agent_name=data['agent_name'],
                    category=data.get('category', ''),
                    tags=data.get('tags', []),
                    context=data.get('context'),
                    success=data.get('success', True)
                )
            )
            
            return jsonify({'prompt_id': prompt_id})
        
        @app.route('/api/prompts/search', methods=['POST'])
        def search_prompts_endpoint():
            data = request.json
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(
                self.find_similar_prompts(
                    query=data['query'],
                    agent_name=data.get('agent_name'),
                    category=data.get('category'),
                    k=data.get('k', 5),
                    min_similarity=data.get('min_similarity', 0.3)
                )
            )
            
            return jsonify({
                'results': [{
                    'prompt_id': result.entry.id,
                    'content': result.entry.content,
                    'similarity_score': result.similarity_score,
                    'rank': result.rank,
                    'usage_count': result.entry.usage_count,
                    'success_rate': result.entry.success_rate
                } for result in results]
            })
        
        @app.route('/api/statistics', methods=['GET'])
        def get_statistics_endpoint():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            stats = loop.run_until_complete(self.get_statistics())
            return jsonify(stats)
        
        return app

# Global service instance
enhanced_prompt_memory = EnhancedPromptMemoryService()
