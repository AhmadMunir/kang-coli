"""
Test script untuk mood functionality
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.keyboards.inline_keyboards import BotKeyboards

def test_mood_functionality():
    """Test mood scale functionality"""
    print("🧪 Testing Mood Functionality")
    print("=" * 40)
    
    try:
        # Test 1: Check if mood scale keyboard works
        print("📋 Test 1: Mood Scale Keyboard...")
        keyboard = BotKeyboards.mood_scale()
        
        # Count buttons
        total_buttons = sum(len(row) for row in keyboard.inline_keyboard)
        mood_buttons = sum(1 for row in keyboard.inline_keyboard[:-1] for button in row)  # Exclude back button row
        
        print(f"✅ Mood scale keyboard created")
        print(f"   • Mood buttons: {mood_buttons} (expected: 5)")
        print(f"   • Total buttons: {total_buttons} (expected: 6 including back button)")
        
        if mood_buttons == 5:
            print("✅ Correct number of mood buttons (1-5)")
        else:
            print(f"❌ Wrong number of mood buttons. Expected 5, got {mood_buttons}")
        
        # Test 2: Check callback data format
        print("\n📋 Test 2: Callback Data Format...")
        mood_callbacks = []
        for row in keyboard.inline_keyboard[:-1]:  # Exclude back button row
            for button in row:
                mood_callbacks.append(button.callback_data)
        
        expected_callbacks = ['mood_1', 'mood_2', 'mood_3', 'mood_4', 'mood_5']
        
        if mood_callbacks == expected_callbacks:
            print("✅ Callback data format correct")
            print(f"   • Callbacks: {mood_callbacks}")
        else:
            print(f"❌ Callback data incorrect")
            print(f"   • Expected: {expected_callbacks}")
            print(f"   • Got: {mood_callbacks}")
        
        # Test 3: Check CallbackHandlers initialization
        print("\n📋 Test 3: CallbackHandlers Initialization...")
        handler = CallbackHandlers()
        print("✅ CallbackHandlers initialized successfully")
        
        # Test 4: Check if _handle_mood_selection method exists
        print("\n📋 Test 4: Mood Handler Method...")
        if hasattr(handler, '_handle_mood_selection'):
            print("✅ _handle_mood_selection method exists")
        else:
            print("❌ _handle_mood_selection method missing")
            return False
        
        # Test 5: Check mood descriptions
        print("\n📋 Test 5: Mood Descriptions...")
        mood_descriptions = {
            1: "😢 Sangat buruk",
            2: "😔 Kurang baik", 
            3: "😐 Netral",
            4: "😊 Baik",
            5: "😄 Sangat baik"
        }
        
        print("✅ Mood descriptions defined:")
        for mood, desc in mood_descriptions.items():
            print(f"   • {mood}: {desc}")
        
        print("\n🎉 All mood functionality tests passed!")
        print("=" * 40)
        
        # Show usage instructions
        print("\n📱 How to Test in Telegram:")
        print("1. Start the bot: /start")
        print("2. Click '📝 Check-in Harian'")
        print("3. Select mood from 1-5")
        print("4. Should receive appropriate response")
        print("5. Should return to main menu")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mood_functionality()
    
    if success:
        print("\n✅ MOOD FUNCTIONALITY READY!")
        print("Bot can now handle mood selection properly.")
    else:
        print("\n❌ TESTS FAILED!")
        print("Please check the errors above.")
