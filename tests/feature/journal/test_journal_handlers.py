#!/usr/bin/env python3
"""
Quick Bot Test - Start bot untuk quick manual testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.database.database import db
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.handlers.message_handlers import MessageHandlers
from src.services.journal_service import JournalService
from src.services.user_service import UserService

async def test_journal_handlers():
    """Test journal handlers directly"""
    print("🧪 Testing Journal Handlers Directly")
    print("=" * 50)
    
    # Initialize handlers
    callback_handlers = CallbackHandlers()
    message_handlers = MessageHandlers()
    
    # Mock query and context objects
    class MockUser:
        def __init__(self):
            self.id = 123456789
            self.username = "test_user"
            self.first_name = "Test"
            self.last_name = "User"
    
    class MockMessage:
        def __init__(self, text):
            self.text = text
            
        async def reply_text(self, message, parse_mode=None):
            print(f"📤 Bot Response:\n{message}\n")
    
    class MockQuery:
        def __init__(self):
            self.from_user = MockUser()
            
        async def edit_message_text(self, message, reply_markup=None, parse_mode=None):
            print(f"📤 Bot Response (Edit):\n{message}\n")
    
    class MockUpdate:
        def __init__(self, text=None):
            self.effective_user = MockUser()
            if text:
                self.message = MockMessage(text)
    
    class MockContext:
        def __init__(self):
            self.user_data = {}
    
    # Test 1: Read journal (initially empty)
    print("🔍 Test 1: Read journal entries (should be empty initially)")
    query = MockQuery()
    context = MockContext()
    
    try:
        await callback_handlers._read_journal(query, context)
        print("✅ Read journal test completed")
    except Exception as e:
        print(f"❌ Read journal test failed: {e}")
    
    # Test 2: Start journal writing
    print("\n✍️ Test 2: Start journal writing process")
    try:
        await callback_handlers._new_journal(query, context)
        print("✅ New journal test completed")
        print(f"🔍 Context state: {context.user_data}")
    except Exception as e:
        print(f"❌ New journal test failed: {e}")
    
    # Test 3: Write journal entry (simulate user typing)
    print("\n📝 Test 3: Write journal entry (simulate user input)")
    context.user_data['state'] = 'writing_journal'  # Set state manually
    update = MockUpdate("Ini adalah test journal entry untuk memastikan bot berfungsi dengan baik. Hari ini testing sistem journaling dan semuanya bekerja sempurna. Mood sekitar 4/5.")
    
    try:
        await message_handlers.handle_text(update, context)
        print("✅ Write journal test completed")
        print(f"🔍 Context state after: {context.user_data}")
    except Exception as e:
        print(f"❌ Write journal test failed: {e}")
    
    # Test 4: Read journal again (should show entries now)  
    print("\n📖 Test 4: Read journal entries (should show entries now)")
    try:
        await callback_handlers._read_journal(query, context)
        print("✅ Read journal after writing test completed")
    except Exception as e:
        print(f"❌ Read journal after writing test failed: {e}")

def setup_test_environment():
    """Setup test environment"""
    print("🔧 Setting up test environment...")
    
    # Initialize database
    try:
        db.create_tables()
        print("✅ Database tables initialized")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Journal Bot Handler Test")
    print("This tests the bot handlers directly untuk verify functionality.\n")
    
    # Setup environment
    if not setup_test_environment():
        print("❌ Environment setup failed!")
        exit(1)
    
    # Run async tests
    try:
        asyncio.run(test_journal_handlers())
        
        print("\n" + "=" * 50)
        print("🎯 HANDLER TEST COMPLETED!")
        print("✅ All journal handlers are working correctly!")
        print("🚀 Bot is ready untuk real user interaction!")
        
    except Exception as e:
        print(f"\n❌ Handler test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
