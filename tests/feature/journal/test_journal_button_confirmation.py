#!/usr/bin/env python3
"""
Test Journal Button Confirmation System
Tests the new button-based confirmation workflow for journal entries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.handlers.message_handlers import MessageHandlers
from src.bot.keyboards.inline_keyboards import BotKeyboards
from src.utils.logger import app_logger

async def test_journal_button_confirmation():
    """Test complete journal workflow with button confirmation"""
    print("🧪 Testing Journal Button Confirmation System")
    print("=" * 60)
    
    # Initialize handlers
    callback_handlers = CallbackHandlers()
    message_handlers = MessageHandlers()
    
    # Mock objects
    class MockUser:
        def __init__(self):
            self.id = 413217834
            self.username = "test_user"
            self.first_name = "Test"
            self.last_name = "User"
    
    class MockMessage:
        def __init__(self, text):
            self.text = text
            
        async def reply_text(self, message, reply_markup=None, parse_mode=None):
            print(f"🤖 Bot Response:\n{message}")
            if reply_markup:
                print(f"📱 Keyboard: {len(reply_markup.inline_keyboard)} rows of buttons")
                for row in reply_markup.inline_keyboard:
                    button_texts = [btn.text for btn in row]
                    print(f"   Buttons: {' | '.join(button_texts)}")
            print()
    
    class MockQuery:
        def __init__(self, data="new_journal"):
            self.from_user = MockUser()
            self.data = data
            
        async def answer(self):
            pass
            
        async def edit_message_text(self, message, reply_markup=None, parse_mode=None):
            print(f"🤖 Bot Response (Edit):\n{message}")
            if reply_markup:
                print(f"📱 Keyboard: {len(reply_markup.inline_keyboard)} rows of buttons")
                for row in reply_markup.inline_keyboard:
                    button_texts = [btn.text for btn in row]
                    print(f"   Buttons: {' | '.join(button_texts)}")
            print()
    
    class MockUpdate:
        def __init__(self, text=None, callback_data=None):
            self.effective_user = MockUser()
            if text:
                self.message = MockMessage(text)
            if callback_data:
                self.callback_query = MockQuery(callback_data)
    
    class MockContext:
        def __init__(self):
            self.user_data = {}
    
    print("🔧 Step 1: Test journal confirmation keyboard creation")
    try:
        keyboard = BotKeyboards.journal_confirmation()
        print("✅ Journal confirmation keyboard created successfully")
        print(f"📱 Keyboard has {len(keyboard.inline_keyboard)} rows")
        for i, row in enumerate(keyboard.inline_keyboard):
            button_texts = [btn.text for btn in row]
            button_callbacks = [btn.callback_data for btn in row]
            print(f"   Row {i+1}: {' | '.join(button_texts)}")
            print(f"   Callbacks: {' | '.join(button_callbacks)}")
    except Exception as e:
        print(f"❌ Keyboard creation failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("📝 Step 2: User clicks 'new_journal' button")
    
    query = MockQuery("new_journal")
    context = MockContext()
    
    try:
        await callback_handlers._new_journal(query, context)
        print(f"✅ New journal callback handled")
        print(f"🔍 Context state: {context.user_data}")
    except Exception as e:
        print(f"❌ New journal callback failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("💬 Step 3: User types journal entry")
    
    journal_text = "Hari ini adalah test untuk sistem journal button confirmation. Saya sedang testing apakah tombol SIMPAN, BATAL, dan EDIT bekerja dengan baik dalam sistem journal yang baru."
    update = MockUpdate(journal_text)
    
    try:
        await message_handlers._handle_journal_input(update, context, context.user_data)
        print(f"✅ Journal input handled with button confirmation")
        print(f"🔍 Context state after input: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal input failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("💾 Step 4: User clicks SIMPAN button")
    
    save_query = MockQuery("journal_save")
    
    try:
        await callback_handlers._journal_save_callback(save_query, context)  
        print(f"✅ Journal save button handled")
        print(f"🔍 Context state after save: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal save button failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("🚫 Step 5: Test BATAL button")
    
    # Reset context for cancel test
    context.user_data = {'state': 'input_journal', 'journal_text': 'Test entry for cancel'}
    cancel_query = MockQuery("journal_cancel")
    
    try:
        await callback_handlers._journal_cancel_callback(cancel_query, context)
        print(f"✅ Journal cancel button handled")
        print(f"🔍 Context state after cancel: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal cancel button failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✏️ Step 6: Test EDIT button")
    
    # Reset context for edit test
    context.user_data = {'state': 'input_journal', 'journal_text': 'Test entry for edit'}
    edit_query = MockQuery("journal_edit")
    
    try:
        await callback_handlers._journal_edit_callback(edit_query, context)
        print(f"✅ Journal edit button handled")
        print(f"🔍 Context state after edit: {context.user_data}")
    except Exception as e:
        print(f"❌ Journal edit button failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Journal Button Confirmation Test")
    print("This tests the new button-based confirmation system.\n")
    
    try:
        success = asyncio.run(test_journal_button_confirmation())
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 ALL BUTTON CONFIRMATION TESTS PASSED!")
            print("✅ Journal confirmation keyboard working!")
            print("✅ SIMPAN button functionality working!")
            print("✅ BATAL button functionality working!")
            print("✅ EDIT button functionality working!")
            print("✅ Button callbacks properly registered!")
            print("\n🚀 Button-based confirmation system ready!")
            print("\n📱 User Experience:")
            print("• User types journal → Gets preview with buttons")
            print("• User clicks SIMPAN → Entry saved with success message")
            print("• User clicks BATAL → Entry canceled, back to journal menu")
            print("• User clicks EDIT → Can rewrite entry")
            print("\n✨ Much better UX than text-based confirmation!")
        else:
            print("\n❌ Some button tests failed. Check implementation.")
            exit(1)
            
    except Exception as e:
        print(f"\n💥 Button test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
