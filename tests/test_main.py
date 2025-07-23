"""
Test suite for AI Operating System Framework main system
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import AIOperatingSystem

class TestAIOperatingSystem(unittest.TestCase):
    """Test cases for the main AI Operating System class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ai_os = AIOperatingSystem()
    
    def test_initialization(self):
        """Test AI Operating System initialization"""
        self.assertIsNotNone(self.ai_os)
        self.assertIsNotNone(self.ai_os.plugin_manager)
        self.assertEqual(self.ai_os.manifest_path, "ai-agents-manifest.json")
    
    def test_agent_discovery(self):
        """Test agent discovery process"""
        self.ai_os.plugin_manager.discover_plugins()
        self.assertGreater(len(self.ai_os.plugin_manager.plugins), 0)
    
    def test_agent_registration(self):
        """Test agent registration"""
        self.ai_os.initialize()
        self.assertGreater(len(self.ai_os.agents), 0)
        
        # Check that each agent has required attributes
        for name, agent in self.ai_os.agents.items():
            self.assertTrue(hasattr(agent, 'name'))
            self.assertTrue(hasattr(agent, 'role'))
            self.assertTrue(hasattr(agent, 'run'))
    
    def test_manifest_loading(self):
        """Test loading agent manifest"""
        self.ai_os.load_agent_manifest()
        # Should not raise any exceptions
    
    def test_system_status(self):
        """Test system status functionality"""
        self.ai_os.initialize()
        # Should not raise any exceptions
        try:
            self.ai_os.show_system_status()
        except Exception as e:
            self.fail(f"System status check failed: {e}")

class TestPluginSystem(unittest.TestCase):
    """Test cases for the plugin system"""
    
    def setUp(self):
        """Set up test fixtures"""
        from core.plugin_manager import PluginManager
        self.plugin_manager = PluginManager("plugins")
    
    def test_plugin_discovery(self):
        """Test plugin discovery"""
        self.plugin_manager.discover_plugins()
        self.assertIsInstance(self.plugin_manager.plugins, list)
    
    def test_plugin_interface(self):
        """Test that all plugins implement the required interface"""
        self.plugin_manager.discover_plugins()
        
        for plugin in self.plugin_manager.plugins:
            self.assertTrue(hasattr(plugin, 'run'), f"Plugin {plugin} missing run method")
            self.assertTrue(callable(getattr(plugin, 'run')), f"Plugin {plugin} run method not callable")

class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_execution(self):
        """Test complete system execution"""
        ai_os = AIOperatingSystem()
        ai_os.initialize()
        
        # Should have agents registered
        self.assertGreater(len(ai_os.agents), 0)
        
        # Test running a single agent (if available)
        if ai_os.agents:
            agent_name = list(ai_os.agents.keys())[0]
            try:
                result = ai_os.run_agent(agent_name)
                # Result can be None or any value, just shouldn't crash
            except Exception as e:
                self.fail(f"Agent execution failed: {e}")

    def test_run_all_agents_execution(self):
        """Test the execution of all agents"""
        ai_os = AIOperatingSystem()
        ai_os.initialize()

        # Should have agents registered
        self.assertGreater(len(ai_os.agents), 0)

        try:
            results = ai_os.run_all_agents()
            self.assertIsInstance(results, dict)
            self.assertEqual(len(results), len(ai_os.agents))
        except Exception as e:
            self.fail(f"run_all_agents failed: {e}")

if __name__ == '__main__':
    # Create reports directory for test outputs
    os.makedirs('reports', exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)
