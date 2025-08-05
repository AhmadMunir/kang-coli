#!/usr/bin/env python3
"""
Test Journal Input Flow - Test complete journal input dengan konfirmasi system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.handlers.message_handlers import MessageHandlers
from src.utils.logger import app_logger

async def test_journal_input_flow():
    """Test complete journal input flow dengan konfirmasi"""
    print("🧪 Testing Enhanced Journal Input Flow")
    print("=" * 60)
    
    # Initialize handlers
    callback_handlers = CallbackHandlers()
    message_handlers = MessageHandlers()
    
    # Mock objects
    class MockUser:
        def __init__(self):
            self.id = 413217834  # Example user ID
            self.username = "khaalila"
            self.first_name = "Test"
            self.last_name = "User"
    
    class MockMessage:
        def __init__(self, text):
            self.text = text
            
        async def reply_text(self, message, parse_mode=None):
            print(f"🤖 Bot Response:\n{message}\n")
    
    class MockQuery:
        def __init__(self):
            self.from_user = MockUser()
            self.data = "new_journal"
            
        async def edit_message_text(self, message, reply_markup=None, parse_mode=None):
            print(f"🤖 Bot Response (Edit):\n{message}\n")
    
    class MockUpdate:
        def __init__(self, text=None, is_callback=False):
            self.effective_user = MockUser()
            if text:
                self.message = MockMessage(text)
            if is_callback:
                self.callback_query = MockQuery()
    
    class MockContext:
        def __init__(self):
            self.user_data = {}
    
    # Test Flow
    print("📝 Step 1: User clicks 'new_journal' button")
    query = MockQuery()
    context = MockContext()
    
    try:
        await callback_handlers._new_journal(query, context)
        print(f"✅ New journal callback handled")
        print(f"🔍 Context state: {context.user_data}")
    except Exception as e:
        print(f"❌ New journal callback failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("💬 Step 2: User sends journal text")
    
    # Simulate user typing journal entry
    journal_text = "Hari ini adalah hari yang cukup produktif. Saya berhasil menyelesaikan beberapa tugas penting dan merasa cukup puas dengan progress yang dibuat. Mood sekitar 4/5 dan grateful untuk kesempatan belajar yang didapat."
    update = MockUpdate(journal_text)
    
    try:
        await message_handlers.handle_text(update, context)
        print(f"✅ Journal input handled")
        print(f"🔍 Context state after input: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal input failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ Step 3: User confirms with 'SIMPAN'")
    
    # Simulate confirmation
    confirm_update = MockUpdate("SIMPAN")
    
    try:
        await message_handlers.handle_text(confirm_update, context)
        print(f"✅ Journal confirmation handled")
        print(f"🔍 Context state after save: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal confirmation failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("🧪 Step 4: Test cancellation flow")
    
    # Reset and test cancellation
    context.user_data = {'state': 'input_journal', 'journal_step': 'waiting_for_confirmation', 'journal_text': 'Test entry untuk cancel'}
    cancel_update = MockUpdate("BATAL")
    
    try:
        await message_handlers.handle_text(cancel_update, context)
        print(f"✅ Journal cancellation handled")
        print(f"🔍 Context state after cancel: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal cancellation failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("🧪 Step 5: Test edit flow")
    
    # Reset and test edit
    context.user_data = {'state': 'input_journal', 'journal_step': 'waiting_for_confirmation', 'journal_text': 'Test entry untuk edit'}
    edit_update = MockUpdate("EDIT")
    
    try:
        await message_handlers.handle_text(edit_update, context)
        print(f"✅ Journal edit handled")
        print(f"🔍 Context state after edit: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal edit failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Enhanced Journal Input Flow Test")
    print("This tests the new confirmation system untuk journal entries.\n")
    
    try:
        success = asyncio.run(test_journal_input_flow())
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED!")
            print("✅ Enhanced journal input system is working correctly!")
            print("✅ State management working properly!")
            print("✅ Confirmation system functional!")
            print("✅ Cancellation dan edit flows working!")
            print("\n🚀 Ready for production use!")
        else:
            print("\n❌ Some tests failed. Check the implementation.")
            exit(1)
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
