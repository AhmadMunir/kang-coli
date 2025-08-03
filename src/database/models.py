from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

Base = declarative_base()

class User(Base):
    """User model untuk menyimpan data pengguna"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    # Recovery tracking
    clean_start_date = Column(DateTime, nullable=True)
    last_relapse_date = Column(DateTime, nullable=True)
    total_relapses = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    
    # User preferences
    daily_reminders = Column(Boolean, default=True)
    reminder_time = Column(String(5), default="08:00")  # Format: HH:MM
    timezone = Column(String(50), default="Asia/Jakarta")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

class JournalEntry(Base):
    """Model untuk menyimpan journal entries pengguna"""
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Foreign key ke User.id
    telegram_id = Column(Integer, nullable=False)
    
    entry_text = Column(Text, nullable=False)
    mood_score = Column(Integer, nullable=True)  # 1-10 scale
    triggers = Column(Text, nullable=True)  # JSON string untuk list triggers
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<JournalEntry(user_id={self.user_id}, created_at={self.created_at})>"

class RelapseRecord(Base):
    """Model untuk menyimpan riwayat relapse"""
    __tablename__ = "relapse_records"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    
    relapse_date = Column(DateTime, nullable=False)
    streak_broken = Column(Integer, nullable=False)  # Streak yang terputus
    notes = Column(Text, nullable=True)
    triggers = Column(Text, nullable=True)  # JSON string
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RelapseRecord(user_id={self.user_id}, streak_broken={self.streak_broken})>"

class CheckIn(Base):
    """Model untuk daily check-ins"""
    __tablename__ = "check_ins"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    
    check_in_date = Column(DateTime, nullable=False)
    mood_score = Column(Integer, nullable=True)  # 1-10 scale
    urge_level = Column(Integer, nullable=True)  # 1-10 scale
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CheckIn(user_id={self.user_id}, check_in_date={self.check_in_date})>"

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
