"""
Enhanced Journal Reading Function with Debug Information
"""

from src.utils.logger import app_logger
from src.utils.helpers import get_user_info

async def enhanced_read_journal(self, query, context):
    """Enhanced journal reading with detailed debug info"""
    user_info = get_user_info(query.from_user)
    user = self.user_service.get_or_create_user(**user_info)
    
    try:
        # Get recent entries from database with detailed logging
        app_logger.info(f"Fetching journal entries for user {user.telegram_id}")
        entries = self.journal_service.get_user_entries(user.telegram_id, limit=5)
        stats = self.journal_service.get_entry_stats(user.telegram_id)
        
        app_logger.info(f"Retrieved {len(entries)} entries for user {user.telegram_id}")
        
        if not entries:
            message = f"""
📖 **Debug: Baca Journal Entries**

**Status**: Belum ada journal entries ditemukan untuk User ID: {user.telegram_id}

**🔍 Debug Information:**
• **Telegram ID**: {user.telegram_id}
• **Username**: {user.username or 'N/A'}
• **Full Name**: {user.first_name} {user.last_name or ''}
• **Database Query**: SELECT * FROM journal_entries WHERE telegram_id = {user.telegram_id}

**🎯 Troubleshooting:**
1. **Belum menulis entry** - Try write new entry first
2. **Database not synced** - Entry might not be saved properly  
3. **User ID mismatch** - Check if using same account

**💡 Next Steps:**
1. **Tulis entry baru** → Klik "✍️ Tulis Entry Baru"
2. **Verify save process** → Look for "✅ Entry Tersimpan" confirmation
3. **Check again** → Return here after writing

**🔧 Advanced Debug:**
• Total entries in database: {stats.get('total_entries', 'Error getting count')}
• Database connection: {'OK' if entries is not None else 'ERROR'}

Try writing a new entry to test the system! ✍️
            """
        else:
            # Format recent entries with enhanced detail
            entries_text = ""
            for i, entry in enumerate(entries, 1):
                date_str = entry.created_at.strftime("%d/%m/%Y %H:%M")
                preview = entry.entry_text[:150] + "..." if len(entry.entry_text) > 150 else entry.entry_text
                word_count = len(entry.entry_text.split())
                char_count = len(entry.entry_text)
                mood_display = f" (Mood: {entry.mood_score}/5)" if entry.mood_score else ""
                
                entries_text += f"""
**{i}. {date_str}**{mood_display}
📝 *{word_count} words, {char_count} chars*
📄 Entry ID: {entry.id}
{preview}
"""
            
            first_date = stats.get('first_entry').strftime('%d/%m/%Y') if stats.get('first_entry') else 'N/A'
            last_date = stats.get('last_entry').strftime('%d/%m/%Y') if stats.get('last_entry') else 'N/A'
            avg_mood = stats.get('average_mood')
            mood_display = f"{avg_mood:.1f}/5" if avg_mood is not None else 'N/A'
            
            message = f"""
📖 **Your Journal Entries**

**✅ Database Status**: {len(entries)} entries found for User {user.telegram_id}

**📊 Detailed Statistics:**
• **Total entries**: {stats.get('total_entries', 0)} entries
• **Total words**: {stats.get('total_words', 0):,} words
• **Total characters**: {sum(len(e.entry_text) for e in entries):,} chars
• **Average words per entry**: {stats.get('average_words', 0)} words
• **First entry**: {first_date}
• **Last entry**: {last_date}
• **Average mood**: {mood_display}

**📚 Recent Entries (Last 5):**{entries_text}

**🎯 Excellent Progress!** Database is working correctly dengan {len(entries)} entries.

**💡 Next Level Features:**
• **Pattern Recognition**: Notice mood trends over time
• **Word Count Growth**: Track writing consistency  
• **Growth Tracking**: Compare early vs recent entries
• **Daily Habit**: Build consistent journaling routine

**🏆 Achievement**: {stats.get('total_entries', 0)} total journal entries! 💪✨

Your journaling system is working perfectly! 📖
            """
            
    except Exception as e:
        app_logger.error(f"Error in enhanced_read_journal: {e}")
        message = f"""
❌ **Error Reading Journal Entries**

**Database error occurred while fetching entries.**

**🔍 Error Information:**
• **User ID**: {user.telegram_id}
• **Error Type**: {type(e).__name__}
• **Error Message**: {str(e)}
• **Time**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

**🛠️ Troubleshooting Steps:**
1. **Restart bot** dengan /start command
2. **Check database** - verify connection is working
3. **Try write entry** - test if saving works first
4. **Report issue** if problem persists

We're sorry for the technical difficulty! 🙏
        """
    
    return message
