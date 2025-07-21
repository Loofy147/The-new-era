#!/usr/bin/env python3
"""
Comprehensive test runner for AI Operating System Framework
"""

import unittest
import sys
import os
import time
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""
    print("🧪 AI Operating System Framework - Test Suite")
    print("=" * 60)
    
    # Change to project root
    os.chdir(project_root)
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover tests
    start_dir = 'tests'
    pattern = 'test_*.py'
    
    print(f"📁 Discovering tests in {start_dir} with pattern {pattern}")
    
    suite = loader.discover(start_dir, pattern=pattern)
    
    # Count tests
    test_count = suite.countTestCases()
    print(f"🔍 Found {test_count} test cases")
    
    if test_count == 0:
        print("⚠️  No tests found!")
        return False
    
    print("\n🚀 Running tests...")
    print("-" * 60)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Generate test report
    generate_test_report(result, end_time - start_time)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Execution Summary")
    print("=" * 60)
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / max(result.testsRun, 1)) * 100
    
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    print("=" * 60)
    
    return result.wasSuccessful()

def generate_test_report(result, execution_time):
    """Generate detailed test report"""
    os.makedirs('reports', exist_ok=True)
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "execution_time_seconds": execution_time,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped) if hasattr(result, 'skipped') else 0,
        "success_rate": ((result.testsRun - len(result.failures) - len(result.errors)) / max(result.testsRun, 1)) * 100,
        "was_successful": result.wasSuccessful(),
        "failure_details": [],
        "error_details": []
    }
    
    # Add failure details
    for test, traceback in result.failures:
        report_data["failure_details"].append({
            "test": str(test),
            "traceback": traceback
        })
    
    # Add error details
    for test, traceback in result.errors:
        report_data["error_details"].append({
            "test": str(test),
            "traceback": traceback
        })
    
    # Save JSON report
    import json
    with open('reports/test_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    # Generate markdown report
    generate_markdown_report(report_data)
    
    print(f"\n📄 Test report saved to: reports/test_report.json")
    print(f"📄 Markdown report saved to: reports/test_report.md")

def generate_markdown_report(report_data):
    """Generate markdown test report"""
    
    with open('reports/test_report.md', 'w') as f:
        f.write("# Test Execution Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- **Tests Run**: {report_data['tests_run']}\n")
        f.write(f"- **Failures**: {report_data['failures']}\n")
        f.write(f"- **Errors**: {report_data['errors']}\n")
        f.write(f"- **Skipped**: {report_data['skipped']}\n")
        f.write(f"- **Success Rate**: {report_data['success_rate']:.1f}%\n")
        f.write(f"- **Execution Time**: {report_data['execution_time_seconds']:.2f} seconds\n")
        f.write(f"- **Result**: {'✅ PASSED' if report_data['was_successful'] else '❌ FAILED'}\n\n")
        
        # Failures
        if report_data['failure_details']:
            f.write("## Failures\n\n")
            for i, failure in enumerate(report_data['failure_details'], 1):
                f.write(f"### {i}. {failure['test']}\n\n")
                f.write("```\n")
                f.write(failure['traceback'])
                f.write("\n```\n\n")
        
        # Errors
        if report_data['error_details']:
            f.write("## Errors\n\n")
            for i, error in enumerate(report_data['error_details'], 1):
                f.write(f"### {i}. {error['test']}\n\n")
                f.write("```\n")
                f.write(error['traceback'])
                f.write("\n```\n\n")
        
        f.write("---\n")
        f.write("*Report generated by AI Operating System Framework test suite*\n")

def run_specific_test(test_module):
    """Run a specific test module"""
    print(f"🎯 Running specific test: {test_module}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """Main test runner function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Operating System Framework Test Runner')
    parser.add_argument('--test', '-t', help='Run specific test module')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.test:
        success = run_specific_test(args.test)
    else:
        success = discover_and_run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
