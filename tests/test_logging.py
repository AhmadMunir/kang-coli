#!/usr/bin/env python3
"""
Test Logging Configuration - Test terminal logging output
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import app_logger
import time

def test_logging_levels():
    """Test different logging levels"""
    print("🧪 Testing Logging Configuration")
    print("=" * 50)
    
    # Test different log levels
    app_logger.debug("🔍 DEBUG: This is a debug message for development")
    app_logger.info("ℹ️  INFO: Bot is starting up normally")
    app_logger.warning("⚠️  WARNING: This is a warning message")
    app_logger.error("❌ ERROR: This is an error message")
    
    # Test user interaction logs
    app_logger.info("👤 User 123456789 (@testuser) sent /start command")
    app_logger.info("💬 Text message from user 123456789: 'Hello bot!' (state: None)")
    app_logger.info("🔘 Callback 'check_streak' from user 123456789 (@testuser)")
    
    # Test service logs
    app_logger.info("📊 Streak service: User 123456789 current streak is 5 days")
    app_logger.info("📝 Journal service: New entry saved for user 123456789")
    app_logger.info("💾 Database: Successfully connected to SQLite database")
    
    # Test bot lifecycle logs
    app_logger.info("🚀 PMO Recovery Coach Bot - Starting Up")
    app_logger.info("✅ Settings validation passed")
    app_logger.info("🤖 Bot Username: pmo_recovery_bot")
    app_logger.info("🗄️ Database initialized successfully")
    app_logger.info("⏰ Daily broadcast scheduler started")
    app_logger.info("🔧 Setting up bot handlers...")
    app_logger.info("🎯 Bot is ready and starting to poll for messages...")
    app_logger.info("📱 Users can now interact with the bot!")
    app_logger.info("⌨️  Press Ctrl+C to stop the bot")
    
    print("\n" + "=" * 50)
    print("✅ Logging test completed!")
    print("💡 You should see colorized logs above in the terminal")
    print("📁 Check logs/ directory for file logs")

def test_continuous_logging():
    """Test continuous logging to simulate bot activity"""
    print("\n🔄 Testing Continuous Logging (simulating bot activity)")
    print("Press Ctrl+C to stop...")
    
    try:
        for i in range(10):
            app_logger.info(f"🔄 Heartbeat {i+1}: Bot is running normally")
            app_logger.debug(f"🔍 Debug info: Iteration {i+1} of continuous test")
            time.sleep(2)
    except KeyboardInterrupt:
        app_logger.info("🛑 Continuous logging test stopped by user")

if __name__ == "__main__":
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    print("🚀 Starting Logging Configuration Test")
    print("This will test terminal logging output dengan various levels")
    
    # Test basic logging levels
    test_logging_levels()
    
    # Ask user if they want continuous test
    print("\n❓ Do you want to test continuous logging? (simulates real bot activity)")
    response = input("Enter 'y' for yes, any other key to skip: ")
    
    if response.lower() == 'y':
        test_continuous_logging()
    
    print("\n🎉 Logging test completed!")
    print("💡 Your logging configuration is ready for bot usage!")
    print("📋 Log files are available in logs/ directory")
