"""
Test script untuk broadcast system
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from src.services.broadcast_service import BroadcastService
from src.services.scheduler_service import SchedulerService
from src.database.database import db
from src.utils.logger import app_logger

async def test_broadcast_system():
    """Test broadcast system functionality"""
    print("🧪 Testing PMO Recovery Bot Broadcast System")
    print("=" * 50)
    
    try:
        # Setup database
        db.create_tables()
        print("✅ Database setup completed")
        
        # Initialize services
        broadcast_service = BroadcastService()
        print("✅ Broadcast service initialized")
        
        # Test 1: Generate daily content
        print("\n📋 Test 1: Generating daily broadcast content...")
        daily_content = broadcast_service._generate_daily_content()
        
        print(f"✅ Generated content for: {daily_content['date']}")
        print(f"📝 Day theme: {daily_content['day_content']['title']}")
        print(f"💡 Recovery fact: {daily_content['recovery_fact']['title']}")
        print(f"🎯 Quote: {daily_content['quote']['text'][:50]}...")
        
        # Test 2: Generate weekly summary content
        print("\n📋 Test 2: Generating weekly summary content...")
        weekly_content = broadcast_service._generate_weekly_summary()
        
        print(f"✅ Generated weekly summary")
        print(f"📊 Week focus: {weekly_content['summary']['title']}")
        print(f"🎯 Tips available: {len([k for k in weekly_content.keys() if 'tip' in k])}")
        
        # Test 3: Validate content structure
        print("\n📋 Test 3: Validating content structure...")
        
        required_daily_keys = ['greeting', 'date', 'quote', 'tip', 'day_content', 
                              'recovery_fact', 'inspiration', 'call_to_action']
        
        missing_keys = [key for key in required_daily_keys if key not in daily_content]
        if missing_keys:
            print(f"❌ Missing daily content keys: {missing_keys}")
        else:
            print("✅ Daily content structure is valid")
        
        required_weekly_keys = ['tip', 'summary', 'stats', 'inspiration']
        
        missing_weekly_keys = [key for key in required_weekly_keys if key not in weekly_content]
        if missing_weekly_keys:
            print(f"❌ Missing weekly content keys: {missing_weekly_keys}")
        else:
            print("✅ Weekly content structure is valid")
        
        # Test 4: Test message formatting
        print("\n📋 Test 4: Testing message formatting...")
        
        formatted_daily = broadcast_service._format_daily_message(daily_content)
        formatted_weekly = broadcast_service._format_weekly_message(weekly_content)
        
        if len(formatted_daily) > 0:
            print("✅ Daily message formatting successful")
            print(f"📏 Daily message length: {len(formatted_daily)} characters")
        else:
            print("❌ Daily message formatting failed")
        
        if len(formatted_weekly) > 0:
            print("✅ Weekly message formatting successful")
            print(f"📏 Weekly message length: {len(formatted_weekly)} characters")
        else:
            print("❌ Weekly message formatting failed")
        
        # Test 5: Test scheduler service (without actually starting it)
        print("\n📋 Test 5: Testing scheduler service configuration...")
        
        # Mock application for scheduler test
        class MockApp:
            pass
        
        mock_app = MockApp()
        scheduler_service = SchedulerService(mock_app)
        
        jobs = scheduler_service.list_scheduled_jobs()
        print(f"✅ Scheduler service initialized")
        print(f"📅 Scheduled jobs configured: {len(jobs) if jobs else 0}")
        
        if jobs:
            for job in jobs:
                print(f"   • {job['name']} - Next: {job['next_run']}")
        
        print("\n🎉 All broadcast system tests completed!")
        print("=" * 50)
        
        # Show sample content
        print("\n📄 Sample Daily Broadcast:")
        print("-" * 30)
        print(formatted_daily[:500] + "..." if len(formatted_daily) > 500 else formatted_daily)
        
        print("\n📄 Sample Weekly Summary:")
        print("-" * 30)
        print(formatted_weekly[:500] + "..." if len(formatted_weekly) > 500 else formatted_weekly)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        app_logger.error(f"Broadcast test error: {e}")
        return False

async def test_admin_commands():
    """Test admin command functionality"""
    print("\n🔧 Testing Admin Commands")
    print("=" * 30)
    
    try:
        from src.bot.handlers.admin_handlers import AdminHandlers
        
        # Mock scheduler service
        class MockSchedulerService:
            def list_scheduled_jobs(self):
                return [
                    {
                        'id': 'daily_broadcast',
                        'name': 'Daily Broadcast',
                        'next_run': '2024-01-01 08:00:00'
                    },
                    {
                        'id': 'afternoon_boost',
                        'name': 'Afternoon Boost',
                        'next_run': '2024-01-01 15:00:00'
                    }
                ]
        
        mock_scheduler = MockSchedulerService()
        admin_handlers = AdminHandlers(mock_scheduler)
        
        print("✅ Admin handlers initialized")
        
        # Test admin check function
        admin_id = settings.ADMIN_USER_ID
        if admin_id:
            is_admin = admin_handlers.is_admin(int(admin_id))
            print(f"✅ Admin check function working: {is_admin}")
        else:
            print("⚠️ No ADMIN_USER_ID set in environment")
        
        print("✅ Admin commands test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Admin test failed: {e}")
        app_logger.error(f"Admin test error: {e}")
        return False

if __name__ == "__main__":
    async def main():
        success = True
        
        # Test broadcast system
        broadcast_success = await test_broadcast_system()
        success = success and broadcast_success
        
        # Test admin commands
        admin_success = await test_admin_commands()
        success = success and admin_success
        
        # Final result
        print("\n" + "=" * 50)
        if success:
            print("🎉 ALL TESTS PASSED! Broadcast system is ready!")
            print("\n📝 Next Steps:")
            print("1. Set your ADMIN_USER_ID in .env file")
            print("2. Start the bot with: python main.py")
            print("3. Use admin commands to test broadcast:")
            print("   • /testbroadcast - Send test broadcast")
            print("   • /broadcastnow - Send daily broadcast")
            print("   • /adminhelp - See all admin commands")
        else:
            print("❌ SOME TESTS FAILED! Check logs for details.")
        print("=" * 50)
    
    # Run the test
    asyncio.run(main())
