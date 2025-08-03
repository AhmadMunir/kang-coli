#!/usr/bin/env python3
"""
Category Test Runner untuk PMO Recovery Bot
Menjalankan tests berdasarkan kategori tertentu
"""

import sys
import subprocess
from pathlib import Path

def run_category_tests(category):
    """Run tests for specific category"""
    
    categories = {
        "quick": ["quick_check.py", "simple_test.py"],
        "bot": ["test_bot.py", "test_handlers.py"],
        "emergency": ["test_emergency.py", "test_emergency_nav.py", "test_enhanced_emergency_protocols.py"],
        "journal": ["test_journal.py", "test_complete_journal.py", "test_journal_database.py"],
        "database": ["test_direct_database.py", "test_journal_database.py"]
    }
    
    if category not in categories:
        print(f"❌ Category '{category}' not found!")
        print(f"Available categories: {', '.join(categories.keys())}")
        return False
    
    test_files = categories[category]
    print(f"🧪 Running {category.upper()} tests...")
    print(f"Files: {', '.join(test_files)}")
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            print(f"\n▶️ Running {test_file}...")
            try:
                result = subprocess.run([sys.executable, str(test_path)], 
                                       capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {test_file} - PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_file} - FAILED")
                    if result.stderr.strip():
                        print(f"Error: {result.stderr.strip()}")
                    failed += 1
            except Exception as e:
                print(f"💥 {test_file} - ERROR: {e}")
                failed += 1
        else:
            print(f"⚠️ {test_file} - FILE NOT FOUND")
    
    print(f"\n📊 {category.upper()} TESTS SUMMARY:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    return failed == 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_category_tests.py <category>")
        print("Categories: quick, bot, emergency, journal, database")
        sys.exit(1)
    
    category = sys.argv[1].lower()
    success = run_category_tests(category)
    sys.exit(0 if success else 1)
