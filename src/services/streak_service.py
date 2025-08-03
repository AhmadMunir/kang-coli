from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import User, RelapseRecord
from src.database.database import db

class StreakService:
    """Service untuk mengelola streak tracking"""
    
    @staticmethod
    def calculate_current_streak(telegram_id: int) -> int:
        """Calculate current clean streak in days"""
        session = db.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return 0
            
            if not user.clean_start_date:
                return 0
            
            # Calculate days since last clean start
            now = datetime.utcnow()
            streak_days = (now - user.clean_start_date).days
            
            # Update current streak in database
            user.current_streak = streak_days
            session.commit()
            
            return streak_days
        finally:
            db.close_session(session)
    
    @staticmethod
    def record_relapse(telegram_id: int, notes: str = None, triggers: list = None) -> bool:
        """Record a relapse and reset streak"""
        session = db.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return False
            
            # Calculate current streak before reset
            current_streak = StreakService.calculate_current_streak(telegram_id)
            
            # Update longest streak if current is longer
            if current_streak > user.longest_streak:
                user.longest_streak = current_streak
            
            # Create relapse record
            relapse = RelapseRecord(
                user_id=user.id,
                telegram_id=telegram_id,
                relapse_date=datetime.utcnow(),
                streak_broken=current_streak,
                notes=notes,
                triggers=str(triggers) if triggers else None
            )
            session.add(relapse)
            
            # Reset user streak
            user.last_relapse_date = datetime.utcnow()
            user.clean_start_date = datetime.utcnow()
            user.current_streak = 0
            user.total_relapses += 1
            user.updated_at = datetime.utcnow()
            
            session.commit()
            return True
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_streak_stats(telegram_id: int) -> dict:
        """Get comprehensive streak statistics"""
        session = db.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return {}
            
            current_streak = StreakService.calculate_current_streak(telegram_id)
            
            # Get total days since first start (including relapses)
            total_days = 0
            if user.created_at:
                total_days = (datetime.utcnow() - user.created_at).days
            
            # Calculate success rate
            success_rate = 0
            if total_days > 0:
                clean_days = total_days - (user.total_relapses * 1)  # Simplified calculation
                success_rate = max(0, (clean_days / total_days) * 100)
            
            return {
                'current_streak': current_streak,
                'longest_streak': user.longest_streak,
                'total_relapses': user.total_relapses,
                'success_rate': round(success_rate, 1),
                'clean_start_date': user.clean_start_date,
                'last_relapse_date': user.last_relapse_date,
                'total_days': total_days
            }
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_streak_milestones(current_streak: int) -> dict:
        """Get milestone information for current streak"""
        milestones = [1, 3, 7, 14, 30, 60, 90, 180, 365]
        
        # Find current milestone
        current_milestone = 0
        for milestone in milestones:
            if current_streak >= milestone:
                current_milestone = milestone
            else:
                break
        
        # Find next milestone
        next_milestone = None
        for milestone in milestones:
            if milestone > current_streak:
                next_milestone = milestone
                break
        
        return {
            'current_milestone': current_milestone,
            'next_milestone': next_milestone,
            'days_to_next': next_milestone - current_streak if next_milestone else 0,
            'milestone_messages': {
                1: "🎉 Hari pertama! Langkah pertama adalah yang terpenting.",
                3: "💪 3 hari clean! Tubuh mulai merasakan perubahan positif.",
                7: "🌟 Seminggu clean! Sistem dopamine mulai recovery.",
                14: "🔥 2 minggu! Mental clarity mulai terasa.",
                30: "🏆 Sebulan clean! Achievement luar biasa!",
                60: "🌈 2 bulan! Perubahan besar dalam hidup.",
                90: "👑 3 bulan! Kamu sudah sangat kuat!",
                180: "🎯 6 bulan! Master of self-control!",
                365: "🏅 Setahun clean! Legendary achievement!"
            }
        }
