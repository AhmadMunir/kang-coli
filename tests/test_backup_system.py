#!/usr/bin/env python3
"""
Test Suite for Backup and Restore System
Comprehensive tests for data backup and recovery functionality
"""

import os
import sys
import asyncio
import tempfile
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
import json
import zipfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.backup_service import backup_service
from src.services.backup_scheduler import backup_scheduler
from src.utils.recovery_tool import recovery_tool

class BackupSystemTest:
    """Test suite for backup and restore system"""
    
    def __init__(self):
        self.test_db_path = "data/test_pmo_recovery.db"
        self.original_db_path = backup_service.db_path
        self.test_backup_dir = Path("test_backups")
        self.original_backup_dir = backup_service.backup_dir
        
    async def setup_test_environment(self):
        """Setup test environment"""
        print("🔧 Setting up test environment...")
        
        # Create test directories
        self.test_backup_dir.mkdir(exist_ok=True)
        for backup_type in ["daily", "weekly", "manual", "emergency"]:
            (self.test_backup_dir / backup_type).mkdir(exist_ok=True)
        
        # Update backup service paths
        backup_service.db_path = self.test_db_path
        backup_service.backup_dir = self.test_backup_dir
        recovery_tool.db_path = self.test_db_path
        
        # Create test database
        await self.create_test_database()
        
        print("✅ Test environment setup complete")
    
    async def create_test_database(self):
        """Create a test database with sample data"""
        print("📊 Creating test database...")
        
        os.makedirs(os.path.dirname(self.test_db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                timezone TEXT DEFAULT 'Asia/Jakarta',
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT NOT NULL,
                mood_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_relapse_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Insert test data
        test_users = [
            (1001, 'testuser1', 'Test', 'User1', '2025-01-01 10:00:00'),
            (1002, 'testuser2', 'Test', 'User2', '2025-01-02 11:00:00'),
            (1003, 'testuser3', 'Test', 'User3', '2025-01-03 12:00:00'),
        ]
        
        cursor.executemany(
            'INSERT INTO users (user_id, username, first_name, last_name, join_date) VALUES (?, ?, ?, ?, ?)',
            test_users
        )
        
        test_journal_entries = [
            (1001, 'Feeling good today, stayed strong!', 8, '2025-08-01 10:00:00'),
            (1001, 'Had some urges but managed to resist', 6, '2025-08-02 15:30:00'),
            (1002, 'Great day, feeling motivated!', 9, '2025-08-01 12:00:00'),
            (1002, 'Struggling a bit but pushing through', 5, '2025-08-03 09:00:00'),
            (1003, 'New start, feeling hopeful', 7, '2025-08-01 14:00:00'),
        ]
        
        cursor.executemany(
            'INSERT INTO journal_entries (user_id, content, mood_score, created_at) VALUES (?, ?, ?, ?)',
            test_journal_entries
        )
        
        test_streaks = [
            (1001, 15, 23, '2025-07-15'),
            (1002, 8, 12, '2025-07-20'),
            (1003, 3, 3, None),
        ]
        
        cursor.executemany(
            'INSERT INTO streaks (user_id, current_streak, longest_streak, last_relapse_date) VALUES (?, ?, ?, ?)',
            test_streaks
        )
        
        conn.commit()
        conn.close()
        
        print("✅ Test database created with sample data")
    
    async def cleanup_test_environment(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up test environment...")
        
        # Restore original paths
        backup_service.db_path = self.original_db_path
        backup_service.backup_dir = self.original_backup_dir
        recovery_tool.db_path = self.original_db_path
        
        # Remove test files
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        if self.test_backup_dir.exists():
            shutil.rmtree(self.test_backup_dir)
        
        print("✅ Test environment cleaned up")
    
    async def test_backup_creation(self):
        """Test backup creation functionality"""
        print("\n🧪 Testing backup creation...")
        
        # Test manual backup
        success, result = await backup_service.create_full_backup("manual")
        
        if success:
            print(f"✅ Manual backup created: {result}")
            
            # Verify backup file exists
            backup_path = Path(result)
            if backup_path.exists():
                print(f"✅ Backup file exists: {backup_path.name}")
                print(f"📊 File size: {backup_path.stat().st_size / 1024:.1f} KB")
                
                # Verify backup contents
                await self.verify_backup_contents(str(backup_path))
            else:
                print(f"❌ Backup file not found: {backup_path}")
                return False
        else:
            print(f"❌ Backup creation failed: {result}")
            return False
        
        return True
    
    async def verify_backup_contents(self, backup_path: str):
        """Verify backup file contents"""
        print("🔍 Verifying backup contents...")
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                file_list = zipf.namelist()
                
                # Check required files
                required_files = [
                    'backup_metadata.json',
                    'database/pmo_recovery.db',
                    'database/pmo_recovery_export.sql',
                    'database/user_data_export.json'
                ]
                
                missing_files = []
                for required_file in required_files:
                    if required_file not in file_list:
                        missing_files.append(required_file)
                
                if missing_files:
                    print(f"❌ Missing files in backup: {missing_files}")
                    return False
                
                # Verify metadata
                with zipf.open('backup_metadata.json') as f:
                    metadata = json.load(f)
                    print(f"✅ Metadata: {metadata['user_count']} users, {metadata['journal_entries_count']} entries")
                
                print("✅ Backup contents verified successfully")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying backup: {e}")
            return False
    
    async def test_database_diagnosis(self):
        """Test database diagnosis functionality"""
        print("\n🧪 Testing database diagnosis...")
        
        diagnosis = await recovery_tool.diagnose_database_issues()
        
        print(f"✅ Database exists: {diagnosis['database_exists']}")
        print(f"✅ Database accessible: {diagnosis['database_accessible']}")
        print(f"✅ Integrity check: {diagnosis['integrity_check']}")
        
        if diagnosis['table_structure']:
            print(f"✅ Tables found: {list(diagnosis['table_structure'].keys())}")
        
        if diagnosis['data_consistency']:
            print(f"✅ Data consistency: {diagnosis['data_consistency']}")
        
        if diagnosis['corruption_indicators']:
            print(f"⚠️  Issues detected: {diagnosis['corruption_indicators']}")
        
        return diagnosis['database_exists'] and diagnosis['database_accessible']
    
    async def test_restore_functionality(self):
        """Test restore functionality"""
        print("\n🧪 Testing restore functionality...")
        
        # First create a backup
        success, backup_path = await backup_service.create_full_backup("manual")
        if not success:
            print(f"❌ Failed to create backup for restore test: {backup_path}")
            return False
        
        # Modify database to simulate data loss
        await self.simulate_data_modification()
        
        # Restore from backup
        success, result = await backup_service.restore_from_backup(backup_path, confirm_restore=True)
        
        if success:
            print(f"✅ Restore completed: {result}")
            
            # Verify restored data
            return await self.verify_restored_data()
        else:
            print(f"❌ Restore failed: {result}")
            return False
    
    async def simulate_data_modification(self):
        """Simulate data modification/loss"""
        print("🔄 Simulating data modification...")
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Delete some data
        cursor.execute("DELETE FROM journal_entries WHERE user_id = 1001")
        cursor.execute("UPDATE users SET first_name = 'Modified' WHERE user_id = 1002")
        
        conn.commit()
        conn.close()
        
        print("✅ Data modification simulated")
    
    async def verify_restored_data(self):
        """Verify data after restore"""
        print("🔍 Verifying restored data...")
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Check if deleted data is restored
        cursor.execute("SELECT COUNT(*) FROM journal_entries WHERE user_id = 1001")
        journal_count = cursor.fetchone()[0]
        
        # Check if modified data is restored
        cursor.execute("SELECT first_name FROM users WHERE user_id = 1002")
        first_name = cursor.fetchone()[0]
        
        conn.close()
        
        if journal_count > 0 and first_name == 'Test':
            print("✅ Data restored successfully")
            return True
        else:
            print(f"❌ Data restoration incomplete: {journal_count} entries, name: {first_name}")
            return False
    
    async def test_backup_listing(self):
        """Test backup listing functionality"""
        print("\n🧪 Testing backup listing...")
        
        # Create a few backups
        for backup_type in ["manual", "emergency"]:
            success, result = await backup_service.create_full_backup(backup_type)
            if success:
                print(f"✅ Created {backup_type} backup")
        
        # List backups
        backups = await backup_service.list_available_backups()
        
        total_backups = sum(len(backup_list) for backup_list in backups.values())
        print(f"✅ Found {total_backups} total backups")
        
        for backup_type, backup_list in backups.items():
            if backup_list:
                print(f"  • {backup_type}: {len(backup_list)} backups")
        
        return total_backups > 0
    
    async def test_backup_status(self):
        """Test backup status functionality"""
        print("\n🧪 Testing backup status...")
        
        status = await backup_service.get_backup_status()
        
        print(f"✅ Database size: {status['database_size_mb']:.2f} MB")
        print(f"✅ Database integrity: {status['database_integrity']}")
        print(f"✅ Total backups: {status['total_backups']}")
        print(f"✅ Backup storage: {status['backup_directory_size_mb']:.2f} MB")
        
        return status['database_exists'] and status['database_integrity']
    
    async def test_scheduler_functionality(self):
        """Test backup scheduler functionality"""
        print("\n🧪 Testing backup scheduler...")
        
        # Test scheduler start/stop
        backup_scheduler.start_scheduler()
        stats = backup_scheduler.get_backup_statistics()
        
        if stats['scheduler_running']:
            print("✅ Scheduler started successfully")
            
            # Test force backup
            success, result = await backup_scheduler.force_backup("manual")
            if success:
                print(f"✅ Force backup successful: {result}")
            else:
                print(f"❌ Force backup failed: {result}")
            
            backup_scheduler.stop_scheduler()
            print("✅ Scheduler stopped successfully")
            return True
        else:
            print("❌ Scheduler failed to start")
            return False
    
    async def run_all_tests(self):
        """Run all backup system tests"""
        print("🧪 Starting Backup System Test Suite")
        print("=" * 50)
        
        test_results = {}
        
        try:
            await self.setup_test_environment()
            
            # Run individual tests
            tests = [
                ("Database Diagnosis", self.test_database_diagnosis),
                ("Backup Creation", self.test_backup_creation),
                ("Backup Listing", self.test_backup_listing),
                ("Backup Status", self.test_backup_status),
                ("Restore Functionality", self.test_restore_functionality),
                ("Scheduler Functionality", self.test_scheduler_functionality),
            ]
            
            for test_name, test_func in tests:
                try:
                    result = await test_func()
                    test_results[test_name] = result
                except Exception as e:
                    print(f"❌ {test_name} failed with error: {e}")
                    test_results[test_name] = False
            
        finally:
            await self.cleanup_test_environment()
        
        # Print results summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<25} {status}")
            if result:
                passed += 1
        
        print("-" * 50)
        print(f"TOTAL: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED!")
            return False

async def main():
    """Main test function"""
    test_suite = BackupSystemTest()
    success = await test_suite.run_all_tests()
    
    if success:
        print("\n✅ Backup system is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Backup system has issues that need to be addressed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
