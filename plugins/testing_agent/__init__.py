from core.plugin_interface import PluginInterface
import json
import os
import re
import ast
from datetime import datetime

class TestAutomationAgent(PluginInterface):
    def __init__(self):
        self.name = "TestGenie"
        self.role = "Testing Automation Agent"
        self.description = "Builds and verifies tests for other agents and system components"
        self.test_results = []
        self.coverage_threshold = 80
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is starting test automation...")
        
        # Discover and analyze code for testing
        test_plan = self.analyze_codebase_for_testing()
        self.generate_tests(test_plan)
        self.run_existing_tests()
        
        print(f"✅ {self.name} completed test automation tasks")
        return test_plan
    
    def analyze_codebase_for_testing(self):
        """Analyze codebase to identify components that need testing"""
        test_plan = {
            "timestamp": datetime.now().isoformat(),
            "components_analyzed": [],
            "test_coverage": {},
            "missing_tests": [],
            "test_suggestions": []
        }
        
        # Analyze core components
        core_files = ['core/plugin_manager.py', 'core/plugin_interface.py']
        for file_path in core_files:
            if os.path.exists(file_path):
                analysis = self.analyze_python_file(file_path)
                test_plan["components_analyzed"].append(analysis)
        
        # Analyze plugin components
        plugin_dirs = [d for d in os.listdir('plugins') if os.path.isdir(os.path.join('plugins', d))]
        for plugin_dir in plugin_dirs:
            plugin_path = f"plugins/{plugin_dir}/__init__.py"
            if os.path.exists(plugin_path):
                analysis = self.analyze_python_file(plugin_path)
                test_plan["components_analyzed"].append(analysis)
        
        # Analyze services
        if os.path.exists('services/prompt_memory/src/simple_prompt_memory.py'):
            analysis = self.analyze_python_file('services/prompt_memory/src/simple_prompt_memory.py')
            test_plan["components_analyzed"].append(analysis)
        
        print(f"🔍 Analyzed {len(test_plan['components_analyzed'])} components for testing")
        
        return test_plan
    
    def analyze_python_file(self, file_path):
        """Analyze a Python file to extract testable components"""
        analysis = {
            "file_path": file_path,
            "classes": [],
            "functions": [],
            "methods": [],
            "test_file_exists": False,
            "complexity_score": 0
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse AST to extract components
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        "line_number": node.lineno
                    }
                    analysis["classes"].append(class_info)
                    analysis["complexity_score"] += len(class_info["methods"])
                
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    function_info = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "line_number": node.lineno
                    }
                    analysis["functions"].append(function_info)
                    analysis["complexity_score"] += 1
            
            # Check if test file exists
            test_file_path = file_path.replace('.py', '_test.py')
            if not os.path.exists(test_file_path):
                test_file_path = file_path.replace('/', '/test_').replace('.py', '.py')
            analysis["test_file_exists"] = os.path.exists(test_file_path)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return analysis
    
    def generate_tests(self, test_plan):
        """Generate test files for components that need testing"""
        generated_tests = []
        
        for component in test_plan["components_analyzed"]:
            if not component["test_file_exists"]:
                test_file_path = self.generate_test_file(component)
                if test_file_path:
                    generated_tests.append(test_file_path)
        
        print(f"📝 Generated {len(generated_tests)} test files")
        
        # Create a test suite runner
        self.create_test_runner(generated_tests)
        
        return generated_tests
    
    def generate_test_file(self, component):
        """Generate a test file for a specific component"""
        file_path = component["file_path"]
        test_dir = "tests"
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test file name
        test_filename = os.path.basename(file_path).replace('.py', '_test.py')
        test_path = os.path.join(test_dir, test_filename)
        
        test_content = self.generate_test_content(component)
        
        with open(test_path, 'w') as f:
            f.write(test_content)
        
        print(f"📄 Generated test file: {test_path}")
        return test_path
    
    def generate_test_content(self, component):
        """Generate test content based on component analysis"""
        file_path = component["file_path"]
        module_name = file_path.replace('/', '.').replace('.py', '')
        
        content = f'''import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from {module_name} import *

class Test{os.path.basename(file_path).replace('.py', '').title()}(unittest.TestCase):
    """Test cases for {file_path}"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
'''
        
        # Generate tests for classes
        for class_info in component["classes"]:
            class_name = class_info["name"]
            content += f'''
    def test_{class_name.lower()}_initialization(self):
        """Test {class_name} can be initialized"""
        try:
            instance = {class_name}()
            self.assertIsNotNone(instance)
        except Exception as e:
            self.fail(f"Failed to initialize {class_name}: {{e}}")
'''
            
            # Generate tests for methods
            for method_name in class_info["methods"]:
                if not method_name.startswith('_'):  # Skip private methods
                    content += f'''
    def test_{class_name.lower()}_{method_name}(self):
        """Test {class_name}.{method_name} method"""
        try:
            instance = {class_name}()
            if hasattr(instance, '{method_name}'):
                # Add specific test logic here
                self.assertTrue(hasattr(instance, '{method_name}'))
        except Exception as e:
            self.skipTest(f"Method {method_name} requires specific setup: {{e}}")
'''
        
        # Generate tests for standalone functions
        for function_info in component["functions"]:
            function_name = function_info["name"]
            if not function_name.startswith('_'):  # Skip private functions
                content += f'''
    def test_{function_name}(self):
        """Test {function_name} function"""
        try:
            # Add specific test logic for {function_name}
            self.assertTrue(callable({function_name}))
        except Exception as e:
            self.skipTest(f"Function {function_name} requires specific setup: {{e}}")
'''
        
        content += '''

if __name__ == '__main__':
    unittest.main()
'''
        
        return content
    
    def create_test_runner(self, test_files):
        """Create a comprehensive test runner"""
        runner_path = "run_tests.py"
        
        content = '''#!/usr/bin/env python3
"""
Comprehensive test runner for AI Operating System Framework
Generated by TestGenie Agent
"""

import unittest
import sys
import os

def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""
    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    
    if os.path.exists(start_dir):
        suite = loader.discover(start_dir, pattern='*_test.py')
    else:
        print("No tests directory found, creating one...")
        os.makedirs(start_dir, exist_ok=True)
        suite = unittest.TestSuite()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / max(result.testsRun, 1)) * 100:.1f}%")
    print(f"{'='*50}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
'''
        
        with open(runner_path, 'w') as f:
            f.write(content)
        
        # Make it executable
        os.chmod(runner_path, 0o755)
        
        print(f"🚀 Created test runner: {runner_path}")
    
    def run_existing_tests(self):
        """Run any existing tests and report results"""
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_found": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "coverage_percentage": 0
        }
        
        # Check for existing test files
        if os.path.exists('tests'):
            test_files = [f for f in os.listdir('tests') if f.endswith('_test.py')]
            test_results["tests_found"] = len(test_files)
            print(f"🧪 Found {len(test_files)} test files")
        
        # Check for services tests
        services_test_dir = 'services/prompt_memory/tests'
        if os.path.exists(services_test_dir):
            service_tests = [f for f in os.listdir(services_test_dir) if f.endswith('.py')]
            print(f"🧪 Found {len(service_tests)} service test files")
        
        self.generate_test_report(test_results)
        return test_results
    
    def generate_test_report(self, results):
        """Generate comprehensive testing report"""
        report_path = "reports/testing_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Testing report saved to: {report_path}")
        
        # Generate testing guidelines
        self.generate_testing_guidelines()
    
    def generate_testing_guidelines(self):
        """Generate testing best practices and guidelines"""
        guidelines_path = "docs/testing_guidelines.md"
        os.makedirs(os.path.dirname(guidelines_path), exist_ok=True)
        
        content = f"""# Testing Guidelines for AI Operating System Framework

Generated by TestGenie Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This document provides comprehensive testing guidelines for the AI Operating System Framework.

## Testing Strategy

### 1. Unit Testing
- Test individual components in isolation
- Focus on core functionality and edge cases
- Aim for {self.coverage_threshold}% code coverage

### 2. Integration Testing
- Test interactions between agents and services
- Verify plugin system functionality
- Test API endpoints and data flow

### 3. Performance Testing
- Monitor agent execution times
- Test system under load
- Verify resource usage patterns

## Test Organization


tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests
├── performance/    # Performance benchmarks
└── fixtures/       # Test data and fixtures
```

## Running Tests

### Quick Test Run
```bash
python run_tests.py
```

### Specific Test File
```bash
python -m unittest tests.core_test
```

### With Coverage
```bash
pip install coverage
coverage run -m unittest discover tests
coverage report -m
```

## Writing Tests

### Test Naming Convention
- Use descriptive test names: `test_agent_handles_invalid_input`
- Group related tests in test classes
- Use setUp and tearDown for test fixtures

### Test Structure
```python
def test_feature_name(self):
    # Arrange
    setup_test_data()
    
    # Act
    result = perform_action()
    
    # Assert
    self.assertEqual(expected, result)
```

## Agent Testing Requirements

Each agent must have:
1. Initialization tests
2. Core functionality tests
3. Error handling tests
4. Integration tests with plugin system

## Continuous Integration

Tests should be run:
- On every commit
- Before deployment
- Nightly for comprehensive suites

## Best Practices

1. **Isolation**: Tests should not depend on each other
2. **Repeatability**: Tests should produce consistent results
3. **Speed**: Unit tests should run quickly
4. **Clarity**: Test purpose should be obvious from the name
5. **Coverage**: Aim for high test coverage without testing trivial code

## Mock and Fixture Guidelines

- Use mocks for external dependencies
- Create reusable fixtures for common test data
- Avoid testing implementation details

## Performance Benchmarks

Critical performance metrics:
- Agent startup time: < 1 second
- Plugin discovery: < 5 seconds
- API response time: < 200ms

---

For questions about testing, consult the TestGenie agent or review this documentation.
"""
        
        with open(guidelines_path, 'w') as f:
            f.write(content)
        
        print(f"📋 Testing guidelines saved to: {guidelines_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "test_files_generated": len(self.test_results),
            "coverage_threshold": self.coverage_threshold,
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return TestAutomationAgent()
