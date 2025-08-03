#!/usr/bin/env python3
"""
Quick Setup Script for PMO Recovery Bot Backup System
Initializes backup system and runs basic tests
"""

import os
import sys
import asyncio
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_directories():
    """Create necessary directories"""
    print("📁 Creating backup directories...")
    
    directories = [
        "backups",
        "backups/daily", 
        "backups/weekly",
        "backups/manual",
        "backups/emergency",
        "recovery",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")

def check_requirements():
    """Check if required packages are installed"""
    print("📦 Checking requirements...")
    
    required_packages = [
        'telegram',
        'schedule', 
        'sqlite3',
        'zipfile',
        'json'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'telegram':
                import telegram
            elif package == 'schedule':
                import schedule
            elif package == 'sqlite3':
                import sqlite3
            elif package == 'zipfile':
                import zipfile
            elif package == 'json':
                import json
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def create_sample_config():
    """Create sample configuration"""
    print("⚙️ Creating sample configuration...")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Create sample admin config
    admin_config = {
        "admin_user_ids": [
            "# Add your Telegram user IDs here",
            "# Example: 123456789"
        ],
        "backup_settings": {
            "daily_backup_time": "03:00",
            "weekly_backup_day": "sunday",
            "weekly_backup_time": "02:00",
            "retention_policy": {
                "daily": 7,
                "weekly": 4, 
                "manual": 10,
                "emergency": 3
            }
        }
    }
    
    config_file = config_dir / "backup_config.json"
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(admin_config, f, indent=2)
        print(f"  ✅ Created {config_file}")
        print("  ⚠️  Remember to add your Telegram user ID to backup_handlers.py")
    else:
        print(f"  ✅ Configuration already exists: {config_file}")

async def test_basic_functionality():
    """Test basic backup functionality"""
    print("🧪 Testing basic functionality...")
    
    try:
        from src.services.backup_service import backup_service
        from src.utils.recovery_tool import recovery_tool
        
        # Test backup service initialization
        status = await backup_service.get_backup_status()
        print(f"  ✅ Backup service initialized")
        print(f"  📊 Database exists: {status['database_exists']}")
        
        # Test recovery tool
        if status['database_exists']:
            diagnosis = await recovery_tool.diagnose_database_issues()
            print(f"  ✅ Recovery tool working")
            print(f"  🔍 Database integrity: {diagnosis['integrity_check']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing functionality: {e}")
        return False

def display_next_steps():
    """Display next steps for user"""
    print("\n" + "=" * 50)
    print("🎉 BACKUP SYSTEM SETUP COMPLETE!")
    print("=" * 50)
    
    print("\n📋 NEXT STEPS:")
    print()
    print("1. 👤 Configure Admin Access:")
    print("   Edit: src/bot/handlers/backup_handlers.py")
    print("   Add your Telegram user ID to ADMIN_USER_IDS")
    print()
    print("2. 🚀 Start the Bot:")
    print("   python main.py")
    print("   or")
    print("   python run_bot.py")
    print()
    print("3. 📱 Use Telegram Commands (Admin only):")
    print("   /backup - Open backup management menu")
    print()
    print("4. 💻 Use Command Line Tools:")
    print("   python backup_manager.py --help")
    print("   or")
    print("   backup_manager.bat (Windows)")
    print()
    print("5. 🧪 Run Tests:")
    print("   python tests/test_backup_system.py")
    print()
    print("6. 📖 Read Documentation:")
    print("   docs/BACKUP_SYSTEM_GUIDE.md")
    print()
    
    print("🔄 AUTOMATIC FEATURES:")
    print("• Daily backups at 3:00 AM")
    print("• Weekly backups on Sunday at 2:00 AM") 
    print("• Automatic cleanup of old backups")
    print("• Database integrity monitoring")
    print()
    
    print("⚠️  IMPORTANT REMINDERS:")
    print("• Test restore process regularly")
    print("• Monitor backup logs")
    print("• Keep backups in multiple locations")
    print("• Update admin user IDs in backup_handlers.py")

async def main():
    """Main setup function"""
    print("🔧 PMO Recovery Bot - Backup System Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup failed. Please install missing requirements.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create sample configuration
    create_sample_config()
    
    # Test basic functionality
    test_success = await test_basic_functionality()
    
    if test_success:
        display_next_steps()
        print("\n✅ Setup completed successfully!")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("Some functionality may not work until the main bot is running.")
        display_next_steps()

if __name__ == "__main__":
    asyncio.run(main())
