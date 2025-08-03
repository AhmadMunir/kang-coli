#!/usr/bin/env python3
"""
Master Test Runner untuk PMO Recovery Bot
Menjalankan semua tests dalam folder tests/
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"🧪 RUNNING: {test_file}")
    print(f"{'='*60}")
    
    try:
        # Change to project root directory
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Run the test
        result = subprocess.run(
            [sys.executable, f"tests/{test_file}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {test_file} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file} - TIMEOUT (>30s)")
        return False
    except Exception as e:
        print(f"💥 {test_file} - EXCEPTION: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PMO Recovery Bot - Master Test Runner")
    print("=" * 60)
    
    # Get all test files
    tests_dir = Path(__file__).parent
    test_files = []
    
    # Categorize tests
    quick_tests = ["quick_check.py", "simple_test.py"]
    bot_tests = ["test_bot.py", "test_handlers.py"]
    emergency_tests = ["test_emergency.py", "test_emergency_nav.py"]
    
    print("📋 Test Categories:")
    print(f"🚀 Quick Tests: {len(quick_tests)} files")
    print(f"🤖 Bot Tests: {len(bot_tests)} files") 
    print(f"🆘 Emergency Tests: {len(emergency_tests)} files")
    
    # Run tests by category
    all_results = {}
    
    print(f"\n🚀 Running Quick Tests...")
    for test in quick_tests:
        if (tests_dir / test).exists():
            all_results[test] = run_test(test)
            time.sleep(1)  # Brief pause between tests
    
    print(f"\n🤖 Running Bot Tests...")
    for test in bot_tests:
        if (tests_dir / test).exists():
            all_results[test] = run_test(test)
            time.sleep(1)
    
    print(f"\n🆘 Running Emergency Tests...")
    for test in emergency_tests:
        if (tests_dir / test).exists():
            all_results[test] = run_test(test)
            time.sleep(1)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for result in all_results.values() if result)
    failed = len(all_results) - passed
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(all_results)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Bot is ready for deployment.")
    else:
        print(f"\n⚠️ {failed} tests failed. Please check and fix issues.")
        
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
