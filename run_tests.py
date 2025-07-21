#!/usr/bin/env python3
"""
Enhanced test runner for AI Operating System Framework
Includes coverage reporting and detailed test analysis
"""

import unittest
import sys
import os
import time
import json
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_test_suite():
    """Run comprehensive test suite with reporting"""
    print("🧪 AI Operating System Framework - Enhanced Test Suite")
    print("=" * 70)
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Test discovery
    loader = unittest.TestLoader()
    start_dir = 'tests'
    pattern = 'test_*.py'
    
    print(f"🔍 Discovering tests in {start_dir} with pattern {pattern}")
    
    try:
        suite = loader.discover(start_dir, pattern=pattern)
        test_count = suite.countTestCases()
        print(f"📊 Found {test_count} test cases")
    except Exception as e:
        print(f"❌ Test discovery failed: {e}")
        return False
    
    if test_count == 0:
        print("⚠️  No tests found!")
        # Create a basic test to ensure the system works
        create_basic_test()
        return False
    
    # Run tests
    print("\n🚀 Executing test suite...")
    print("-" * 70)
    
    # Custom test runner with detailed reporting
    stream = TestResultStream()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Analyze results
    test_analysis = analyze_test_results(result, execution_time)
    
    # Generate reports
    generate_test_reports(test_analysis, stream.get_output())
    
    # Print summary
    print_test_summary(test_analysis)
    
    return result.wasSuccessful()

class TestResultStream:
    """Custom stream to capture test output"""
    
    def __init__(self):
        self.output = []
    
    def write(self, text):
        self.output.append(text)
        sys.stdout.write(text)
    
    def flush(self):
        sys.stdout.flush()
    
    def get_output(self):
        return ''.join(self.output)

def analyze_test_results(result, execution_time):
    """Analyze test results and generate metrics"""
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    successful = total_tests - failures - errors - skipped
    
    success_rate = (successful / max(total_tests, 1)) * 100
    
    analysis = {
        "execution_timestamp": datetime.now().isoformat(),
        "execution_time_seconds": execution_time,
        "total_tests": total_tests,
        "successful": successful,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "success_rate": success_rate,
        "was_successful": result.wasSuccessful(),
        "test_details": {
            "failure_details": [
                {
                    "test": str(test),
                    "error": str(error).split('\n')[-2] if '\n' in str(error) else str(error)
                }
                for test, error in result.failures
            ],
            "error_details": [
                {
                    "test": str(test),
                    "error": str(error).split('\n')[-2] if '\n' in str(error) else str(error)
                }
                for test, error in result.errors
            ]
        },
        "performance_metrics": {
            "avg_test_time": execution_time / max(total_tests, 1),
            "tests_per_second": total_tests / max(execution_time, 0.1)
        }
    }
    
    return analysis

