#!/usr/bin/env python3
"""
Test Runner - Run all tests dalam tests/ folder dengan clean reporting
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test_file(test_file):
    """Run individual test file"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
            if result.stdout:
                # Show only summary lines
                lines = result.stdout.split('\n')
                summary_lines = [line for line in lines if any(keyword in line.lower() 
                               for keyword in ['✅', '❌', '🎉', 'passed', 'failed', 'completed'])]
                if summary_lines:
                    print("📊 Summary:")
                    for line in summary_lines[-3:]:  # Show last 3 summary lines
                        if line.strip():
                            print(f"   {line}")
        else:
            print(f"❌ {test_file} - FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ {test_file} - ERROR: {e}")
        return False

def main():
    """Run all tests dalam tests folder"""
    print("🚀 PMO Recovery Bot - Test Suite Runner")
    print("=" * 60)
    
    # Find all test files
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("❌ Tests directory not found!")
        return False
    
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("❌ No test files found!")
        return False
    
    print(f"📋 Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"   • {test_file.name}")
    
    # Run tests
    results = {}
    passed = 0
    failed = 0
    
    for test_file in sorted(test_files):
        success = run_test_file(str(test_file))
        results[test_file.name] = success
        
        if success:
            passed += 1
        else:
            failed += 1
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUITE SUMMARY")
    print(f"{'='*60}")
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(test_files)}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! Test suite is working correctly! ✨")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Check individual test outputs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
