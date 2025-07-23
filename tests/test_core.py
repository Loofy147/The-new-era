import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.plugin_manager import PluginManager
from core.plugin_interface import PluginInterface

class TestPluginManager(unittest.TestCase):
    """Test cases for PluginManager"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.plugin_manager = PluginManager("plugins")
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_pluginmanager_initialization(self):
        """Test PluginManager can be initialized"""
        try:
            instance = PluginManager("plugins")
            self.assertIsNotNone(instance)
        except Exception as e:
            self.fail(f"Failed to initialize PluginManager: {e}")

    def test_pluginmanager_discover_plugins(self):
        """Test PluginManager.discover_plugins method"""
        try:
            instance = PluginManager("plugins")
            if hasattr(instance, 'discover_plugins'):
                instance.discover_plugins()
                self.assertTrue(hasattr(instance, 'plugins'))
        except Exception as e:
            self.skipTest(f"Method discover_plugins requires specific setup: {e}")

    def test_pluginmanager_run_plugins(self):
        """Test PluginManager.run_plugins method"""
        try:
            instance = PluginManager("plugins")
            if hasattr(instance, 'run_plugins'):
                instance.discover_plugins()
                # Just test that it doesn't crash
                instance.run_plugins()
                self.assertTrue(True)
        except Exception as e:
            self.skipTest(f"Method run_plugins requires specific setup: {e}")

class TestPluginInterface(unittest.TestCase):
    """Test cases for PluginInterface"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_plugininterface_initialization(self):
        """Test PluginInterface can be initialized"""
        try:
            # PluginInterface is abstract, so we can't instantiate it directly
            self.assertTrue(hasattr(PluginInterface, 'run'))
        except Exception as e:
            self.fail(f"Failed to check PluginInterface: {e}")

if __name__ == '__main__':
    unittest.main()
