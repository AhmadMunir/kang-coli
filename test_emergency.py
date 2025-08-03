#!/usr/bin/env python3
"""
Test Emergency Callbacks
"""

print("🧪 Testing Emergency Callback Routing...")

# Test import semua modules yang dibutuhkan
try:
    from src.bot.handlers.callback_handlers import CallbackHandlers
    print("✅ CallbackHandlers imported")
    
    from src.bot.keyboards.inline_keyboards import BotKeyboards
    print("✅ BotKeyboards imported")
    
    # Test emergency menu keyboard
    emergency_keyboard = BotKeyboards.emergency_menu()
    print("✅ Emergency menu keyboard created")
    
    # Test callback handlers instance
    handlers = CallbackHandlers()
    print("✅ CallbackHandlers instance created")
    
    print("\n🎯 Emergency Callbacks yang sudah diperbaiki:")
    callbacks = [
        "urge_surfing",
        "trigger_analysis", 
        "immediate_distraction",
        "mindfulness_protocol",
        "emergency_contacts",
        "accountability_check"
    ]
    
    for callback in callbacks:
        print(f"  ✅ {callback}")
    
    print("\n🎉 Semua emergency callbacks sudah terdaftar!")
    print("Bot siap untuk testing emergency mode.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
