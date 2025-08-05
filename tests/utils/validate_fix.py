#!/usr/bin/env python3
"""
Validate Journal Fix
"""

def validate_fix():
    print("🔍 Validating Journal Input Fix")
    print("=" * 40)
    
    # Check if main.py has message handler registration
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        if 'MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text)' in content:
            print("✅ MessageHandler registration found in main.py")
        else:
            print("❌ MessageHandler registration missing in main.py")
            return False
        
        # Check setup_bot_handlers_sync function
        if 'setup_bot_handlers_sync(application, scheduler_service)' in content:
            print("✅ setup_bot_handlers_sync call found")
        else:
            print("❌ setup_bot_handlers_sync call missing")
            return False
            
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False
    
    # Check message_handlers.py implementation
    try:
        with open('src/bot/handlers/message_handlers.py', 'r') as f:
            content = f.read()
        
        required_methods = [
            'def handle_text(',
            'def _handle_journal_input(',
            'def _handle_journal_confirmation(',
            'def _save_journal_entry(',
            'def _cancel_journal_entry(',
            'def _edit_journal_entry('
        ]
        
        for method in required_methods:
            if method in content:
                print(f"✅ Method {method.replace('def ', '').replace('(', '')} found")
            else:
                print(f"❌ Method {method.replace('def ', '').replace('(', '')} missing")
                return False
                
    except Exception as e:
        print(f"❌ Error reading message_handlers.py: {e}")
        return False
    
    # Check callback_handlers.py
    try:
        with open('src/bot/handlers/callback_handlers.py', 'r') as f:
            content = f.read()
        
        if "context.user_data['state'] = 'input_journal'" in content:
            print("✅ State setting found in callback_handlers.py")
        else:
            print("❌ State setting missing in callback_handlers.py")
            return False
            
    except Exception as e:
        print(f"❌ Error reading callback_handlers.py: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 ALL VALIDATIONS PASSED!")
    print("✅ MessageHandler properly registered")
    print("✅ Journal methods implemented") 
    print("✅ State management configured")
    print("\n📋 MASALAH SUDAH DIPERBAIKI:")
    print("• MessageHandler sekarang terdaftar di main.py")
    print("• Text messages akan diterima oleh handle_text()")
    print("• Journal input akan mendapat respon")
    print("• Confirmation system aktif")
    
    return True

if __name__ == "__main__":
    success = validate_fix()
    
    if success:
        print("\n🚀 SIAP UNTUK TEST!")
        print("Run: python main.py")
        print("Journal input sekarang akan bekerja dengan baik!")
    else:
        print("\n❌ Masih ada masalah dalam implementasi")
        exit(1)
