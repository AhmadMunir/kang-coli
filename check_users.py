#!/usr/bin/env python3
"""
Check Bot User Statistics
Analyze user data and engagement metrics
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import db
from src.database.models import User, CheckIn, JournalEntry, MoodEntry, RelapseRecord
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

def analyze_users():
    """Analyze user statistics and engagement"""
    
    print("👥 ANALYZING BOT USERS")
    print("=" * 50)
    
    try:
        session = db.get_session()
        
        if not session:
            print("❌ Cannot connect to database")
            return
        
        # Total users
        total_users = session.query(User).count()
        print(f"📊 **TOTAL USERS**: {total_users}")
        
        if total_users == 0:
            print("💭 No users found in database")
            session.close()
            return
        
        # Users with recent activity (based on updated_at)
        last_30_days = datetime.now() - timedelta(days=30)
        active_users = session.query(User).filter(
            User.updated_at >= last_30_days
        ).count()
        
        print(f"🔥 **ACTIVE USERS (30 days)**: {active_users}")
        print(f"📈 **ACTIVITY RATE**: {(active_users/total_users*100):.1f}%")
        
        # User registration timeline
        print(f"\n📅 **USER REGISTRATION TIMELINE**")
        users_by_date = session.query(
            func.date(User.created_at).label('date'),
            func.count().label('count')
        ).group_by(func.date(User.created_at)).order_by(desc('date')).limit(10).all()
        
        for date, count in users_by_date:
            print(f"   {date}: {count} new users")
        
        # Engagement metrics
        print(f"\n💪 **ENGAGEMENT METRICS**")
        
        # Check-ins
        total_checkins = session.query(CheckIn).count()
        unique_checkin_users = session.query(CheckIn.user_id).distinct().count()
        print(f"   ✅ Total Check-ins: {total_checkins}")
        print(f"   👤 Users with Check-ins: {unique_checkin_users}")
        if unique_checkin_users > 0:
            avg_checkins = total_checkins / unique_checkin_users
            print(f"   📊 Avg Check-ins per User: {avg_checkins:.1f}")
        
        # Journal entries
        total_journals = session.query(JournalEntry).count()
        unique_journal_users = session.query(JournalEntry.user_id).distinct().count()
        print(f"   📝 Total Journal Entries: {total_journals}")
        print(f"   👤 Users with Journals: {unique_journal_users}")
        if unique_journal_users > 0:
            avg_journals = total_journals / unique_journal_users
            print(f"   📊 Avg Journals per User: {avg_journals:.1f}")
        
        # Mood entries (new feature)
        total_moods = session.query(MoodEntry).count()
        unique_mood_users = session.query(MoodEntry.user_id).distinct().count()
        print(f"   🌡️ Total Mood Entries: {total_moods}")
        print(f"   👤 Users with Mood Tracking: {unique_mood_users}")
        if unique_mood_users > 0:
            avg_moods = total_moods / unique_mood_users
            print(f"   📊 Avg Mood Entries per User: {avg_moods:.1f}")
        
        # Relapse records
        total_relapses = session.query(RelapseRecord).count()
        unique_relapse_users = session.query(RelapseRecord.user_id).distinct().count()
        print(f"   ⚠️ Total Relapse Records: {total_relapses}")
        print(f"   👤 Users with Relapses: {unique_relapse_users}")
        
        # User settings analysis
        print(f"\n⚙️ **USER PREFERENCES**")
        
        users_with_reminders = session.query(User).filter(
            User.daily_reminders == True
        ).count()
        reminder_rate = (users_with_reminders / total_users * 100) if total_users > 0 else 0
        print(f"   🔔 Users with Daily Reminders: {users_with_reminders} ({reminder_rate:.1f}%)")
        
        # Timezone preferences
        timezone_stats = session.query(
            User.timezone,
            func.count().label('count')
        ).group_by(User.timezone).all()
        
        print(f"   🌐 Timezone Distribution:")
        for timezone, count in timezone_stats:
            timezone_name = timezone or 'Not set'
            percentage = (count / total_users * 100) if total_users > 0 else 0
            print(f"      {timezone_name}: {count} users ({percentage:.1f}%)")
        
        # Streak analysis
        print(f"\n🏆 **RECOVERY PROGRESS**")
        
        users_with_streaks = session.query(User).filter(User.current_streak > 0).count()
        if users_with_streaks > 0:
            avg_current_streak = session.query(func.avg(User.current_streak)).filter(User.current_streak > 0).scalar()
            max_current_streak = session.query(func.max(User.current_streak)).scalar()
            avg_longest_streak = session.query(func.avg(User.longest_streak)).filter(User.longest_streak > 0).scalar()
            max_longest_streak = session.query(func.max(User.longest_streak)).scalar()
            
            print(f"   🔥 Users with Active Streaks: {users_with_streaks}")
            print(f"   📊 Average Current Streak: {avg_current_streak:.1f} days")
            print(f"   🎯 Highest Current Streak: {max_current_streak} days")
            print(f"   📈 Average Best Streak: {avg_longest_streak or 0:.1f} days")
            print(f"   🏆 All-time Best Streak: {max_longest_streak or 0} days")
        else:
            print(f"   💭 No active streaks found")
        
        # Most active users by check-ins
        print(f"\n🏆 **TOP ACTIVE USERS**")
        
        if total_checkins > 0:
            top_checkin_users = session.query(
                User.telegram_id,
                User.username,
                func.count(CheckIn.id).label('checkin_count')
            ).join(CheckIn, User.id == CheckIn.user_id)\
             .group_by(User.id)\
             .order_by(desc('checkin_count'))\
             .limit(5).all()
            
            print("   📈 By Check-ins:")
            for i, (telegram_id, username, count) in enumerate(top_checkin_users, 1):
                username_display = f"@{username}" if username else f"ID:{telegram_id}"
                print(f"      {i}. {username_display}: {count} check-ins")
        
        # Users by journal entries
        if total_journals > 0:
            top_journal_users = session.query(
                User.telegram_id,
                User.username,
                func.count(JournalEntry.id).label('journal_count')
            ).join(JournalEntry, User.id == JournalEntry.user_id)\
             .group_by(User.id)\
             .order_by(desc('journal_count'))\
             .limit(5).all()
            
            print("   📝 By Journal Entries:")
            for i, (telegram_id, username, count) in enumerate(top_journal_users, 1):
                username_display = f"@{username}" if username else f"ID:{telegram_id}"
                print(f"      {i}. {username_display}: {count} journals")
        
        # Recent activity
        print(f"\n⏰ **RECENT ACTIVITY (Last 7 days)**")
        
        last_week = datetime.now() - timedelta(days=7)
        
        recent_checkins = session.query(CheckIn).filter(
            CheckIn.created_at >= last_week
        ).count()
        
        recent_journals = session.query(JournalEntry).filter(
            JournalEntry.created_at >= last_week
        ).count()
        
        recent_moods = session.query(MoodEntry).filter(
            MoodEntry.created_at >= last_week
        ).count()
        
        recent_active_users = session.query(User).filter(
            User.updated_at >= last_week
        ).count()
        
        print(f"   👤 Active Users: {recent_active_users}")
        print(f"   ✅ Check-ins: {recent_checkins}")
        print(f"   📝 Journal Entries: {recent_journals}")
        print(f"   🌡️ Mood Entries: {recent_moods}")
        
        # User growth analysis
        print(f"\n📈 **GROWTH ANALYSIS**")
        
        # Users in different time periods
        last_7_days = datetime.now() - timedelta(days=7)
        last_30_days = datetime.now() - timedelta(days=30)
        last_90_days = datetime.now() - timedelta(days=90)
        
        new_users_7d = session.query(User).filter(User.created_at >= last_7_days).count()
        new_users_30d = session.query(User).filter(User.created_at >= last_30_days).count()
        new_users_90d = session.query(User).filter(User.created_at >= last_90_days).count()
        
        print(f"   📊 New Users (7 days): {new_users_7d}")
        print(f"   📊 New Users (30 days): {new_users_30d}")
        print(f"   📊 New Users (90 days): {new_users_90d}")
        
        # Retention analysis
        if total_users > 0:
            retention_7d = (recent_active_users / total_users * 100)
            retention_30d = (active_users / total_users * 100)
            print(f"   🔄 7-day Retention: {retention_7d:.1f}%")
            print(f"   🔄 30-day Retention: {retention_30d:.1f}%")
        
        session.close()
        
        print(f"\n🎯 **KEY INSIGHTS**")
        
        if total_users < 10:
            print("   💡 Bot is in early stage - focus on user acquisition")
        elif active_users / total_users < 0.3:
            print("   💡 Consider improving user engagement strategies")
        else:
            print("   🎉 Good user engagement levels!")
        
        if unique_mood_users > 0:
            print("   ✨ Mood tracking feature is being used - great!")
        else:
            print("   💭 Mood tracking is new - monitor adoption")
        
        print(f"\n✅ Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error analyzing users: {e}")
        import traceback
        traceback.print_exc()

def show_user_details():
    """Show detailed user information"""
    
    print("\n\n👤 DETAILED USER INFORMATION")
    print("=" * 50)
    
    try:
        session = db.get_session()
        
        # Get all users with basic info
        users = session.query(User).order_by(desc(User.created_at)).all()
        
        print(f"📋 **USER LIST** ({len(users)} total)")
        print("-" * 40)
        
        for i, user in enumerate(users, 1):
            print(f"{i}. User ID: {user.telegram_id}")
            if user.username:
                print(f"   Username: @{user.username}")
            if user.first_name:
                print(f"   Name: {user.first_name}")
            print(f"   Joined: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Last Updated: {user.updated_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Daily Reminders: {'✅' if user.daily_reminders else '❌'}")
            print(f"   Reminder Time: {user.reminder_time}")
            print(f"   Timezone: {user.timezone}")
            print(f"   Current Streak: {user.current_streak} days")
            print(f"   Longest Streak: {user.longest_streak} days")
            print(f"   Total Relapses: {user.total_relapses}")
            if user.clean_start_date:
                print(f"   Clean Since: {user.clean_start_date.strftime('%Y-%m-%d')}")
            if user.last_relapse_date:
                print(f"   Last Relapse: {user.last_relapse_date.strftime('%Y-%m-%d')}")
            print()
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error showing user details: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("🕐 User Analysis started at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Analyze user statistics
    analyze_users()
    
    # Show detailed user info
    show_user_details()
    
    print("🕐 Analysis completed at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    main()
