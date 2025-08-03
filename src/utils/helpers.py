from datetime import datetime, timedelta
from typing import Dict, Any
from telegram import User

def get_user_info(user: User) -> Dict[str, Any]:
    """Extract user information from Telegram User object"""
    return {
        'telegram_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

def format_streak_message(current_streak: int, stats: dict, milestones: dict) -> str:
    """Format streak information into a beautiful message"""
    
    # Get milestone info
    current_milestone = milestones.get('current_milestone', 0)
    next_milestone = milestones.get('next_milestone')
    days_to_next = milestones.get('days_to_next', 0)
    milestone_messages = milestones.get('milestone_messages', {})
    
    # Build the message
    message = f"""
📊 **Your Recovery Progress**

🔥 **Current Streak: {current_streak} hari**
🏆 **Longest Streak: {stats['longest_streak']} hari**
📈 **Success Rate: {stats['success_rate']}%**

**Milestone Status:**
"""
    
    # Add current milestone achievement
    if current_milestone > 0 and current_milestone in milestone_messages:
        message += f"✅ **Achieved:** {milestone_messages[current_milestone]}\n"
    
    # Add next milestone target
    if next_milestone:
        message += f"🎯 **Next Target:** {next_milestone} hari (dalam {days_to_next} hari lagi)\n"
    else:
        message += "👑 **You've reached legendary status!**\n"
    
    # Add motivational section based on streak
    if current_streak == 0:
        message += "\n🌱 **Starting Fresh:** Setiap journey dimulai dari langkah pertama. Today is day one!"
    elif current_streak < 7:
        message += f"\n💪 **Building Momentum:** {current_streak} hari! Tubuh mulai merasakan perubahan positif."
    elif current_streak < 30:
        message += f"\n🔥 **Strong Progress:** {current_streak} hari! Sistem dopamine mulai recovery."
    elif current_streak < 90:
        message += f"\n🌟 **Excellent Work:** {current_streak} hari! Mental clarity sedang berkembang."
    else:
        message += f"\n👑 **Legendary Status:** {current_streak} hari! Master of self-control!"
    
    # Add recovery benefits section
    message += "\n\n**Recovery Benefits at Your Stage:**"
    benefits = get_recovery_benefits(current_streak)
    for benefit in benefits:
        message += f"\n• {benefit}"
    
    message += "\n\n💪 Keep going strong! Every day counts!"
    
    return message

def get_recovery_benefits(streak_days: int) -> list:
    """Get recovery benefits based on streak length"""
    if streak_days == 0:
        return [
            "Detoxification process dimulai",
            "Motivasi untuk berubah meningkat",
            "Kesadaran akan masalah bertambah"
        ]
    elif streak_days <= 3:
        return [
            "Dopamine receptors mulai recovery",
            "Motivasi natural mulai kembali",
            "Energi fisik meningkat"
        ]
    elif streak_days <= 7:
        return [
            "Kualitas tidur membaik",
            "Mood swings mulai stabil",
            "Konsentrasi meningkat"
        ]
    elif streak_days <= 14:
        return [
            "Mental clarity lebih baik",
            "Kepercayaan diri meningkat",
            "Social anxiety berkurang"
        ]
    elif streak_days <= 30:
        return [
            "Produktivitas meningkat signifikan",
            "Relationship dengan orang lain membaik",
            "Hobi dan interest kembali menarik"
        ]
    elif streak_days <= 60:
        return [
            "Perubahan fisik terlihat (postur, eye contact)",
            "Kreativitas dan problem-solving membaik",
            "Inner peace dan self-respect kuat"
        ]
    elif streak_days <= 90:
        return [
            "Rewiring otak hampir complete",
            "Natural confidence dan charisma",
            "Emotional stability excellent"
        ]
    else:
        return [
            "Complete neuroplasticity transformation",
            "Master-level self-control",
            "Inspirasi untuk orang lain",
            "Life satisfaction tinggi"
        ]

def format_duration(start_date: datetime, end_date: datetime = None) -> str:
    """Format duration between two dates"""
    if not end_date:
        end_date = datetime.utcnow()
    
    duration = end_date - start_date
    days = duration.days
    
    if days == 0:
        hours = duration.seconds // 3600
        if hours == 0:
            minutes = duration.seconds // 60
            return f"{minutes} menit"
        return f"{hours} jam"
    elif days == 1:
        return "1 hari"
    else:
        return f"{days} hari"

def calculate_success_rate(total_days: int, clean_days: int) -> float:
    """Calculate success rate percentage"""
    if total_days == 0:
        return 0.0
    return (clean_days / total_days) * 100

def get_motivational_emoji(streak: int) -> str:
    """Get appropriate emoji based on streak"""
    if streak == 0:
        return "🌱"
    elif streak < 7:
        return "💪"
    elif streak < 30:
        return "🔥"
    elif streak < 90:
        return "🌟"
    else:
        return "👑"

def format_time_ago(date: datetime) -> str:
    """Format datetime as 'time ago' string"""
    if not date:
        return "Tidak ada data"
    
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 0:
        return f"{diff.days} hari yang lalu"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} jam yang lalu"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} menit yang lalu"
    else:
        return "Baru saja"

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = text.strip()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized

def validate_mood_score(score: int) -> bool:
    """Validate mood score (1-10)"""
    return 1 <= score <= 10

def get_mood_emoji(score: int) -> str:
    """Get emoji representation of mood score"""
    if score <= 2:
        return "😢"
    elif score <= 4:
        return "😕"
    elif score <= 6:
        return "😐"
    elif score <= 8:
        return "🙂"
    else:
        return "😊"
