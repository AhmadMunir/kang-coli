#!/usr/bin/env python3
"""
Complete Journal Flow Test - Test full journal writing dan reading workflow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.database import db
from src.services.journal_service import JournalService
from src.services.user_service import UserService
from datetime import datetime

def test_complete_journal_workflow():
    """Test complete journal workflow dari start to finish"""
    print("🧪 Testing Complete Journal Workflow")
    print("=" * 60)
    
    # Initialize services
    user_service = UserService()
    journal_service = JournalService()
    
    # Test user data (simulating Telegram user)
    test_user_data = {
        'telegram_id': 123456789,
        'username': 'test_user',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    print(f"👤 Creating test user...")
    
    # Step 1: Create or get user (simulating get_or_create_user)
    user = user_service.get_or_create_user(**test_user_data)
    print(f"✅ User created/retrieved: {user.telegram_id} (@{user.username})")
    
    # Step 2: Check initial journal state (simulating "📖 Baca Entries")
    print(f"\n📖 Step 1: Check initial journal state...")
    initial_entries = journal_service.get_user_entries(user.telegram_id, limit=5)
    initial_stats = journal_service.get_entry_stats(user.telegram_id)
    
    print(f"Initial entries count: {len(initial_entries)}")
    print(f"Initial stats: {initial_stats}")
    
    # Step 3: Write multiple journal entries (simulating user writing)
    print(f"\n✍️ Step 2: Writing journal entries...")
    
    test_entries = [
        {
            'text': "Hari ini adalah hari yang cukup challenging. Saya merasa stress dengan pekerjaan tapi berhasil manage dengan breathing exercises. Grateful untuk support keluarga. Mood sekitar 3/5.",
            'mood': 3
        },
        {
            'text': "Excellent day today! Berhasil menyelesaikan semua tasks dan merasa very productive. Morning routine berjalan smooth dan energy level tinggi sepanjang hari. Mood 5/5!",
            'mood': 5
        },
        {
            'text': "Mixed feelings hari ini. Ada beberapa challenges tapi juga ada small victories. Trying to focus pada positive aspects dan learning dari difficulties. Progress is progress.",
            'mood': 4
        }
    ]
    
    saved_count = 0
    for i, entry_data in enumerate(test_entries, 1):
        print(f"  Writing entry {i}...")
        
        success = journal_service.create_journal_entry(
            telegram_id=user.telegram_id,
            entry_text=entry_data['text'],
            mood_score=entry_data['mood']
        )
        
        if success:
            saved_count += 1
            print(f"  ✅ Entry {i} saved successfully!")
        else:
            print(f"  ❌ Entry {i} failed to save!")
    
    print(f"📊 Successfully saved {saved_count}/{len(test_entries)} entries")
    
    # Step 4: Read entries back (simulating "📖 Baca Entries" after writing)
    print(f"\n📖 Step 3: Reading entries back from database...")
    
    final_entries = journal_service.get_user_entries(user.telegram_id, limit=5)
    final_stats = journal_service.get_entry_stats(user.telegram_id)
    
    print(f"Final entries count: {len(final_entries)}")
    print(f"Final stats: {final_stats}")
    
    # Step 5: Display entries like bot would
    print(f"\n📚 Step 4: Display entries (bot format)...")
    
    if final_entries:
        print(f"✅ Found {len(final_entries)} entries for user {user.telegram_id}")
        print(f"\n📊 Statistics:")
        print(f"• Total entries: {final_stats.get('total_entries', 0)}")
        print(f"• Total words: {final_stats.get('total_words', 0):,}")
        print(f"• Average words: {final_stats.get('average_words', 0)}")
        print(f"• Average mood: {final_stats.get('average_mood', 0):.1f}/5")
        
        print(f"\n📖 Recent entries:")
        for i, entry in enumerate(final_entries[:3], 1):
            date_str = entry.created_at.strftime("%d/%m/%Y %H:%M")
            preview = entry.entry_text[:80] + "..." if len(entry.entry_text) > 80 else entry.entry_text
            word_count = len(entry.entry_text.split())
            
            print(f"{i}. {date_str} (Mood: {entry.mood_score}/5)")
            print(f"   📝 {word_count} words")
            print(f"   {preview}")
            print()
    else:
        print(f"❌ No entries found for user {user.telegram_id}")
        return False
    
    # Step 6: Verify data integrity
    print(f"🔍 Step 5: Verify data integrity...")
    
    # Check if entry count increased
    entry_increase = len(final_entries) - len(initial_entries)
    if entry_increase >= saved_count:
        print(f"✅ Entry count increased correctly (+{entry_increase})")
    else:
        print(f"❌ Entry count increase mismatch (expected +{saved_count}, got +{entry_increase})")
        return False
    
    # Check if stats are reasonable
    if (final_stats.get('total_entries', 0) > 0 and 
        final_stats.get('total_words', 0) > 0 and
        final_stats.get('average_mood') is not None):
        print(f"✅ Statistics are valid and reasonable")
    else:
        print(f"❌ Statistics are invalid: {final_stats}")
        return False
    
    # Check if entries have proper content
    for entry in final_entries[:saved_count]:
        if (entry.entry_text and 
            len(entry.entry_text) > 10 and
            entry.mood_score is not None and
            1 <= entry.mood_score <= 5):
            print(f"✅ Entry {entry.id} has valid content and mood")
        else:
            print(f"❌ Entry {entry.id} has invalid data")
            return False
    
    print(f"\n🎉 ALL TESTS PASSED!")
    print(f"✅ Complete journal workflow is working correctly!")
    print(f"✅ Users can write and read journal entries successfully!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Complete Journal Workflow Test...")
    print("This simulates the full user experience dari start to finish.\n")
    
    try:
        success = test_complete_journal_workflow()
        
        if success:
            print("\n" + "=" * 60)
            print("🎯 CONCLUSION: Journal system is fully functional!")
            print("💾 Database storage: ✅ Working")
            print("✍️ Writing entries: ✅ Working") 
            print("📖 Reading entries: ✅ Working")
            print("📊 Statistics: ✅ Working")
            print("🔍 Data integrity: ✅ Working")
            print("\n🚀 Ready for production use!")
        else:
            print("\n❌ Some tests failed. Check the implementation.")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
