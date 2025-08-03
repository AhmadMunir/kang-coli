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
