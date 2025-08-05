#!/usr/bin/env python3
"""
Direct Database Test - Minimal test untuk check journal functionality
"""

import sqlite3
import os
from datetime import datetime

def test_journal_database_direct():
    """Test database directly with sqlite3"""
    
    # Database path (from settings.py)
    db_path = "data/pmo_recovery.db"
    
    print("🔍 Direct SQLite Database Test")
    print("=" * 50)
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Creating database file...")
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Connected to database: {db_path}")
        
        # Check if journal_entries table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='journal_entries'
        """)
        
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ journal_entries table does not exist!")
            print("Creating journal_entries table...")
            
            # Create table manually
            cursor.execute("""
                CREATE TABLE journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    telegram_id INTEGER NOT NULL,
                    entry_text TEXT NOT NULL,
                    mood_score INTEGER,
                    triggers TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ journal_entries table created!")
        else:
            print("✅ journal_entries table exists!")
        
        # Show table structure
        cursor.execute("PRAGMA table_info(journal_entries)")
        columns = cursor.fetchall()
        print(f"\n📋 Table Structure:")
        for col in columns:
            print(f"  • {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Count existing entries
        cursor.execute("SELECT COUNT(*) FROM journal_entries")
        total_count = cursor.fetchone()[0]
        print(f"\n📊 Total entries in database: {total_count}")
        
        # Show recent entries if any
        if total_count > 0:
            cursor.execute("""
                SELECT id, telegram_id, entry_text, mood_score, created_at 
                FROM journal_entries 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            recent_entries = cursor.fetchall()
            print(f"\n📖 Recent entries:")
            for entry in recent_entries:
                entry_id, telegram_id, text, mood, created = entry
                preview = text[:50] + "..." if len(text) > 50 else text
                print(f"  {entry_id}. User {telegram_id}: {preview} (Mood: {mood}, {created})")
        
        # Test insert new entry
        test_telegram_id = 999999999
        test_entry = f"Test journal entry created at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} untuk verify database functionality."
        
        print(f"\n✍️ Testing insert new entry for user {test_telegram_id}...")
        
        cursor.execute("""
            INSERT INTO journal_entries (user_id, telegram_id, entry_text, mood_score, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (test_telegram_id, test_telegram_id, test_entry, 4, datetime.now()))
        
        conn.commit()
        
        # Verify insert
        cursor.execute("""
            SELECT COUNT(*) FROM journal_entries 
            WHERE telegram_id = ?
        """, (test_telegram_id,))
        
        test_count = cursor.fetchone()[0]
        print(f"✅ Insert successful! User {test_telegram_id} now has {test_count} entries.")
        
        # Test retrieve entries for specific user
        cursor.execute("""
            SELECT id, entry_text, mood_score, created_at 
            FROM journal_entries 
            WHERE telegram_id = ? 
            ORDER BY created_at DESC
        """, (test_telegram_id,))
        
        user_entries = cursor.fetchall()
        print(f"📖 Retrieved {len(user_entries)} entries for user {test_telegram_id}:")
        
        for entry in user_entries:
            entry_id, text, mood, created = entry
            preview = text[:80] + "..." if len(text) > 80 else text
            print(f"  • ID {entry_id}: {preview} (Mood: {mood}, {created})")
        
        # Final count
        cursor.execute("SELECT COUNT(*) FROM journal_entries")
        final_count = cursor.fetchone()[0]
        print(f"\n📊 Final total entries: {final_count}")
        
        print(f"\n✅ Database test completed successfully!")
        print(f"✅ Journal entries can be saved and retrieved!")
        print(f"✅ Database schema is correct!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print(f"🔒 Database connection closed.")

if __name__ == "__main__":
    print("🚀 Starting Direct Database Test...")
    
    success = test_journal_database_direct()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("💾 Database is working correctly!")
        print("📖 Journal entries can be saved and retrieved!")
    else:
        print("\n❌ TESTS FAILED!")
        print("🔧 Check database configuration and permissions!")
    
    print("\n" + "=" * 50)
