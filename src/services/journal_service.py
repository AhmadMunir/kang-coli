from datetime import datetime
from typing import List, Optional
from src.database.database import db
from src.database.models import JournalEntry
from src.utils.logger import app_logger

class JournalService:
    """Service untuk mengelola journal entries"""
    
    def __init__(self):
        pass
    
    def create_journal_entry(self, telegram_id: int, entry_text: str, mood_score: Optional[int] = None) -> bool:
        """Create new journal entry"""
        session = db.get_session()
        
        try:
            # Create new journal entry
            new_entry = JournalEntry(
                user_id=telegram_id,  # Using telegram_id as user_id for simplicity
                telegram_id=telegram_id,
                entry_text=entry_text,
                mood_score=mood_score,
                created_at=datetime.utcnow()
            )
            
            session.add(new_entry)
            session.commit()
            
            app_logger.info(f"Journal entry created for user {telegram_id}")
            return True
            
        except Exception as e:
            session.rollback()
            app_logger.error(f"Error creating journal entry: {e}")
            return False
        finally:
            db.close_session(session)
    
    def get_user_entries(self, telegram_id: int, limit: int = 10) -> List[JournalEntry]:
        """Get recent journal entries for user"""
        session = db.get_session()
        
        try:
            entries = session.query(JournalEntry)\
                .filter(JournalEntry.telegram_id == telegram_id)\
                .order_by(JournalEntry.created_at.desc())\
                .limit(limit)\
                .all()
            
            return entries
            
        except Exception as e:
            app_logger.error(f"Error getting journal entries: {e}")
            return []
        finally:
            db.close_session(session)
    
    def get_entry_count(self, telegram_id: int) -> int:
        """Get total journal entry count for user"""
        session = db.get_session()
        
        try:
            count = session.query(JournalEntry)\
                .filter(JournalEntry.telegram_id == telegram_id)\
                .count()
            
            return count
            
        except Exception as e:
            app_logger.error(f"Error getting entry count: {e}")
            return 0
        finally:
            db.close_session(session)
    
    def get_entry_stats(self, telegram_id: int) -> dict:
        """Get journal statistics for user"""
        session = db.get_session()
        
        try:
            entries = session.query(JournalEntry)\
                .filter(JournalEntry.telegram_id == telegram_id)\
                .all()
            
            if not entries:
                return {
                    'total_entries': 0,
                    'total_words': 0,
                    'average_words': 0,
                    'first_entry': None,
                    'last_entry': None,
                    'average_mood': None
                }
            
            total_words = sum(len(entry.entry_text.split()) for entry in entries)
            mood_scores = [entry.mood_score for entry in entries if entry.mood_score is not None]
            
            stats = {
                'total_entries': len(entries),
                'total_words': total_words,
                'average_words': total_words // len(entries) if entries else 0,
                'first_entry': entries[-1].created_at if entries else None,
                'last_entry': entries[0].created_at if entries else None,
                'average_mood': sum(mood_scores) / len(mood_scores) if mood_scores else None
            }
            
            return stats
            
        except Exception as e:
            app_logger.error(f"Error getting entry stats: {e}")
            return {}
        finally:
            db.close_session(session)
