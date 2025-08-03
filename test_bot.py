#!/usr/bin/env python3
"""
Test script untuk PMO Recovery Bot
"""

def test_imports():
    """Test if all modules can be imported"""
    try:
        from config.settings import settings
        print("✅ Settings module imported")
        
        from src.database.models import User, JournalEntry, RelapseRecord, CheckIn
        print("✅ Database models imported")
        
        from src.services import UserService, StreakService, MotivationalService, EmergencyService
        print("✅ Services imported")
        
        from src.bot.handlers import CommandHandlers, CallbackHandlers
        print("✅ Bot handlers imported")
        
        from src.bot.keyboards import BotKeyboards
        print("✅ Bot keyboards imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database operations"""
    try:
        from src.database.database import db
        
        # Create tables
        db.create_tables()
        print("✅ Database tables created")
        
        # Test user service
        from src.services import UserService
        user = UserService.get_or_create_user(
            telegram_id=123456,
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        print(f"✅ Test user created: {user}")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_services():
    """Test service functionality"""
    try:
        from src.services import MotivationalService, EmergencyService
        
        # Test motivational service
        motivational = MotivationalService()
        quote = motivational.get_daily_quote()
        print(f"✅ Daily quote: {quote['text'][:50]}...")
        
        tip = motivational.get_coping_tip()
        print(f"✅ Coping tip: {tip['title']}")
        
        # Test emergency service
        emergency = EmergencyService()
        intervention = emergency.get_emergency_intervention()
        print(f"✅ Emergency intervention: {intervention['alert_message'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Services error: {e}")
        return False

def test_bot_token():
    """Test bot token validity (without starting bot)"""
    try:
        from config.settings import settings
        
        if not settings.BOT_TOKEN:
            print("❌ BOT_TOKEN not set")
            return False
        
        if len(settings.BOT_TOKEN) < 40:
            print("❌ BOT_TOKEN seems invalid (too short)")
            return False
        
        print("✅ BOT_TOKEN appears valid")
        return True
    except Exception as e:
        print(f"❌ Token test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 PMO Recovery Bot - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Test", test_database),
        ("Services Test", test_services),
        ("Bot Token Test", test_bot_token)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("Run: python main.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
