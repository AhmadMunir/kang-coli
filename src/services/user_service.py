from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.database import db

class UserService:
    """Service untuk mengelola user data"""
    
    @staticmethod
    def get_or_create_user(telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> User:
        """Get existing user or create new one"""
        session = db.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    clean_start_date=datetime.utcnow()
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            else:
                # Update user info if changed
                updated = False
                if user.username != username:
                    user.username = username
                    updated = True
                if user.first_name != first_name:
                    user.first_name = first_name
                    updated = True
                if user.last_name != last_name:
                    user.last_name = last_name
                    updated = True
                
                if updated:
                    user.updated_at = datetime.utcnow()
                    session.commit()
                    session.refresh(user)
            
            return user
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_user(telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        session = db.get_session()
        try:
            return session.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            db.close_session(session)
    
    @staticmethod
    def update_user_preferences(telegram_id: int, daily_reminders: bool = None,
                              reminder_time: str = None, timezone: str = None) -> bool:
        """Update user preferences"""
        session = db.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return False
            
            if daily_reminders is not None:
                user.daily_reminders = daily_reminders
            if reminder_time is not None:
                user.reminder_time = reminder_time
            if timezone is not None:
                user.timezone = timezone
            
            user.updated_at = datetime.utcnow()
            session.commit()
            return True
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_all_users_with_reminders() -> list[User]:
        """Get all users who have daily reminders enabled"""
        session = db.get_session()
        try:
            return session.query(User).filter(User.daily_reminders == True).all()
        finally:
            db.close_session(session)
    
    @staticmethod
    def has_checked_in_today(telegram_id: int) -> bool:
        """Check if user has done mood check-in today"""
        session = db.get_session()
        try:
            from src.database.models import MoodEntry
            today = datetime.now().date()
            
            mood_entry = session.query(MoodEntry).filter(
                MoodEntry.user_id == telegram_id,
                MoodEntry.created_at >= datetime.combine(today, datetime.min.time()),
                MoodEntry.created_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
            ).first()
            
            return mood_entry is not None
        except Exception:
            return False
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_users_without_checkin_today() -> list[User]:
        """Get users with reminders enabled who haven't checked in today"""
        session = db.get_session()
        try:
            from src.database.models import MoodEntry
            today = datetime.now().date()
            
            # Get all users with reminders
            users_with_reminders = session.query(User).filter(User.daily_reminders == True).all()
            
            users_without_checkin = []
            for user in users_with_reminders:
                # Check if user has mood entry today
                mood_entry = session.query(MoodEntry).filter(
                    MoodEntry.user_id == user.telegram_id,
                    MoodEntry.created_at >= datetime.combine(today, datetime.min.time()),
                    MoodEntry.created_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
                ).first()
                
                if not mood_entry:
                    users_without_checkin.append(user)
            
            return users_without_checkin
        except Exception:
            return []
        finally:
            db.close_session(session)
    
    @staticmethod
    def record_mood_checkin(telegram_id: int, mood_score: int, notes: str = None) -> bool:
        """Record daily mood check-in"""
        session = db.get_session()
        try:
            from src.database.models import MoodEntry
            
            # Check if already checked in today
            today = datetime.now().date()
            existing_entry = session.query(MoodEntry).filter(
                MoodEntry.user_id == telegram_id,
                MoodEntry.created_at >= datetime.combine(today, datetime.min.time()),
                MoodEntry.created_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
            ).first()
            
            if existing_entry:
                # Update existing entry
                existing_entry.mood_score = mood_score
                existing_entry.notes = notes
                existing_entry.updated_at = datetime.utcnow()
            else:
                # Create new entry
                mood_entry = MoodEntry(
                    user_id=telegram_id,
                    mood_score=mood_score,
                    notes=notes
                )
                session.add(mood_entry)
            
            session.commit()
            return True
        except Exception:
            return False
        finally:
            db.close_session(session)
