#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PMO Recovery Bot - Test Organization Guide
==========================================

This file defines the recommended structure for organizing tests
and provides guidance on testing standards for the project.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from settings
try:
    from config.settings import settings
except ImportError:
    print("⚠️ Error: Could not import settings. Make sure you're running this from the project root.")
    sys.exit(1)

def print_test_structure():
    """Print the test structure guide"""
    print("\n" + "="*60)
    print("🧪 PMO RECOVERY BOT - TEST ORGANIZATION GUIDE")
    print("="*60)
    
    print("""
🔍 TEST STRUCTURE:

tests/
├── __init__.py                      # Test package initialization
├── README.md                        # Testing guide & documentation
├── conftest.py                      # Common fixtures & configuration
├── run_all_tests.py                 # Script to run all tests
├── run_category_tests.py            # Script to run tests by category
│
├── unit/                            # Unit tests for individual components
│   ├── __init__.py
│   ├── test_user_service.py         # Testing User Service functionality
│   ├── test_streak_service.py       # Testing Streak calculations
│   └── ...                          # Other unit tests
│
├── integration/                     # Integration tests between components
│   ├── __init__.py
│   ├── test_database_models.py      # Testing database model integrations
│   ├── test_service_interactions.py # Testing service interactions
│   └── ...                          # Other integration tests
│
├── functional/                      # Testing complete bot functions
│   ├── __init__.py
│   ├── test_handlers.py             # Testing message handlers
│   ├── test_callback_handlers.py    # Testing callback handlers
│   ├── test_commands.py             # Testing bot commands
│   └── ...                          # Other functional tests
│
├── feature/                         # Feature-specific tests
│   ├── __init__.py
│   ├── mood/                        # Mood tracking feature tests
│   │   ├── __init__.py
│   │   ├── test_mood_checkin.py     # Testing mood check-in flow
│   │   └── test_mood_analysis.py    # Testing mood analysis functionality
│   ├── broadcast/                   # Broadcast feature tests
│   │   ├── __init__.py
│   │   └── test_broadcast_mood.py   # Testing broadcast with mood integration
│   └── ...                          # Other feature-specific tests
│
└── utils/                           # Test utilities and helpers
    ├── __init__.py
    ├── mock_data.py                 # Mock data generators
    ├── test_helpers.py              # Helper functions for testing
    └── ...                          # Other test utilities
""")
    
    print("\n" + "="*60)
    print("📋 TESTING STANDARDS")
    print("="*60)
    
    print("""
1️⃣ **Naming Conventions**
   - All test files should be named with `test_` prefix
   - Test functions should be named `test_<what_is_being_tested>`
   - Test classes should be named `Test<ComponentName>`

2️⃣ **Test Documentation**
   - Each test file should have a docstring explaining what is tested
   - Each test function should have a clear, descriptive name
   - Complex tests should include comments explaining the test flow

3️⃣ **Test Structure**
   - Each test should follow the Arrange-Act-Assert pattern
   - Tests should be isolated and not depend on other tests
   - Use fixtures for common setup and teardown

4️⃣ **Test Coverage**
   - Aim for high test coverage of core functionality
   - Prioritize testing critical paths and edge cases
   - Include both happy path and error case testing

5️⃣ **Test Execution**
   - Use `python -m tests.run_all_tests` to run all tests
   - Use `python -m tests.run_category_tests <category>` for specific tests
   - Test new features before merging changes
""")

def get_test_info():
    """Get information about current test structure"""
    test_dir = Path(__file__).parent
    
    # Count test files
    test_files = list(test_dir.glob("test_*.py"))
    
    # Check for organized directories
    unit_dir = test_dir / "unit"
    integration_dir = test_dir / "integration"
    functional_dir = test_dir / "functional"
    feature_dir = test_dir / "feature"
    
    organized = all(d.exists() for d in [unit_dir, integration_dir, functional_dir, feature_dir])
    
    return {
        "total_tests": len(test_files),
        "organized": organized
    }

