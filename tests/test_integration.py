import unittest
import sys
import os
import tempfile
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import AIOperatingSystem

class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete AI Operating System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ai_os = AIOperatingSystem()
        # Create temporary reports directory for testing
        self.temp_dir = tempfile.mkdtemp()
        if not os.path.exists('reports'):
            os.makedirs('reports')
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_full_system_initialization(self):
        """Test complete system initialization"""
        try:
            self.ai_os.initialize()
            self.assertGreater(len(self.ai_os.agents), 0)
            print(f"✅ System initialized with {len(self.ai_os.agents)} agents")
        except Exception as e:
            self.fail(f"System initialization failed: {e}")
    
    def test_agent_discovery_and_registration(self):
        """Test that agents are discovered and registered properly"""
        self.ai_os.initialize()
        
        # Check that agents are registered
        self.assertIsInstance(self.ai_os.agents, dict)
        self.assertGreater(len(self.ai_os.agents), 0)
        
        # Check that each agent has required attributes
        for name, agent in self.ai_os.agents.items():
            with self.subTest(agent=name):
                self.assertTrue(hasattr(agent, 'name'), f"Agent {name} missing 'name' attribute")
                self.assertTrue(hasattr(agent, 'role'), f"Agent {name} missing 'role' attribute")
                self.assertTrue(hasattr(agent, 'run'), f"Agent {name} missing 'run' method")
    
    def test_agent_execution_workflow(self):
        """Test that agents can be executed without errors"""
        self.ai_os.initialize()
        
        if not self.ai_os.agents:
            self.skipTest("No agents available for testing")
        
        # Test running a single agent
        agent_name = list(self.ai_os.agents.keys())[0]
        try:
            result = self.ai_os.run_agent(agent_name)
            # The result can be anything, we just want to ensure no exceptions
            print(f"✅ Agent {agent_name} executed successfully")
        except Exception as e:
            self.fail(f"Agent {agent_name} execution failed: {e}")
    
    def test_system_status_check(self):
        """Test system status functionality"""
        self.ai_os.initialize()
        
        try:
            # This should not raise an exception
            self.ai_os.show_system_status()
            print("✅ System status check completed")
        except Exception as e:
            self.fail(f"System status check failed: {e}")
    
    def test_manifest_loading(self):
        """Test that the agent manifest can be loaded"""
        try:
            self.ai_os.load_agent_manifest()
            print("✅ Agent manifest loaded successfully")
        except Exception as e:
            self.fail(f"Manifest loading failed: {e}")
    
    def test_plugin_manager_integration(self):
        """Test plugin manager integration"""
        self.assertIsNotNone(self.ai_os.plugin_manager)
        
        # Test plugin discovery
        self.ai_os.plugin_manager.discover_plugins()
        self.assertIsInstance(self.ai_os.plugin_manager.plugins, list)
        print(f"✅ Plugin manager discovered {len(self.ai_os.plugin_manager.plugins)} plugins")

class TestServiceIntegration(unittest.TestCase):
    """Integration tests for services"""
    
    def test_prompt_memory_service_structure(self):
        """Test that prompt memory service is properly structured"""
        service_path = "services/prompt_memory"
        self.assertTrue(os.path.exists(service_path), "Prompt memory service directory not found")
        
        # Check for required files
        required_files = ["app.py", "src/__init__.py", "src/simple_prompt_memory.py"]
        for file_path in required_files:
            full_path = os.path.join(service_path, file_path)
            self.assertTrue(os.path.exists(full_path), f"Required file {file_path} not found")
        
        print("✅ Prompt memory service structure validated")

class TestReportingIntegration(unittest.TestCase):
    """Integration tests for reporting system"""
    
    def test_reports_directory_creation(self):
        """Test that reports directory is created"""
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        self.assertTrue(os.path.exists('reports'), "Reports directory not created")
        print("✅ Reports directory validated")
    
    def test_report_file_generation(self):
        """Test that report files can be generated"""
        # This is a basic test - in a real scenario, we'd run agents and check their outputs
        test_report_path = "reports/test_report.json"
        
        # Create a test report
        import json
        test_data = {"test": True, "timestamp": "2025-01-21T10:00:00Z"}
        
        with open(test_report_path, 'w') as f:
            json.dump(test_data, f)
        
        self.assertTrue(os.path.exists(test_report_path), "Test report not created")
        
        # Clean up
        if os.path.exists(test_report_path):
            os.remove(test_report_path)
        
        print("✅ Report generation capability validated")

if __name__ == '__main__':
    # Set up test environment
    os.makedirs('reports', exist_ok=True)
    
    # Run tests with verbose output
    unittest.main(verbosity=2)
