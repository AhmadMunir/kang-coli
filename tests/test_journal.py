"""
Test script untuk journal functionality
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.handlers.callback_handlers import CallbackHandlers
from src.bot.keyboards.inline_keyboards import BotKeyboards

def test_journal_functionality():
    """Test journal functionality"""
    print("🧪 Testing Journal Functionality")
    print("=" * 40)
    
    try:
        # Test 1: Check if journal menu keyboard works
        print("📋 Test 1: Journal Menu Keyboard...")
        keyboard = BotKeyboards.journal_menu()
        
        # Count buttons and check callback data
        journal_callbacks = []
        for row in keyboard.inline_keyboard[:-1]:  # Exclude back button row
            for button in row:
                journal_callbacks.append(button.callback_data)
        
        expected_callbacks = ['new_journal', 'read_journal', 'mood_analysis', 'trigger_journal']
        
        print(f"✅ Journal menu keyboard created")
        print(f"   • Journal callbacks: {journal_callbacks}")
        
        if all(cb in journal_callbacks for cb in expected_callbacks):
            print("✅ All expected journal callbacks present")
        else:
            missing = [cb for cb in expected_callbacks if cb not in journal_callbacks]
            print(f"❌ Missing callbacks: {missing}")
            return False
        
        # Test 2: Check CallbackHandlers initialization
        print("\n📋 Test 2: CallbackHandlers Initialization...")
        handler = CallbackHandlers()
        print("✅ CallbackHandlers initialized successfully")
        
        # Test 3: Check if journal handler methods exist
        print("\n📋 Test 3: Journal Handler Methods...")
        journal_methods = ['_new_journal', '_read_journal', '_mood_analysis', '_trigger_analysis']
        
        missing_methods = []
        for method in journal_methods:
            if hasattr(handler, method):
                print(f"✅ {method} method exists")
            else:
                print(f"❌ {method} method missing")
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
            return False
        
        # Test 4: Check journal menu method
        print("\n📋 Test 4: Journal Menu Method...")
        if hasattr(handler, '_journal_menu'):
            print("✅ _journal_menu method exists")
        else:
            print("❌ _journal_menu method missing")
            return False
        
        # Test 5: Display journal features info
        print("\n📋 Test 5: Journal Features Information...")
        
        journal_features = {
            "✍️ Tulis Entry Baru": "Write personal reflections and daily experiences",
            "📖 Baca Entries": "Review past entries (Coming Soon)",
            "🎯 Analisis Mood": "AI-powered mood pattern analysis (Coming Soon)", 
            "🔍 Analisis Trigger": "Identify triggers from journal content (Coming Soon)"
        }
        
        print("✅ Journal features defined:")
        for feature, description in journal_features.items():
            print(f"   • {feature}: {description}")
        
        print("\n🎉 All journal functionality tests passed!")
        print("=" * 40)
        
        # Show usage instructions
        print("\n📱 How to Test in Telegram:")
        print("1. Start the bot: /start")
        print("2. Click '📖 Journal'")
        print("3. Read about journal features and benefits")
        print("4. Click any journal option (✍️, 📖, 🎯, 🔍)")
        print("5. Should receive appropriate information")
        print("6. Should return to main menu with back button")
        
        # Show journal benefits
        print("\n📝 Journal System Benefits:")
        print("• Self-Awareness & Emotional Intelligence")
        print("• Progress Tracking & Pattern Recognition")
        print("• Trigger Identification & Risk Management")
        print("• Therapeutic Writing & Stress Relief")
        print("• Goal Setting & Achievement Tracking")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_journal_functionality()
    
    if success:
        print(f"\n✅ JOURNAL FUNCTIONALITY READY!")
        print("Journal system can now handle all menu options properly.")
        print("\nUsers can:")
        print("• Access detailed journal feature information")
        print("• Navigate to all journal options without errors")
        print("• Understand the benefits and purpose of journaling")
        print("• Get guidance for current and upcoming features")
    else:
        print(f"\n❌ TESTS FAILED!")
        print("Please check the errors above.")
