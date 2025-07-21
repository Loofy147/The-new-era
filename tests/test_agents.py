import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import agent modules
try:
    from plugins.cost_optimization_agent import CostOptimizationAgent
    from plugins.security_agent import SecurityHardeningAgent
    from plugins.privacy_agent import PrivacyGuardAgent
    from plugins.insights_agent import AnalyticsInsightsAgent
except ImportError as e:
    print(f"Warning: Could not import some agents: {e}")

class TestAgentInterface(unittest.TestCase):
    """Test that all agents implement the required interface"""
    
    def test_agents_have_run_method(self):
        """Test that all agents have a run method"""
        agent_classes = []
        
        # Try to import and test each agent
        try:
            from plugins.cost_optimization_agent import CostOptimizationAgent
            agent_classes.append(CostOptimizationAgent)
        except ImportError:
            pass
        
        try:
            from plugins.security_agent import SecurityHardeningAgent
            agent_classes.append(SecurityHardeningAgent)
        except ImportError:
            pass
        
        for agent_class in agent_classes:
            with self.subTest(agent=agent_class.__name__):
                agent = agent_class()
                self.assertTrue(hasattr(agent, 'run'))
                self.assertTrue(callable(getattr(agent, 'run')))

class TestCostOptimizationAgent(unittest.TestCase):
    """Test cases for CostOptimizationAgent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from plugins.cost_optimization_agent import CostOptimizationAgent
            self.agent = CostOptimizationAgent()
        except ImportError:
            self.skipTest("CostOptimizationAgent not available")
    
    def test_agent_initialization(self):
        """Test agent can be initialized"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "CostOptBot")
        self.assertEqual(self.agent.role, "Cost Optimization Agent")
    
    def test_agent_has_required_methods(self):
        """Test agent has required methods"""
        self.assertTrue(hasattr(self.agent, 'run'))
        self.assertTrue(hasattr(self.agent, 'get_metrics'))

class TestSecurityAgent(unittest.TestCase):
    """Test cases for SecurityHardeningAgent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from plugins.security_agent import SecurityHardeningAgent
            self.agent = SecurityHardeningAgent()
        except ImportError:
            self.skipTest("SecurityHardeningAgent not available")
    
    def test_agent_initialization(self):
        """Test agent can be initialized"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "SecuBot")
        self.assertEqual(self.agent.role, "Security Hardening Agent")
    
    def test_agent_has_required_methods(self):
        """Test agent has required methods"""
        self.assertTrue(hasattr(self.agent, 'run'))
        self.assertTrue(hasattr(self.agent, 'get_metrics'))

class TestPrivacyAgent(unittest.TestCase):
    """Test cases for PrivacyGuardAgent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from plugins.privacy_agent import PrivacyGuardAgent
            self.agent = PrivacyGuardAgent()
        except ImportError:
            self.skipTest("PrivacyGuardAgent not available")
    
    def test_agent_initialization(self):
        """Test agent can be initialized"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "PrivacyGuard")
        self.assertEqual(self.agent.role, "Data Privacy Agent")
    
    def test_agent_has_required_methods(self):
        """Test agent has required methods"""
        self.assertTrue(hasattr(self.agent, 'run'))
        self.assertTrue(hasattr(self.agent, 'get_metrics'))

class TestInsightsAgent(unittest.TestCase):
    """Test cases for AnalyticsInsightsAgent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from plugins.insights_agent import AnalyticsInsightsAgent
            self.agent = AnalyticsInsightsAgent()
        except ImportError:
            self.skipTest("AnalyticsInsightsAgent not available")
    
    def test_agent_initialization(self):
        """Test agent can be initialized"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "InsightsBot")
        self.assertEqual(self.agent.role, "Analytics & Insights Agent")
    
    def test_agent_has_required_methods(self):
        """Test agent has required methods"""
        self.assertTrue(hasattr(self.agent, 'run'))
        self.assertTrue(hasattr(self.agent, 'get_metrics'))

if __name__ == '__main__':
    unittest.main()
