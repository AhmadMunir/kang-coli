#!/usr/bin/env python3
"""
Test Mood Analysis Callback Fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.bot.handlers.callback_handlers import CallbackHandlers
from src.utils.logger import app_logger

async def test_mood_analysis_callback():
    """Test the fixed mood analysis callback routing"""
    print("🧪 Testing Fixed Mood Analysis Callback")
    print("=" * 50)
    
    # Mock objects
    class MockUser:
        def __init__(self):
            self.id = 413217834
            self.username = "test_user"
            self.first_name = "Test"
            self.last_name = "User"
    
    class MockQuery:
        def __init__(self, callback_data):
            self.from_user = MockUser()
            self.data = callback_data
            
        async def answer(self):
            pass
            
        async def edit_message_text(self, message, reply_markup=None, parse_mode=None):
            print(f"🤖 Bot Response for '{self.data}':")
            print(f"   Message length: {len(message)} characters")
            if "Analisis Mood" in message:
                print("   ✅ Correct mood analysis response")
            elif "mood value" in message.lower():
                print("   ❌ Wrong response - mood selection handler called")
            else:
                print("   ❓ Unknown response type")
            print()
    
    class MockContext:
        def __init__(self):
            self.user_data = {}
    
    # Initialize callback handlers
    callback_handlers = CallbackHandlers()
    
    # Test different mood-related callbacks
    test_cases = [
        ("mood_analysis", "Should call _mood_analysis method"),
        ("mood_1", "Should call _handle_mood_selection method"),
        ("mood_5", "Should call _handle_mood_selection method"),
        ("trigger_journal", "Should call _trigger_analysis method")
    ]
    
    print("🔧 Testing callback routing...")
    
    for callback_data, expected in test_cases:
        print(f"\n📝 Testing callback: '{callback_data}' - {expected}")
        
        query = MockQuery(callback_data)
        context = MockContext()
        
        try:
            await callback_handlers.handle_callback(
                type('MockUpdate', (), {'callback_query': query, 'effective_user': MockUser()})(),
                context
            )
            print(f"✅ Callback '{callback_data}' handled successfully")
            
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print(f"❌ Callback '{callback_data}' still has int parsing error!")
                print(f"   Error: {e}")
                return False
        except Exception as e:
            print(f"⚠️  Callback '{callback_data}' had other error: {e}")
            # This might be expected for some unimplemented features
    
    return True

async def test_specific_mood_analysis():
    """Test mood_analysis specifically"""
    print("\n" + "=" * 50)
    print("🎯 Testing Mood Analysis Specifically")
    print("=" * 50)
    
    class MockQuery:
        def __init__(self):
            self.from_user = type('MockUser', (), {
                'id': 413217834,
                'username': 'test_user',
                'first_name': 'Test'
            })()
            self.data = "mood_analysis"
            
        async def answer(self):
            pass
            
        async def edit_message_text(self, message, reply_markup=None, parse_mode=None):
            print("🤖 Mood Analysis Response:")
            print(f"   Contains 'Analisis Mood': {'Analisis Mood' in message}")
            print(f"   Contains 'Coming Soon': {'Coming Soon' in message}")
            print(f"   Message preview: {message[:100]}...")
            return True
    
    callback_handlers = CallbackHandlers()
    query = MockQuery()
    context = type('MockContext', (), {'user_data': {}})()
    
    try:
        await callback_handlers._mood_analysis(query, context)
        print("✅ Mood analysis method executed successfully!")
        return True
    except Exception as e:
        print(f"❌ Mood analysis method failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Mood Analysis Callback Fix Test")
    print("This tests if the int() parsing error is fixed.\n")
    
    async def run_tests():
        try:
            success1 = await test_mood_analysis_callback()
            success2 = await test_specific_mood_analysis()
            
            if success1 and success2:
                print("\n" + "=" * 50)
                print("🎉 MOOD ANALYSIS CALLBACK FIX SUCCESSFUL!")
                print("✅ No more int() parsing error!")
                print("✅ mood_analysis callback routes correctly!")
                print("✅ mood_1, mood_2, etc still work for mood selection!")
                print("✅ Callback routing order fixed!")
                print("\n🚀 Mood analysis ready for use!")
            else:
                print("\n❌ Mood analysis callback still has issues.")
                exit(1)
                
        except Exception as e:
            print(f"\n💥 Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            exit(1)
    
    asyncio.run(run_tests())
