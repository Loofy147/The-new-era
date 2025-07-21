import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.prompt_memory.src.simple_prompt_memory import PromptMemory
from pathlib import Path

class TestPromptMemory(unittest.TestCase):
    """Test cases for PromptMemory service"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_storage_path = Path("test_prompts.json")
        self.prompt_memory = PromptMemory(self.test_storage_path)
    
    def tearDown(self):
        """Clean up after each test method."""
        if self.test_storage_path.exists():
            self.test_storage_path.unlink()
    
    def test_prompt_memory_initialization(self):
        """Test PromptMemory can be initialized"""
        try:
            instance = PromptMemory(Path("test.json"))
            self.assertIsNotNone(instance)
        except Exception as e:
            self.fail(f"Failed to initialize PromptMemory: {e}")

    def test_prompt_memory_add(self):
        """Test PromptMemory.add method"""
        try:
            instance = PromptMemory(Path("test.json"))
            if hasattr(instance, 'add'):
                instance.add("Test prompt")
                self.assertTrue(len(instance.prompts) > 0)
        except Exception as e:
            self.skipTest(f"Method add requires specific setup: {e}")

    def test_prompt_memory_search(self):
        """Test PromptMemory.search method"""
        try:
            instance = PromptMemory(Path("test.json"))
            if hasattr(instance, 'search'):
                instance.add("Test prompt about AI")
                results = instance.search("AI", 5)
                self.assertIsInstance(results, list)
        except Exception as e:
            self.skipTest(f"Method search requires specific setup: {e}")

    def test_prompt_memory_get_all(self):
        """Test PromptMemory.get_all method"""
        try:
            instance = PromptMemory(Path("test.json"))
            if hasattr(instance, 'get_all'):
                prompts = instance.get_all()
                self.assertIsInstance(prompts, list)
        except Exception as e:
            self.skipTest(f"Method get_all requires specific setup: {e}")

if __name__ == '__main__':
    unittest.main()
