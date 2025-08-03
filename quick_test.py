#!/usr/bin/env python3
"""
Quick Test - Check Enhanced Journal Methods Exist
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    print("🧪 Quick Implementation Check")
    print("=" * 50)
    
    try:
        # Test message handlers import
        from src.bot.handlers.message_handlers import MessageHandlers
        print("✅ MessageHandlers imported")
        
        # Create instance
        handler = MessageHandlers()
        print("✅ MessageHandlers instance created")
        
        # Check required methods exist
        required_methods = [
            '_handle_journal_input',
            '_handle_journal_confirmation',
            '_save_journal_entry',
            '_cancel_journal_entry',
            '_edit_journal_entry'
        ]
        
        for method in required_methods:
            if hasattr(handler, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        # Test callback handlers import
        from src.bot.handlers.callback_handlers import CallbackHandlers
        print("✅ CallbackHandlers imported")
        
        # Create instance
        callback_handler = CallbackHandlers()
        print("✅ CallbackHandlers instance created")
        
        print("\n" + "=" * 50)
        print("🎉 IMPLEMENTATION CHECK PASSED!")
        print("✅ All enhanced journal methods are present")
        print("✅ Handlers can be instantiated")
        print("\n📋 Enhanced Journal Flow:")
        print("1. User clicks 'new_journal' button")
        print("2. Bot sets state: input_journal, waiting_for_text")
        print("3. User types journal entry")
        print("4. Bot shows confirmation with preview")
        print("5. User chooses SIMPAN/BATAL/EDIT")
        print("6. Bot processes choice accordingly")
        print("\n🚀 Ready for production testing!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
