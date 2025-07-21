import asyncio
import json
import numpy as np
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from abc import ABC, abstractmethod
import sqlite3
import pickle

# Lightweight embedding implementation without heavy ML dependencies
from sentence_transformers import SentenceTransformer
import faiss

@dataclass
class PromptEntry:
    """Prompt entry with metadata"""
    id: str
    content: str
    embedding: Optional[np.ndarray]
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0
    success_rate: float = 1.0
    agent_name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

@dataclass
class SearchResult:
    """Search result with similarity score"""
    entry: PromptEntry
    similarity_score: float
    rank: int

@dataclass
class SemanticCluster:
    """Semantic cluster of similar prompts"""
    id: str
    centroid: np.ndarray
    prompts: List[str]
    category: str
    description: str
    created_at: datetime

class EmbeddingModel(ABC):
    """Abstract embedding model interface"""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        pass

class SentenceTransformerModel(EmbeddingModel):
    """Sentence transformer embedding model"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            logging.error(f"Failed to load SentenceTransformer: {e}")
            # Fallback to simple embedding
            self.model = None
            self.dimension = 384
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        if self.model:
            return self.model.encode(texts)
        else:
            # Simple fallback embedding using text hashing
            return self._simple_embedding(texts)
    
    def get_dimension(self) -> int:
        return self.dimension
    
    def _simple_embedding(self, texts: List[str]) -> np.ndarray:
        """Simple fallback embedding using hash-based features"""
        embeddings = []
        for text in texts:
            # Create feature vector from text characteristics
            features = np.zeros(self.dimension)
            
            # Text length features
            features[0] = min(len(text) / 1000, 1.0)
            features[1] = len(text.split()) / 100
            
            # Character frequency features
            for i, char in enumerate(text.lower()[:50]):
                if char.isalnum():
                    features[i + 2] = ord(char) / 127
            
            # Hash-based features for remaining dimensions
            for i in range(52, self.dimension):
                hash_input = f"{text}_{i}".encode()
                hash_value = hashlib.md5(hash_input).hexdigest()
                features[i] = int(hash_value[:8], 16) / (16**8)
            
            embeddings.append(features)
        
        return np.array(embeddings)

class VectorIndex:
    """FAISS-based vector index for similarity search"""
    
    def __init__(self, dimension: int, index_type: str = "IVF"):
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.id_map: Dict[int, str] = {}
        self.reverse_id_map: Dict[str, int] = {}
        self._next_id = 0
        
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        try:
            if self.index_type == "IVF":
                # IVF (Inverted File) index for large datasets
                quantizer = faiss.IndexFlatL2(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, min(100, max(1, self._next_id // 10)))
            else:
                # Flat L2 index for exact search
                self.index = faiss.IndexFlatL2(self.dimension)
        except Exception as e:
            logging.error(f"Failed to initialize FAISS index: {e}")
            # Fallback to simple implementation
            self.index = None
            self._vectors: Dict[int, np.ndarray] = {}
    
    def add_vectors(self, embeddings: np.ndarray, ids: List[str]):
        """Add vectors to index"""
        if len(embeddings) != len(ids):
            raise ValueError("Number of embeddings must match number of IDs")
        
        # Map string IDs to integer IDs
        int_ids = []
        for str_id in ids:
            if str_id not in self.reverse_id_map:
                self.id_map[self._next_id] = str_id
                self.reverse_id_map[str_id] = self._next_id
                int_ids.append(self._next_id)
                self._next_id += 1
            else:
                int_ids.append(self.reverse_id_map[str_id])
        
        if self.index:
            try:
                # Train index if needed
                if hasattr(self.index, 'is_trained') and not self.index.is_trained:
                    if len(embeddings) >= self.index.nlist:
                        self.index.train(embeddings.astype(np.float32))
                
                self.index.add(embeddings.astype(np.float32))
            except Exception as e:
                logging.error(f"FAISS add failed: {e}")
                # Use fallback storage
                for i, embedding in enumerate(embeddings):
                    self._vectors[int_ids[i]] = embedding
        else:
            # Fallback storage
            for i, embedding in enumerate(embeddings):
                self._vectors[int_ids[i]] = embedding
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> Tuple[List[float], List[str]]:
        """Search for similar vectors"""
        query_embedding = query_embedding.reshape(1, -1).astype(np.float32)
        
        if self.index and hasattr(self.index, 'search'):
            try:
                distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
                
                # Convert to string IDs
                string_ids = []
                valid_distances = []
                for i, idx in enumerate(indices[0]):
                    if idx != -1 and idx in self.id_map:
                        string_ids.append(self.id_map[idx])
                        # Convert L2 distance to similarity score
                        similarity = 1.0 / (1.0 + distances[0][i])
                        valid_distances.append(similarity)
                
                return valid_distances, string_ids
            except Exception as e:
                logging.error(f"FAISS search failed: {e}")
        
        # Fallback to brute force search
        return self._brute_force_search(query_embedding[0], k)
    
    def _brute_force_search(self, query_embedding: np.ndarray, k: int) -> Tuple[List[float], List[str]]:
        """Fallback brute force search"""
        if not hasattr(self, '_vectors') or not self._vectors:
            return [], []
        
        similarities = []
        for int_id, vector in self._vectors.items():
            # Cosine similarity
            similarity = np.dot(query_embedding, vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(vector)
            )
            similarities.append((similarity, self.id_map[int_id]))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k
        top_k = similarities[:k]
        scores = [s[0] for s in top_k]
        ids = [s[1] for s in top_k]
        
        return scores, ids
    
    def remove_vector(self, str_id: str) -> bool:
        """Remove vector from index"""
        if str_id not in self.reverse_id_map:
            return False
        
        int_id = self.reverse_id_map[str_id]
        
        # Remove from mappings
        del self.id_map[int_id]
        del self.reverse_id_map[str_id]
        
        # Remove from fallback storage if used
        if hasattr(self, '_vectors') and int_id in self._vectors:
            del self._vectors[int_id]
        
        # Note: FAISS doesn't support efficient removal, would need rebuild
        return True
    
    def get_size(self) -> int:
        """Get number of vectors in index"""
        if self.index and hasattr(self.index, 'ntotal'):
            return self.index.ntotal
        elif hasattr(self, '_vectors'):
            return len(self._vectors)
        return 0

class VectorSearchEngine:
    """Advanced vector search engine for prompt memory"""
    
    def __init__(self, data_dir: str = "data/vector_search"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.embedding_model = SentenceTransformerModel()
        self.vector_index = VectorIndex(self.embedding_model.get_dimension())
        self.prompt_store: Dict[str, PromptEntry] = {}
        self.clusters: Dict[str, SemanticCluster] = {}
        
        self.db_path = self.data_dir / "prompts.db"
        self.index_path = self.data_dir / "vector_index.pkl"
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self._init_database()
        
        # Load existing data
        self._load_data()
    
    def _init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    category TEXT,
                    tags TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 1.0,
                    agent_name TEXT,
                    context TEXT,
                    embedding BLOB
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clusters (
                    id TEXT PRIMARY KEY,
                    centroid BLOB,
                    prompts TEXT,
                    category TEXT,
                    description TEXT,
                    created_at TEXT
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON prompts(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_agent ON prompts(agent_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_usage ON prompts(usage_count)")
    
    def _load_data(self):
        """Load existing prompts and index"""
        try:
            # Load prompts from database
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute("SELECT * FROM prompts")
                
                embeddings = []
                ids = []
                
                for row in cursor:
                    prompt_id, content, category, tags_str, created_at, updated_at, usage_count, success_rate, agent_name, context_str, embedding_blob = row
                    
                    # Reconstruct PromptEntry
                    entry = PromptEntry(
                        id=prompt_id,
                        content=content,
                        embedding=pickle.loads(embedding_blob) if embedding_blob else None,
                        category=category or "",
                        tags=json.loads(tags_str) if tags_str else [],
                        created_at=datetime.fromisoformat(created_at),
                        updated_at=datetime.fromisoformat(updated_at),
                        usage_count=usage_count,
                        success_rate=success_rate,
                        agent_name=agent_name,
                        context=json.loads(context_str) if context_str else None
                    )
                    
                    self.prompt_store[prompt_id] = entry
                    
                    if entry.embedding is not None:
                        embeddings.append(entry.embedding)
                        ids.append(prompt_id)
                
                # Add to vector index
                if embeddings:
                    self.vector_index.add_vectors(np.array(embeddings), ids)
                
                self.logger.info(f"Loaded {len(self.prompt_store)} prompts from database")
                
        except Exception as e:
            self.logger.error(f"Failed to load existing data: {e}")
    
    async def add_prompt(self, content: str, category: str = "", tags: List[str] = None, 
                        agent_name: str = None, context: Dict[str, Any] = None) -> str:
        """Add a new prompt to the search engine"""
        if tags is None:
            tags = []
        
        # Generate unique ID
        prompt_id = hashlib.md5(f"{content}_{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Generate embedding
        embedding = self.embedding_model.encode([content])[0]
        
        # Create prompt entry
        entry = PromptEntry(
            id=prompt_id,
            content=content,
            embedding=embedding,
            category=category,
            tags=tags,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            agent_name=agent_name,
            context=context
        )
        
        # Store in memory
        self.prompt_store[prompt_id] = entry
        
        # Add to vector index
        self.vector_index.add_vectors(embedding.reshape(1, -1), [prompt_id])
        
        # Persist to database
        await self._save_prompt_to_db(entry)
        
        self.logger.info(f"Added prompt {prompt_id} to search engine")
        return prompt_id
    
    async def _save_prompt_to_db(self, entry: PromptEntry):
        """Save prompt to database"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO prompts 
                (id, content, category, tags, created_at, updated_at, usage_count, 
                 success_rate, agent_name, context, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id,
                entry.content,
                entry.category,
                json.dumps(entry.tags),
                entry.created_at.isoformat(),
                entry.updated_at.isoformat(),
                entry.usage_count,
                entry.success_rate,
                entry.agent_name,
                json.dumps(entry.context) if entry.context else None,
                pickle.dumps(entry.embedding) if entry.embedding is not None else None
            ))
    
    async def search_similar(self, query: str, k: int = 10, category: str = None, 
                           agent_name: str = None, min_similarity: float = 0.0) -> List[SearchResult]:
        """Search for similar prompts"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Vector search
        similarities, ids = self.vector_index.search(query_embedding, k * 2)  # Get more candidates
        
        # Filter and rank results
        results = []
        for i, (similarity, prompt_id) in enumerate(zip(similarities, ids)):
            if prompt_id not in self.prompt_store:
                continue
            
            entry = self.prompt_store[prompt_id]
            
            # Apply filters
            if category and entry.category != category:
                continue
            if agent_name and entry.agent_name != agent_name:
                continue
            if similarity < min_similarity:
                continue
            
            results.append(SearchResult(
                entry=entry,
                similarity_score=similarity,
                rank=len(results) + 1
            ))
            
            if len(results) >= k:
                break
        
        # Update usage statistics
        for result in results:
            await self._update_usage_stats(result.entry.id)
        
        return results
    
    async def search_by_tags(self, tags: List[str], k: int = 10) -> List[SearchResult]:
        """Search prompts by tags"""
        results = []
        
        for prompt_id, entry in self.prompt_store.items():
            # Calculate tag overlap
            overlap = len(set(tags) & set(entry.tags))
            if overlap == 0:
                continue
            
            similarity_score = overlap / len(set(tags) | set(entry.tags))
            
            results.append(SearchResult(
                entry=entry,
                similarity_score=similarity_score,
                rank=0
            ))
        
        # Sort by similarity and assign ranks
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        for i, result in enumerate(results[:k]):
            result.rank = i + 1
        
        return results[:k]
    
    async def get_trending_prompts(self, days: int = 7, k: int = 10) -> List[SearchResult]:
        """Get trending prompts based on recent usage"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        trending = []
        for entry in self.prompt_store.values():
            if entry.updated_at >= cutoff_date and entry.usage_count > 0:
                # Score based on usage frequency and success rate
                score = entry.usage_count * entry.success_rate
                trending.append(SearchResult(
                    entry=entry,
                    similarity_score=score,
                    rank=0
                ))
        
        # Sort by score and assign ranks
        trending.sort(key=lambda x: x.similarity_score, reverse=True)
        for i, result in enumerate(trending[:k]):
            result.rank = i + 1
        
        return trending[:k]
    
    async def cluster_prompts(self, min_cluster_size: int = 3, max_clusters: int = 20) -> List[SemanticCluster]:
        """Cluster prompts semantically"""
        if len(self.prompt_store) < min_cluster_size:
            return []
        
        # Get all embeddings
        embeddings = []
        prompt_ids = []
        for prompt_id, entry in self.prompt_store.items():
            if entry.embedding is not None:
                embeddings.append(entry.embedding)
                prompt_ids.append(prompt_id)
        
        if not embeddings:
            return []
        
        embeddings = np.array(embeddings)
        
        try:
            from sklearn.cluster import KMeans
            
            # Determine optimal number of clusters
            n_clusters = min(max_clusters, max(2, len(embeddings) // min_cluster_size))
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Create clusters
            clusters = []
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_prompts = [prompt_ids[i] for i in range(len(prompt_ids)) if cluster_mask[i]]
                
                if len(cluster_prompts) >= min_cluster_size:
                    # Calculate centroid
                    centroid = embeddings[cluster_mask].mean(axis=0)
                    
                    # Generate cluster description
                    sample_prompts = [self.prompt_store[pid].content for pid in cluster_prompts[:3]]
                    description = f"Cluster of {len(cluster_prompts)} prompts: {', '.join(sample_prompts[:2])}..."
                    
                    # Determine dominant category
                    categories = [self.prompt_store[pid].category for pid in cluster_prompts]
                    dominant_category = max(set(categories), key=categories.count) if categories else ""
                    
                    cluster = SemanticCluster(
                        id=f"cluster_{cluster_id}",
                        centroid=centroid,
                        prompts=cluster_prompts,
                        category=dominant_category,
                        description=description,
                        created_at=datetime.now()
                    )
                    
                    clusters.append(cluster)
            
            # Cache clusters
            self.clusters = {cluster.id: cluster for cluster in clusters}
            
            return clusters
            
        except ImportError:
            self.logger.warning("sklearn not available, skipping clustering")
            return []
    
    async def _update_usage_stats(self, prompt_id: str):
        """Update usage statistics for a prompt"""
        if prompt_id in self.prompt_store:
            entry = self.prompt_store[prompt_id]
            entry.usage_count += 1
            entry.updated_at = datetime.now()
            
            # Save to database
            await self._save_prompt_to_db(entry)
    
    async def update_success_rate(self, prompt_id: str, success: bool):
        """Update success rate for a prompt"""
        if prompt_id not in self.prompt_store:
            return
        
        entry = self.prompt_store[prompt_id]
        
        # Update success rate using exponential moving average
        alpha = 0.1  # Learning rate
        new_success = 1.0 if success else 0.0
        entry.success_rate = (1 - alpha) * entry.success_rate + alpha * new_success
        entry.updated_at = datetime.now()
        
        await self._save_prompt_to_db(entry)
    
    async def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from the search engine"""
        if prompt_id not in self.prompt_store:
            return False
        
        # Remove from memory
        del self.prompt_store[prompt_id]
        
        # Remove from vector index
        self.vector_index.remove_vector(prompt_id)
        
        # Remove from database
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        
        self.logger.info(f"Deleted prompt {prompt_id}")
        return True
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        total_prompts = len(self.prompt_store)
        categories = {}
        agents = {}
        
        for entry in self.prompt_store.values():
            categories[entry.category] = categories.get(entry.category, 0) + 1
            if entry.agent_name:
                agents[entry.agent_name] = agents.get(entry.agent_name, 0) + 1
        
        return {
            'total_prompts': total_prompts,
            'categories': categories,
            'agents': agents,
            'index_size': self.vector_index.get_size(),
            'clusters': len(self.clusters),
            'embedding_dimension': self.embedding_model.get_dimension()
        }
    
    async def export_prompts(self, format: str = "json") -> str:
        """Export all prompts to file"""
        export_data = []
        
        for entry in self.prompt_store.values():
            export_entry = {
                'id': entry.id,
                'content': entry.content,
                'category': entry.category,
                'tags': entry.tags,
                'created_at': entry.created_at.isoformat(),
                'updated_at': entry.updated_at.isoformat(),
                'usage_count': entry.usage_count,
                'success_rate': entry.success_rate,
                'agent_name': entry.agent_name,
                'context': entry.context
            }
            export_data.append(export_entry)
        
        export_path = self.data_dir / f"prompts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == "json":
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return str(export_path)
