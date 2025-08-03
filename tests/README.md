# 🧪 Test Suite Documentation

## Overview
Folder ini berisi semua test files untuk PMO Recovery Coach AI Bot. Tests ini digunakan untuk verify functionality, debug issues, dan ensure quality dari bot system.

## Test Files Structure

### 📊 Database Tests
- **`test_direct_database.py`** - Direct SQLite database connectivity dan schema verification
- **`test_journal_database.py`** - Journal-specific database operations testing
- **`test_complete_journal_workflow.py`** - End-to-end journal workflow testing

### 🤖 Bot Handler Tests  
- **`test_bot.py`** - Comprehensive bot setup dan component testing
- **`test_handlers.py`** - Handler functionality testing
- **`test_journal_handlers.py`** - Journal callback dan message handlers testing
- **`test_mood.py`** - Mood tracking functionality testing

### 🆘 Emergency System Tests
- **`test_emergency.py`** - Emergency callback routing testing
- **`test_emergency_nav.py`** - Emergency navigation enhancement testing
- **`test_enhanced_emergency_protocols.py`** - Enhanced emergency protocols testing

### 🔧 Service Tests
- **`test_journal.py`** - JournalService methods testing
- **`test_broadcast.py`** - Broadcast service dan scheduling testing

### 🚀 Quick Tests
- **`quick_check.py`** - Simple import dan dependency check
- **`quick_test.py`** - Quick functionality verification
- **`simple_test.py`** - Basic import testing

### 🔍 Validation Tests
- **`validate_fix.py`** - Bug fix validation
- **`test_implementation.py`** - Implementation verification
- **`test_complete_journal.py`** - Complete journal feature testing

### 🔍 Utility Files
- **`enhanced_journal_reader.py`** - Enhanced journal reading functionality utility

## How to Run Tests

### Run Individual Tests
```bash
# Database connectivity test
python tests/test_direct_database.py

# Complete journal workflow test  
python tests/test_complete_journal_workflow.py

# Bot handlers test
python tests/test_journal_handlers.py
```

### Run All Tests
```bash
# From project root
python -m pytest tests/ -v

# Or run individually
for test in tests/test_*.py; do python "$test"; done
```

## Test Categories

### ✅ Database Tests
These tests verify that:
- SQLite database dapat created dan accessed
- Tables exist dengan proper schema
- CRUD operations working correctly
- Transaction handling is secure
- Data integrity is maintained

### ✅ Service Tests  
These tests verify that:
- Service classes initialize properly
- Business logic methods work correctly
- Error handling is robust
- Data validation is effective

### ✅ Handler Tests
These tests verify that:
- Telegram bot handlers respond correctly
- State management works properly
- User input is processed correctly
- Bot responses are appropriate

### ✅ Integration Tests
These tests verify that:
- End-to-end workflows function properly
- Components integrate seamlessly
- User experience is smooth
- System behavior is predictable

## Test Results Summary

### 🎯 Recent Test Results
- ✅ **Database Tests**: All passing - SQLite working correctly
- ✅ **Journal Workflow**: All passing - Complete functionality verified
- ✅ **Bot Handlers**: All passing - User interaction working
- ✅ **Service Layer**: All passing - Business logic verified

### 📊 Coverage Areas
- **Database Storage**: ✅ Verified working
- **Journal Writing**: ✅ Verified working  
- **Journal Reading**: ✅ Verified working
- **Statistics**: ✅ Verified working
- **Error Handling**: ✅ Verified working
- **User Experience**: ✅ Verified working

## Adding New Tests

### Test File Naming Convention
- `test_[component_name].py` - For component-specific tests
- `test_[feature_name]_workflow.py` - For end-to-end workflow tests
- `test_[integration_name].py` - For integration tests

### Test Structure Template
```python
#!/usr/bin/env python3
"""
Test Description
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components to test
from src.services.your_service import YourService

def test_your_functionality():
    """Test description"""
    # Test implementation
    pass

if __name__ == "__main__":
    print("🚀 Starting Your Test...")
    # Run tests
    print("✅ Test completed!")
```

## Troubleshooting Tests

### Common Issues
1. **Import Errors**: Check sys.path.append line points to correct directory
2. **Database Errors**: Ensure data/ directory exists dan writable
3. **Service Errors**: Verify all dependencies are installed
4. **Handler Errors**: Check mock objects are properly configured

### Debug Tips
- Use `print()` statements untuk verbose output
- Check log files dalam `logs/` directory
- Verify database state dengan direct SQLite queries
- Test components individually before integration tests

## Quality Assurance

### Test Standards
- ✅ All tests should be self-contained
- ✅ Tests should clean up after themselves
- ✅ Tests should provide clear pass/fail indicators
- ✅ Tests should include comprehensive error handling
- ✅ Tests should document expected behavior

### Continuous Testing
- Run tests before commits
- Verify tests pass after major changes
- Add new tests untuk new features
- Update tests when requirements change

---
**Maintained by**: PMO Recovery Team  
**Last Updated**: August 3, 2025  
**Test Coverage**: Comprehensive  
**Status**: All tests passing ✅
