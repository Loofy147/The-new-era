import json
from pathlib import Path

class PromptMemory:
    def __init__(self, storage_path: Path, index_path: Path = None):
        self.storage_path = storage_path
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> list[str]:
        if not self.storage_path.exists():
            return []
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _save_prompts(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.prompts, f)

    def add(self, prompt: str):
        self.prompts.append(prompt)
        self._save_prompts()

    def search(self, query: str, k: int = 5) -> list[str]:
        # Simple keyword-based search for demo purposes
        query_lower = query.lower()
        matches = []
        for prompt in self.prompts:
            if query_lower in prompt.lower():
                matches.append(prompt)
        return matches[:k]

    def get_all(self) -> list[str]:
        return self.prompts
