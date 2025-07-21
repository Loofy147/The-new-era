import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class PromptMemory:
    def __init__(self, storage_path: Path, index_path: Path):
        self.storage_path = storage_path
        self.index_path = index_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.prompts = self._load_prompts()
        self.index = self._load_index()

    def _load_prompts(self) -> list[str]:
        if not self.storage_path.exists():
            return []
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _load_index(self):
        if self.index_path.exists():
            return faiss.read_index(str(self.index_path))
        else:
            index = faiss.IndexFlatL2(384)
            return index

    def _save_prompts(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.prompts, f)

    def _save_index(self):
        faiss.write_index(self.index, str(self.index_path))

    def add(self, prompt: str):
        self.prompts.append(prompt)
        embedding = self.model.encode([prompt])
        self.index.add(embedding)
        self._save_prompts()
        self._save_index()

    def search(self, query: str, k: int = 5) -> list[str]:
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        return [self.prompts[i] for i in indices[0]]

    def get_all(self) -> list[str]:
        return self.prompts