def generate_test_reports(analysis, test_output):
    """Generate comprehensive test reports"""
    
    # JSON Report
    with open('reports/test_execution_report.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    # Markdown Report
    generate_markdown_report(analysis)
    
    # HTML Report (simple)
    generate_html_report(analysis)
    
    print(f"\n📄 Test reports generated:")
    print(f"   • reports/test_execution_report.json")
    print(f"   • reports/test_execution_report.md")
    print(f"   • reports/test_execution_report.html")

def generate_markdown_report(analysis):
    """Generate markdown test report"""
    
    with open('reports/test_execution_report.md', 'w') as f:
        f.write("# Test Execution Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- **Total Tests**: {analysis['total_tests']}\n")
        f.write(f"- **Successful**: {analysis['successful']}\n")
        f.write(f"- **Failures**: {analysis['failures']}\n")
        f.write(f"- **Errors**: {analysis['errors']}\n")
        f.write(f"- **Skipped**: {analysis['skipped']}\n")
        f.write(f"- **Success Rate**: {analysis['success_rate']:.1f}%\n")
        f.write(f"- **Execution Time**: {analysis['execution_time_seconds']:.2f} seconds\n")
        f.write(f"- **Result**: {'✅ PASSED' if analysis['was_successful'] else '❌ FAILED'}\n\n")
        
        # Performance
        f.write("## Performance Metrics\n\n")
        perf = analysis['performance_metrics']
        f.write(f"- **Average Test Time**: {perf['avg_test_time']:.3f} seconds\n")
        f.write(f"- **Tests per Second**: {perf['tests_per_second']:.1f}\n\n")
        
        # Issues
        if analysis['test_details']['failure_details']:
            f.write("## Test Failures\n\n")
            for i, failure in enumerate(analysis['test_details']['failure_details'], 1):
                f.write(f"### {i}. {failure['test']}\n\n")
                f.write(f"```\n{failure['error']}\n```\n\n")
        
        if analysis['test_details']['error_details']:
            f.write("## Test Errors\n\n")
            for i, error in enumerate(analysis['test_details']['error_details'], 1):
                f.write(f"### {i}. {error['test']}\n\n")
                f.write(f"```\n{error['error']}\n```\n\n")

def generate_html_report(analysis):
    """Generate simple HTML test report"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Operating System Framework - Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f8ff; padding: 20px; border-radius: 8px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #f9f9f9; padding: 15px; border-radius: 5px; flex: 1; }}
        .success {{ color: #28a745; }}
        .failure {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 Test Execution Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Tests</h3>
            <h2>{analysis['total_tests']}</h2>
        </div>
        <div class="metric">
            <h3>Success Rate</h3>
            <h2 class="{'success' if analysis['success_rate'] > 80 else 'warning' if analysis['success_rate'] > 50 else 'failure'}">{analysis['success_rate']:.1f}%</h2>
        </div>
        <div class="metric">
            <h3>Execution Time</h3>
            <h2>{analysis['execution_time_seconds']:.2f}s</h2>
        </div>
        <div class="metric">
            <h3>Result</h3>
            <h2 class="{'success' if analysis['was_successful'] else 'failure'}">{'PASSED' if analysis['was_successful'] else 'FAILED'}</h2>
        </div>
    </div>
    
    <h2>Test Results Breakdown</h2>
    <ul>
        <li class="success">Successful: {analysis['successful']}</li>
        <li class="failure">Failures: {analysis['failures']}</li>
        <li class="failure">Errors: {analysis['errors']}</li>
        <li class="warning">Skipped: {analysis['skipped']}</li>
    </ul>
</body>
</html>
"""
    
    with open('reports/test_execution_report.html', 'w') as f:
        f.write(html_content)

def print_test_summary(analysis):
    """Print detailed test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 70)
    
    # Results
    print(f"Total Tests: {analysis['total_tests']}")
    print(f"Successful: {analysis['successful']}")
    print(f"Failures: {analysis['failures']}")
    print(f"Errors: {analysis['errors']}")
    print(f"Skipped: {analysis['skipped']}")
    print(f"Success Rate: {analysis['success_rate']:.1f}%")
    print(f"Execution Time: {analysis['execution_time_seconds']:.2f} seconds")
    
    # Performance
    perf = analysis['performance_metrics']
    print(f"Average Test Time: {perf['avg_test_time']:.3f} seconds")
    print(f"Tests per Second: {perf['tests_per_second']:.1f}")
    
    # Overall result
    if analysis['was_successful']:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        
        if analysis['failures'] > 0:
            print(f"   💥 {analysis['failures']} test failures")
        
        if analysis['errors'] > 0:
            print(f"   🚨 {analysis['errors']} test errors")
    
    print("=" * 70)

def create_basic_test():
    """Create a basic test if none exist"""
    print("📝 Creating basic test file...")
    
    os.makedirs('tests', exist_ok=True)
    
    basic_test_content = '''import unittest

class TestBasicSystem(unittest.TestCase):
    """Basic system tests"""
    
    def test_import_main(self):
        """Test that main module can be imported"""
        try:
            import main
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Could not import main module: {e}")
    
    def test_basic_functionality(self):
        """Test basic system functionality"""
        self.assertEqual(1 + 1, 2)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''
    
    with open('tests/test_basic.py', 'w') as f:
        f.write(basic_test_content)
    
    print("✅ Basic test file created")

def main():
    """Main test runner function"""
    success = run_test_suite()
    
    if success:
        print("\n🎉 Test suite completed successfully!")
    else:
        print("\n⚠️  Test suite completed with issues. Check reports for details.")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
