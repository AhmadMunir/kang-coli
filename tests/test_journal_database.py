#!/usr/bin/env python3
"""
Test script untuk check journal database functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.database import db
from src.database.models import JournalEntry
from src.services.journal_service import JournalService
from datetime import datetime

def test_journal_database():
    """Test journal database operations"""
    print("🧪 Testing Journal Database Operations...")
    
    # Initialize service
    journal_service = JournalService()
    test_telegram_id = 123456789
    
    print(f"\n📊 Initial state - Checking existing entries...")
    initial_count = journal_service.get_entry_count(test_telegram_id)
    print(f"Initial entry count: {initial_count}")
    
    # Test creating journal entry
    print(f"\n✍️ Testing journal entry creation...")
    test_entry = "Ini adalah test journal entry untuk memastikan database berfungsi dengan baik. Hari ini testing sistem journal dengan berbagai fitur."
    
    success = journal_service.create_journal_entry(
        telegram_id=test_telegram_id,
        entry_text=test_entry,
        mood_score=4
    )
    
    if success:
        print("✅ Journal entry created successfully!")
    else:
        print("❌ Failed to create journal entry!")
        return False
    
    # Test retrieving entries
    print(f"\n📖 Testing entry retrieval...")
    entries = journal_service.get_user_entries(test_telegram_id, limit=5)
    new_count = journal_service.get_entry_count(test_telegram_id)
    
    print(f"New entry count: {new_count}")
    print(f"Retrieved entries: {len(entries)}")
    
    if entries:
        latest_entry = entries[0]
        print(f"Latest entry preview: {latest_entry.entry_text[:50]}...")
        print(f"Created at: {latest_entry.created_at}")
        print(f"Mood score: {latest_entry.mood_score}")
    
    # Test statistics
    print(f"\n📊 Testing statistics...")
    stats = journal_service.get_entry_stats(test_telegram_id)
    print(f"Statistics: {stats}")
    
    # Check if count increased
    if new_count > initial_count:
        print(f"\n✅ SUCCESS: Entry count increased from {initial_count} to {new_count}")
        return True
    else:
        print(f"\n❌ FAILED: Entry count did not increase")
        return False

def check_database_tables():
    """Check if database tables exist"""
    print("\n🗄️ Checking database tables...")
    
    session = db.get_session()
    try:
        # Check if we can query the table
        count = session.query(JournalEntry).count()
        print(f"✅ JournalEntry table exists with {count} total entries")
        
        # Show recent entries
        recent = session.query(JournalEntry).order_by(JournalEntry.created_at.desc()).limit(5).all()
        if recent:
            print(f"\n📖 Recent entries in database:")
            for i, entry in enumerate(recent, 1):
                print(f"{i}. User {entry.telegram_id}: {entry.entry_text[:50]}... ({entry.created_at})")
        else:
            print("No entries found in database")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    finally:
        db.close_session(session)
    
    return True

if __name__ == "__main__":
    print("🚀 Journal Database Test Started")
    print("=" * 50)
    
    # Check tables first
    if not check_database_tables():
        print("❌ Database table check failed!")
        exit(1)
    
    # Test journal operations
    if test_journal_database():
        print("\n🎉 All tests passed! Journal system is working correctly.")
    else:
        print("\n❌ Some tests failed! Check the implementation.")
        exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Journal Database Test Completed")
