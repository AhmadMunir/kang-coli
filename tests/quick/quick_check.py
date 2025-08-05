print("Testing Python execution...")

try:
    import telegram
    print(f"✅ Telegram version: {telegram.__version__}")
    
    import config.settings
    print("✅ Config loaded")
    
    from telegram.ext import Application
    print("✅ Application imported")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Bot is ready to run!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
