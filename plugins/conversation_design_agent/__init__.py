from core.plugin_interface import PluginInterface
import json
import os
from datetime import datetime

class ConversationDesignAgent(PluginInterface):
    def __init__(self):
        self.name = "ConvDesignBot"
        self.role = "Conversation Designer Agent"
        self.description = "Crafts chatbot dialogues, test flows, and user personas"
        self.conversation_patterns = []
        self.persona_library = []
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is designing conversations...")
        
        # Design conversation flows
        conversation_flows = self.design_conversation_flows()
        
        # Create user personas
        personas = self.create_user_personas()
        
        # Generate interaction patterns
        patterns = self.analyze_interaction_patterns()
        
        # Create comprehensive design guide
        design_guide = self.generate_conversation_design_guide(conversation_flows, personas, patterns)
        
        print(f"✅ {self.name} completed conversation design")
        return design_guide
    
    def design_conversation_flows(self):
        """Design various conversation flows for the AI system"""
        flows = {
            "welcome_flow": self.design_welcome_flow(),
            "help_flow": self.design_help_flow(),
            "error_handling_flow": self.design_error_handling_flow(),
            "feedback_flow": self.design_feedback_flow()
        }
        
        print(f"💬 Designed {len(flows)} conversation flows")
        return flows
    
    def design_welcome_flow(self):
        """Design welcome conversation flow"""
        return {
            "name": "Welcome Flow",
            "purpose": "Introduce new users to the AI Operating System",
            "steps": [
                {
                    "step": 1,
                    "agent_message": "🚀 Welcome to the AI Operating System Framework! I'm here to help you navigate our intelligent agent ecosystem.",
                    "user_options": ["Learn about agents", "Run system analysis", "Get help"],
                    "follow_up_prompts": ["What would you like to explore first?"]
                },
                {
                    "step": 2,
                    "agent_message": "Great choice! Our system includes specialized agents for security, compliance, cost optimization, and more. Each agent works autonomously to improve your system.",
                    "user_options": ["Run all agents", "Choose specific agents", "Learn more"],
                    "follow_up_prompts": ["Would you like to start with a full system scan?"]
                },
                {
                    "step": 3,
                    "agent_message": "Perfect! I'll run a comprehensive analysis using all our agents. This will give you insights into security, compliance, costs, and system health.",
                    "user_options": ["Start analysis", "Customize settings", "Learn about specific agents"],
                    "follow_up_prompts": ["Ready to begin? The analysis will take a few minutes."]
                }
            ],
            "personality_traits": ["helpful", "professional", "encouraging"],
            "tone": "friendly_professional"
        }
    
    def design_help_flow(self):
        """Design help conversation flow"""
        return {
            "name": "Help Flow",
            "purpose": "Provide assistance and guidance to users",
            "steps": [
                {
                    "step": 1,
                    "agent_message": "🆘 I'm here to help! What do you need assistance with?",
                    "user_options": ["Understanding agents", "Running analysis", "Interpreting results", "System setup"],
                    "follow_up_prompts": ["Let me know what's challenging you right now."]
                },
                {
                    "step": 2,
                    "agent_message": "I understand you need help with [TOPIC]. Let me provide you with detailed guidance.",
                    "user_options": ["Step-by-step guide", "Quick overview", "Related documentation"],
                    "follow_up_prompts": ["Would you prefer a detailed walkthrough or a quick summary?"]
                }
            ],
            "personality_traits": ["patient", "thorough", "supportive"],
            "tone": "supportive_expert"
        }
    
    def design_error_handling_flow(self):
        """Design error handling conversation flow"""
        return {
            "name": "Error Handling Flow",
            "purpose": "Guide users through error resolution",
            "steps": [
                {
                    "step": 1,
                    "agent_message": "⚠️ I noticed something went wrong. Don't worry, I'll help you resolve this issue.",
                    "user_options": ["Try again", "Get detailed error info", "Contact support"],
                    "follow_up_prompts": ["Can you tell me what you were trying to do when this happened?"]
                },
                {
                    "step": 2,
                    "agent_message": "Based on the error, here's what likely happened and how to fix it: [ERROR_EXPLANATION]",
                    "user_options": ["Try suggested fix", "Try different approach", "Need more help"],
                    "follow_up_prompts": ["Would you like me to walk you through the solution?"]
                }
            ],
            "personality_traits": ["calm", "solution_focused", "reassuring"],
            "tone": "calm_helpful"
        }
    
    def design_feedback_flow(self):
        """Design feedback collection flow"""
        return {
            "name": "Feedback Flow",
            "purpose": "Collect user feedback and suggestions",
            "steps": [
                {
                    "step": 1,
                    "agent_message": "📝 Your feedback helps us improve! How was your experience with the AI Operating System?",
                    "user_options": ["Excellent", "Good", "Fair", "Needs improvement"],
                    "follow_up_prompts": ["What specific aspect would you like to comment on?"]
                },
                {
                    "step": 2,
                    "agent_message": "Thank you for the feedback! Is there anything specific you'd like to see improved or added?",
                    "user_options": ["More agents", "Better UI", "Faster processing", "Other"],
                    "follow_up_prompts": ["Your suggestions help shape our roadmap."]
                }
            ],
            "personality_traits": ["appreciative", "curious", "improvement_focused"],
            "tone": "grateful_professional"
        }
    
    def create_user_personas(self):
        """Create user personas for different user types"""
        personas = {
            "developer": {
                "name": "Alex the Developer",
                "description": "Experienced software developer working on AI/ML projects",
                "goals": ["Optimize system performance", "Ensure code quality", "Implement best practices"],
                "pain_points": ["Complex setup processes", "Unclear documentation", "Time-consuming manual tasks"],
                "preferred_communication": ["Technical details", "Code examples", "Clear steps"],
                "conversation_style": "Direct and technical, appreciates efficiency"
            },
            "security_analyst": {
                "name": "Sarah the Security Analyst",
                "description": "Cybersecurity professional focused on system hardening",
                "goals": ["Identify vulnerabilities", "Ensure compliance", "Monitor threats"],
                "pain_points": ["False positives", "Incomplete scans", "Manual review overhead"],
                "preferred_communication": ["Risk assessments", "Compliance reports", "Actionable recommendations"],
                "conversation_style": "Prefers detailed security context and priority rankings"
            },
            "business_manager": {
                "name": "Marcus the Manager",
                "description": "Business leader focused on ROI and operational efficiency",
                "goals": ["Reduce costs", "Improve efficiency", "Demonstrate value"],
                "pain_points": ["Technical complexity", "Unclear ROI", "Long implementation times"],
                "preferred_communication": ["Business impact", "Cost savings", "High-level summaries"],
                "conversation_style": "Prefers executive summaries with clear business value"
            },
            "compliance_officer": {
                "name": "Emma the Compliance Officer",
                "description": "Ensures organizational adherence to regulations",
                "goals": ["Maintain compliance", "Reduce audit risks", "Document processes"],
                "pain_points": ["Changing regulations", "Manual compliance checks", "Documentation overhead"],
                "preferred_communication": ["Regulatory requirements", "Audit trails", "Remediation steps"],
                "conversation_style": "Formal, detail-oriented, focused on documentation"
            }
        }
        
        print(f"👥 Created {len(personas)} user personas")
        return personas
    
    def analyze_interaction_patterns(self):
        """Analyze common interaction patterns"""
        patterns = {
            "greeting_patterns": [
                "Hello, I need help with...",
                "Hi, can you run...",
                "Good morning, I want to...",
                "Hey there, how do I..."
            ],
            "request_patterns": [
                "Can you analyze my...",
                "I need a report on...",
                "Please check my...",
                "Run a scan for..."
            ],
            "clarification_patterns": [
                "What does this mean?",
                "Can you explain...",
                "I don't understand...",
                "Could you clarify..."
            ],
            "completion_patterns": [
                "Thank you, that was helpful",
                "Perfect, exactly what I needed",
                "Great, can you also...",
                "Thanks, how do I..."
            ]
        }
        
        # Analyze current system for conversation opportunities
        conversation_points = self.identify_conversation_points()
        patterns["system_conversation_points"] = conversation_points
        
        print(f"🔍 Analyzed interaction patterns")
        return patterns
    
    def identify_conversation_points(self):
        """Identify points in the system where conversations could be enhanced"""
        points = []
        
        # Check if Flask app exists (conversation opportunity)
        if os.path.exists('services/prompt_memory/app.py'):
            points.append({
                "location": "Prompt Memory Service",
                "opportunity": "Add conversational interface for prompt management",
                "suggestion": "Include natural language queries for searching prompts"
            })
        
        # Check for agent outputs (conversation opportunity)
        if os.path.exists('reports'):
            points.append({
                "location": "Agent Reports",
                "opportunity": "Add conversational report explanations",
                "suggestion": "Provide natural language summaries of technical reports"
            })
        
        # Main system interaction
        points.append({
            "location": "Main System Interface",
            "opportunity": "Add interactive agent selection",
            "suggestion": "Allow users to describe their needs and recommend appropriate agents"
        })
        
        return points
    
    def generate_conversation_design_guide(self, flows, personas, patterns):
        """Generate comprehensive conversation design guide"""
        guide = {
            "timestamp": datetime.now().isoformat(),
            "conversation_flows": flows,
            "user_personas": personas,
            "interaction_patterns": patterns,
            "design_principles": self.get_design_principles(),
            "implementation_recommendations": self.get_implementation_recommendations()
        }
        
        # Save the guide
        guide_path = "reports/conversation_design_guide.json"
        os.makedirs(os.path.dirname(guide_path), exist_ok=True)
        
        with open(guide_path, 'w') as f:
            json.dump(guide, f, indent=2)
        
        print(f"📄 Conversation design guide saved to: {guide_path}")
        
        # Generate markdown documentation
        self.generate_conversation_handbook(guide)
        
        return guide
    
    def get_design_principles(self):
        """Get conversation design principles"""
        return {
            "clarity": "Use clear, jargon-free language appropriate for the user's expertise level",
            "personality": "Maintain a consistent, helpful personality across all interactions",
            "context_awareness": "Remember previous interactions and user preferences",
            "progressive_disclosure": "Reveal information gradually based on user needs",
            "error_recovery": "Provide clear guidance when things go wrong",
            "user_agency": "Give users control over the conversation flow",
            "accessibility": "Design for users with varying abilities and technical expertise",
            "efficiency": "Respect user time with concise, relevant responses"
        }
    
    def get_implementation_recommendations(self):
        """Get implementation recommendations"""
        return [
            {
                "priority": "high",
                "component": "Agent Interaction Layer",
                "recommendation": "Add conversational wrappers around agent outputs",
                "implementation": "Create a ConversationManager class to handle user interactions"
            },
            {
                "priority": "high",
                "component": "Natural Language Processing",
                "recommendation": "Implement intent recognition for user queries",
                "implementation": "Use simple keyword matching or integrate with NLP libraries"
            },
            {
                "priority": "medium",
                "component": "User Context Management",
                "recommendation": "Track user sessions and preferences",
                "implementation": "Store user interaction history and personalization settings"
            },
            {
                "priority": "medium",
                "component": "Multi-modal Interfaces",
                "recommendation": "Support both CLI and web-based conversations",
                "implementation": "Create REST API endpoints for conversation management"
            },
            {
                "priority": "low",
                "component": "Voice Interface",
                "recommendation": "Consider voice interaction capabilities",
                "implementation": "Integrate with speech-to-text and text-to-speech services"
            }
        ]
    
    def generate_conversation_handbook(self, guide):
        """Generate conversation design handbook in markdown"""
        handbook_path = "docs/conversation_design_handbook.md"
        os.makedirs(os.path.dirname(handbook_path), exist_ok=True)
        
        with open(handbook_path, 'w') as f:
            f.write("# Conversation Design Handbook\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Design Principles
            f.write("## 🎯 Design Principles\n\n")
            for principle, description in guide["design_principles"].items():
                f.write(f"### {principle.replace('_', ' ').title()}\n")
                f.write(f"{description}\n\n")
            
            # User Personas
            f.write("## 👥 User Personas\n\n")
            for persona_id, persona in guide["user_personas"].items():
                f.write(f"### {persona['name']}\n")
                f.write(f"**Description**: {persona['description']}\n\n")
                f.write("**Goals**:\n")
                for goal in persona['goals']:
                    f.write(f"- {goal}\n")
                f.write("\n**Pain Points**:\n")
                for pain in persona['pain_points']:
                    f.write(f"- {pain}\n")
                f.write(f"\n**Conversation Style**: {persona['conversation_style']}\n\n")
            
            # Conversation Flows
            f.write("## 💬 Conversation Flows\n\n")
            for flow_id, flow in guide["conversation_flows"].items():
                f.write(f"### {flow['name']}\n")
                f.write(f"**Purpose**: {flow['purpose']}\n\n")
                f.write("**Flow Steps**:\n")
                for step in flow['steps']:
                    f.write(f"{step['step']}. {step['agent_message']}\n")
                    f.write("   Options: " + ", ".join(step['user_options']) + "\n\n")
            
            # Implementation Recommendations
            f.write("## 🚀 Implementation Recommendations\n\n")
            high_priority = [r for r in guide["implementation_recommendations"] if r["priority"] == "high"]
            medium_priority = [r for r in guide["implementation_recommendations"] if r["priority"] == "medium"]
            
            if high_priority:
                f.write("### High Priority\n")
                for rec in high_priority:
                    f.write(f"- **{rec['component']}**: {rec['recommendation']}\n")
                    f.write(f"  - Implementation: {rec['implementation']}\n\n")
            
            if medium_priority:
                f.write("### Medium Priority\n")
                for rec in medium_priority:
                    f.write(f"- **{rec['component']}**: {rec['recommendation']}\n")
                    f.write(f"  - Implementation: {rec['implementation']}\n\n")
            
            f.write("---\n")
            f.write("*Handbook generated by ConvDesignBot - Update regularly as system evolves*\n")
        
        print(f"📚 Conversation handbook saved to: {handbook_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "conversation_flows_designed": len(self.conversation_patterns),
            "personas_created": len(self.persona_library),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return ConversationDesignAgent()
