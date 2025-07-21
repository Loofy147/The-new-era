import pytest
from pathlib import Path
import os
import json
from services.prompt_memory.src.prompt_memory import PromptMemory

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

@pytest.fixture
def prompt_memory(temp_dir):
    storage_path = temp_dir / "prompts.json"
    index_path = temp_dir / "prompt_index.faiss"
    return PromptMemory(storage_path, index_path)

def test_add_prompt(prompt_memory):
    prompt = "This is a test prompt."
    prompt_memory.add(prompt)
    assert prompt in prompt_memory.get_all()

def test_get_all_prompts(prompt_memory):
    prompts = ["prompt1", "prompt2", "prompt3"]
    for p in prompts:
        prompt_memory.add(p)
    all_prompts = prompt_memory.get_all()
    assert len(all_prompts) == 3
    assert set(all_prompts) == set(prompts)

def test_search_prompts(prompt_memory):
    prompts = [
        "The quick brown fox jumps over the lazy dog.",
        "The five boxing wizards jump quickly.",
        "How vexingly quick daft zebras jump!",
    ]
    for p in prompts:
        prompt_memory.add(p)

    results = prompt_memory.search("fast animals", k=2)
    assert len(results) == 2
    assert all(r in prompts for r in results)
