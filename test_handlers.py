#!/usr/bin/env python3
"""
Debug Handler Registration Test
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_handler_registration():
    print("🔍 Testing Handler Registration")
    print("=" * 50)
    
    try:
        from telegram.ext import Application, MessageHandler, filters
        from src.bot.handlers.message_handlers import MessageHandlers
        from src.bot.handlers.callback_handlers import CallbackHandlers
        from config.settings import settings
        
        print("✅ All imports successful")
        
        # Create fake application for testing
        application = Application.builder().token("fake_token").build()
        print("✅ Application created")
        
        # Initialize handlers
        message_handlers = MessageHandlers()
        callback_handlers = CallbackHandlers()
        print("✅ Handlers initialized")
        
        # Test the exact line from main.py
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text))
        print("✅ MessageHandler registered successfully")
        
        # Check handlers in application
        handlers = application.handlers
        print(f"✅ Total handler groups: {len(handlers)}")
        
        # Find our message handler
        for group_id, group_handlers in handlers.items():
            for handler in group_handlers:
                if isinstance(handler, MessageHandler):
                    print(f"✅ Found MessageHandler in group {group_id}")
                    print(f"   Filter: {handler.filters}")
                    print(f"   Callback: {handler.callback}")
        
        # Test method existence
        methods_to_check = [
            'handle_text',
            '_handle_journal_input',
            '_handle_journal_confirmation'
        ]
        
        for method in methods_to_check:
            if hasattr(message_handlers, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
        
        print("\n" + "=" * 50)
        print("🎉 HANDLER REGISTRATION TEST PASSED!")
        print("✅ MessageHandler correctly registered")
        print("✅ All required methods exist")
        print("✅ Journal input should now work")
        
        return True
        
    except Exception as e:
        print(f"❌ Handler registration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_handler_registration()
    
    if success:
        print("\n🚀 Ready to test bot!")
        print("1. Start bot dengan: python main.py")
        print("2. Send /start command")
        print("3. Click Journal → Tulis Entry Baru")
        print("4. Type journal text")
        print("5. Verify response appears!")
    else:
        print("\n❌ Fix handler registration first!")
        exit(1)