def organize_tests():
    """Create organized test directory structure"""
    test_dir = Path(__file__).parent
    
    # Create directories
    dirs = ["unit", "integration", "functional", "feature", "feature/mood", "feature/broadcast", "utils"]
    
    for d in dirs:
        dir_path = test_dir / d
        dir_path.mkdir(exist_ok=True)
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write('"""Test package for {}"""\n'.format(d))
    
    # Create README.md
    readme_path = test_dir / "README.md"
    if not readme_path.exists():
        with open(readme_path, 'w') as f:
            f.write("""# PMO Recovery Bot Tests

This directory contains tests for the PMO Recovery Bot project.

## Running Tests

```bash
# Run all tests
python -m tests.run_all_tests

# Run specific category
python -m tests.run_category_tests unit
python -m tests.run_category_tests feature.mood
```

## Test Structure

Tests are organized into the following categories:

- **unit**: Unit tests for individual components
- **integration**: Tests for interactions between components
- **functional**: Tests for complete bot functions
- **feature**: Feature-specific tests
  - **mood**: Mood tracking feature tests
  - **broadcast**: Broadcast system tests
- **utils**: Test utilities and helpers
""")
    
    # Create run_all_tests.py
    run_all_path = test_dir / "run_all_tests.py"
    if not run_all_path.exists():
        with open(run_all_path, 'w') as f:
            f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Run all tests for PMO Recovery Bot
\"\"\"

import os
import sys
import unittest
import argparse

def run_all_tests():
    \"\"\"Run all tests in the tests directory\"\"\"
    # Add project root to path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run PMO Recovery Bot tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    # Discover and run tests
    test_suite = unittest.defaultTestLoader.discover('.', pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = test_runner.run(test_suite)
    
    # Return proper exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
""")
    
    # Create run_category_tests.py
    run_category_path = test_dir / "run_category_tests.py"
    if not run_category_path.exists():
        with open(run_category_path, 'w') as f:
            f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Run tests for a specific category for PMO Recovery Bot
\"\"\"

import os
import sys
import unittest
import argparse

def run_category_tests(category):
    \"\"\"Run tests in the specified category\"\"\"
    # Add project root to path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run PMO Recovery Bot category tests')
    parser.add_argument('category', help='Test category to run (e.g., unit, integration, feature.mood)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    
    category_path = args.category.replace('.', '/')
    
    # Discover and run tests
    test_path = os.path.join(os.path.dirname(__file__), category_path)
    if not os.path.exists(test_path):
        print(f"Error: Category '{args.category}' not found")
        return 1
    
    test_suite = unittest.defaultTestLoader.discover(test_path, pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = test_runner.run(test_suite)
    
    # Return proper exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Please specify a test category")
        print("Usage: python -m tests.run_category_tests <category>")
        print("Example: python -m tests.run_category_tests unit")
        sys.exit(1)
    
    sys.exit(run_category_tests(sys.argv[1]))
""")
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="PMO Recovery Bot Test Organization")
    parser.add_argument("--organize", action="store_true", help="Create organized test directory structure")
    args = parser.parse_args()
    
    if args.organize:
        if organize_tests():
            print("\n✅ Test directories organized successfully!")
            print("   Check the tests/ directory for the new structure.")
    else:
        test_info = get_test_info()
        print_test_structure()
        
        print("\n" + "="*60)
        print("📊 CURRENT TEST STATUS")
        print("="*60)
        
        print(f"\n🧪 Total test files: {test_info['total_tests']}")
        print(f"🔧 Directory structure organized: {'✅ Yes' if test_info['organized'] else '❌ No'}")
        
        if not test_info['organized']:
            print("\n💡 Tip: Run with --organize to create the recommended directory structure:")
            print("   python -m tests.test_organization --organize")

if __name__ == "__main__":
    main()
