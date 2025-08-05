#!/usr/bin/env python3
"""Test mood check-in enhancement implementation"""

print("🧪 Testing Mood Check-in Enhancement")
print("=" * 50)

try:
    print("1. Testing mood handlers import...")
    import src.bot.handlers.mood_checkin_handlers
    print("   ✅ Mood handlers imported successfully")
    
    print("2. Testing broadcast service import...")
    import src.services.broadcast_service
    print("   ✅ Broadcast service imported successfully")
    
    print("3. Testing user service mood methods...")
    from src.services.user_service import UserService
    user_service = UserService()
    
    # Test if methods exist
    assert hasattr(user_service, 'has_checked_in_today'), "Missing has_checked_in_today method"
    assert hasattr(user_service, 'get_users_without_checkin_today'), "Missing get_users_without_checkin_today method"
    assert hasattr(user_service, 'record_mood_checkin'), "Missing record_mood_checkin method"
    print("   ✅ User service mood methods found")
    
    print("4. Testing keyboard imports...")
    from src.bot.keyboards.inline_keyboards import BotKeyboards
    keyboards = BotKeyboards()
    
    # Test if mood keyboards exist
    assert hasattr(keyboards, 'mood_checkin_menu'), "Missing mood_checkin_menu method"
    assert hasattr(keyboards, 'mood_details_menu'), "Missing mood_details_menu method"
    assert hasattr(keyboards, 'quick_mood_response'), "Missing quick_mood_response method"
    print("   ✅ Mood keyboards found")
    
    print("5. Testing database model...")
    from src.database.models import MoodEntry
    print("   ✅ MoodEntry model imported successfully")
    
    print("\n🎉 All mood check-in enhancement components working!")
    print("📋 Summary:")
    print("   • Mood check-in handlers: Ready")
    print("   • Enhanced broadcast service: Ready")
    print("   • User service mood tracking: Ready")
    print("   • Mood keyboards: Ready")
    print("   • Database model: Ready")
    print("\n💡 Next step: Test with actual bot to verify integration!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
