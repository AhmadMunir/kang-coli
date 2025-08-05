#!/usr/bin/env python3
"""
Test Journal Edit Callback Fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.utils.helpers import get_user_info
from src.utils.logger import app_logger

async def test_journal_edit_callback():
    """Test the fixed journal edit callback"""
    print("🧪 Testing Fixed Journal Edit Callback")
    print("=" * 50)
    
    # Mock objects
    class MockUser:
        def __init__(self):
            self.id = 413217834
            self.username = "test_user"
            self.first_name = "Test"
            self.last_name = "User"
    
    class MockQuery:
        def __init__(self):
            self.from_user = MockUser()
            self.data = "journal_edit"
            
        async def answer(self):
            pass
            
        async def edit_message_text(self, message, parse_mode=None):
            print(f"🤖 Bot Response (Edit):\n{message}\n")
    
    class MockContext:
        def __init__(self):
            self.user_data = {
                'state': 'input_journal',
                'journal_step': 'waiting_for_confirmation',
                'journal_text': 'Test journal entry to be edited'
            }
    
    # Initialize callback handlers
    callback_handlers = CallbackHandlers()
    
    # Test the edit callback
    query = MockQuery()
    context = MockContext()
    
    print("📝 Initial context state:")
    print(f"   State: {context.user_data.get('state')}")
    print(f"   Journal step: {context.user_data.get('journal_step')}")
    print(f"   Journal text: {context.user_data.get('journal_text')}")
    
    print("\n🔧 Testing journal edit callback...")
    
    try:
        await callback_handlers._journal_edit_callback(query, context)
        print("✅ Journal edit callback executed successfully!")
        
        print("\n📝 Context state after edit:")
        print(f"   State: {context.user_data.get('state')}")
        print(f"   Journal step: {context.user_data.get('journal_step')}")
        print(f"   Journal text: {context.user_data.get('journal_text')}")
        
        # Verify state changes
        if context.user_data.get('state') == 'input_journal':
            print("✅ State correctly set to 'input_journal'")
        else:
            print("❌ State not set correctly")
            return False
            
        if context.user_data.get('journal_step') == 'waiting_for_text':
            print("✅ Journal step correctly set to 'waiting_for_text'")
        else:
            print("❌ Journal step not set correctly")
            return False
            
        if 'journal_text' not in context.user_data:
            print("✅ Journal text correctly cleared")
        else:
            print("❌ Journal text not cleared")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Journal edit callback failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Journal Edit Callback Fix Test")
    print("This tests if the NameError in _journal_edit_callback is fixed.\n")
    
    try:
        success = asyncio.run(test_journal_edit_callback())
        
        if success:
            print("\n" + "=" * 50)
            print("🎉 JOURNAL EDIT CALLBACK FIX SUCCESSFUL!")
            print("✅ No more NameError exception!")
            print("✅ State management working correctly!")
            print("✅ Journal text properly cleared for rewrite!")
            print("✅ User can now edit journal entries!")
            print("\n🚀 Edit functionality ready for production!")
        else:
            print("\n❌ Journal edit callback still has issues.")
            exit(1)
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
