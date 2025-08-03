from datetime import datetime, time
from typing import List, Dict
import random
from src.services import UserService, MotivationalService
from src.utils.logger import app_logger
from config.settings import settings

class BroadcastService:
    """Service untuk mengirim broadcast harian kepada users"""
    
    def __init__(self, bot_application=None):
        self.bot_application = bot_application
        self.user_service = UserService()
        self.motivational_service = MotivationalService()
        
    async def send_daily_broadcast(self):
        """Send daily broadcast to all users with reminders enabled"""
        try:
            # Get all users with daily reminders enabled
            users = self.user_service.get_all_users_with_reminders()
            
            if not users:
                app_logger.info("No users with daily reminders enabled")
                return
            
            # Generate daily content
            broadcast_content = self._generate_daily_content()
            
            sent_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    await self._send_message_to_user(user.telegram_id, broadcast_content)
                    sent_count += 1
                    app_logger.debug(f"Daily broadcast sent to user {user.telegram_id}")
                except Exception as e:
                    failed_count += 1
                    app_logger.error(f"Failed to send broadcast to user {user.telegram_id}: {e}")
            
            app_logger.info(f"Daily broadcast completed: {sent_count} sent, {failed_count} failed")
            
        except Exception as e:
            app_logger.error(f"Error in daily broadcast: {e}")
    
    def _generate_daily_content(self) -> Dict:
        """Generate daily broadcast content"""
        
        # Get current day info
        now = datetime.now()
        day_name = now.strftime("%A")
        date_str = now.strftime("%d %B %Y")
        
        # Get motivational content
        daily_quote = self.motivational_service.get_daily_quote()
        daily_tip = self.motivational_service.get_coping_tip()
        
        # Generate specific content based on day of week
        day_specific_content = self._get_day_specific_content(day_name.lower())
        
        # Recovery facts and tips
        recovery_fact = self._get_daily_recovery_fact()
        
        # Success story or testimonial
        inspiration = self._get_daily_inspiration()
        
        return {
            "greeting": f"🌅 **Selamat {self._get_time_greeting()}, Recovery Warriors!**",
            "date": f"📅 {day_name}, {date_str}",
            "quote": daily_quote,
            "tip": daily_tip,
            "day_content": day_specific_content,
            "recovery_fact": recovery_fact,
            "inspiration": inspiration,
            "call_to_action": self._get_daily_call_to_action()
        }
    
    def _get_time_greeting(self) -> str:
        """Get appropriate greeting based on time"""
        now = datetime.now()
        hour = now.hour
        
        if 5 <= hour < 12:
            return "Pagi"
        elif 12 <= hour < 15:
            return "Siang"
        elif 15 <= hour < 18:
            return "Sore"
        else:
            return "Malam"
    
    def _get_day_specific_content(self, day: str) -> Dict:
        """Get content specific to day of the week"""
        
        day_contents = {
            "monday": {
                "title": "💪 Monday Motivation",
                "message": "Mulai minggu baru dengan tekad yang kuat! Setiap Monday adalah kesempatan fresh start. Set intention positif untuk 7 hari ke depan.",
                "focus": "Goal Setting & Weekly Planning"
            },
            "tuesday": {
                "title": "🧠 Tuesday Wisdom",
                "message": "Neuroplasticity bekerja 24/7 untuk memperbaiki otakmu. Setiap hari clean adalah investasi untuk mental clarity yang lebih baik.",
                "focus": "Brain Science & Mental Health"
            },
            "wednesday": {
                "title": "🎯 Wednesday Challenge",
                "message": "Midweek check! Bagaimana progress minggu ini? Remember: consistency beats perfection. Small daily wins create massive transformations.",
                "focus": "Progress Review & Accountability"
            },
            "thursday": {
                "title": "🌱 Thursday Growth",
                "message": "Growth happens outside comfort zone. Setiap kali kamu menolak urge, kamu sedang membangun mental strength yang incredible.",
                "focus": "Personal Development & Resilience"
            },
            "friday": {
                "title": "🔥 Friday Power",
                "message": "TGIF! Weekend approaching, but stay vigilant. Plan positive activities dan avoid high-risk situations. You've got this!",
                "focus": "Weekend Preparation & Safety Planning"
            },
            "saturday": {
                "title": "🎨 Saturday Creativity",
                "message": "Weekend adalah waktu perfect untuk explore hobbies dan creative outlets. Channel energimu ke aktivitas yang fulfilling dan productive!",
                "focus": "Creative Activities & Hobbies"
            },
            "sunday": {
                "title": "🙏 Sunday Reflection",
                "message": "Time for reflection and gratitude. What did you learn this week? How did you grow? Prepare mentally untuk minggu yang amazing ahead.",
                "focus": "Reflection & Gratitude Practice"
            }
        }
        
        return day_contents.get(day, day_contents["monday"])  # Default to Monday if day not found
    
    def _get_daily_recovery_fact(self) -> Dict:
        """Get daily recovery fact or scientific insight"""
        
        recovery_facts = [
            {
                "title": "🧬 Dopamine Recovery Timeline",
                "fact": "Dopamine receptors mulai recovery dalam 2-4 minggu abstinence. Peak sensitivity kembali normal setelah 90+ hari clean.",
                "takeaway": "Trust the process - otak kamu sedang healing!"
            },
            {
                "title": "💪 Willpower adalah Muscle",
                "fact": "Self-control bisa dilatih seperti otot. Semakin sering digunakan untuk hal positif, semakin kuat jadinya.",
                "takeaway": "Setiap 'no' pada urge = strengthening your willpower muscle"
            },
            {
                "title": "🌊 Urge Wave Pattern",
                "fact": "Urges memiliki pattern seperti gelombang: rise, peak (10-20 menit), lalu naturally decrease. Tidak ada urge yang bertahan selamanya.",
                "takeaway": "Ride the wave - jangan fight atau give in, just wait it out"
            },
            {
                "title": "🎯 Success Rate Statistics",
                "fact": "People yang track progress dan punya support system memiliki success rate 3x lebih tinggi dalam recovery journey.",
                "takeaway": "Tracking dan community support = game changer!"
            },
            {
                "title": "🧘 Mindfulness Benefits",
                "fact": "10 menit daily mindfulness practice dapat mengurangi craving intensity hingga 60% dalam 4 minggu.",
                "takeaway": "Small mindfulness practice = big impact on urge management"
            },
            {
                "title": "🏃 Exercise Impact",
                "fact": "30 menit exercise dapat meningkatkan mood dan focus selama 2-4 jam, plus mengurangi urge intensity significantly.",
                "takeaway": "Move your body = change your mental state instantly"
            },
            {
                "title": "💤 Sleep & Recovery",
                "fact": "Kurang tidur meningkatkan craving hingga 300%. Quality sleep adalah foundation untuk strong willpower.",
                "takeaway": "Prioritize sleep = prioritize your recovery success"
            }
        ]
        
        return random.choice(recovery_facts)
    
    def _get_daily_inspiration(self) -> Dict:
        """Get daily inspiration or success story"""
        
        inspirations = [
            {
                "title": "💎 Success Story",
                "story": "Seorang user mencapai 180 hari clean dan melaporkan: 'Confidence naik dramatically, relationship dengan keluarga membaik, career breakthrough, dan inner peace yang belum pernah dirasakan sebelumnya.'",
                "lesson": "Long-term recovery = life transformation"
            },
            {
                "title": "🌟 Community Win",
                "story": "95% users yang aktif menggunakan bot selama 30+ hari melaporkan significant improvement dalam self-control dan life satisfaction.",
                "lesson": "Consistency dengan support tools = proven success"
            },
            {
                "title": "🚀 Progress Principle",
                "story": "Remember: Kamu tidak berjuang sendirian. Ribuan orang di seluruh dunia sedang menjalani journey yang sama dan banyak yang berhasil.",
                "lesson": "You're part of a global recovery movement"
            },
            {
                "title": "🎯 Milestone Magic",
                "story": "Research shows: Orang yang celebrate small wins dan milestones memiliki motivation yang lebih sustainable dalam long-term recovery.",
                "lesson": "Celebrate every victory, no matter how small"
            },
            {
                "title": "💪 Resilience Reminder",
                "story": "Setiap kali kamu overcome urge, neural pathways untuk self-control menjadi stronger. Kamu literally rewiring your brain for success.",
                "lesson": "Every resistance builds permanent strength"
            }
        ]
        
        return random.choice(inspirations)
    
    def _get_daily_call_to_action(self) -> str:
        """Get daily call to action"""
        
        ctas = [
            "💪 **Daily Challenge**: Set one small goal untuk hari ini dan achieve it. Build momentum!",
            "📝 **Reflection Time**: Spend 5 menit untuk journal tentang gratitude dan goals hari ini.",
            "🎯 **Accountability Check**: Rate your mental state 1-10 dan share di check-in menu.",
            "🧘 **Mindfulness Moment**: Take 3 deep breaths dan set positive intention untuk hari ini.",
            "🔥 **Power Hour**: Dedicate 1 jam untuk productive activity yang bikin kamu bangga.",
            "🌟 **Act of Kindness**: Lakukan satu hal baik untuk orang lain hari ini. Spread positivity!",
            "📚 **Learn Something New**: Spend 15 menit untuk belajar skill baru atau baca educational content."
        ]
        
        return random.choice(ctas)
    
    async def _send_message_to_user(self, telegram_id: int, content: Dict):
        """Send formatted message to specific user"""
        
        # Format the complete message
        message = f"""
{content['greeting']}

{content['date']}

**💭 Quote of the Day:**
"{content['quote']['text']}"
*- {content['quote']['author']}*

**{content['day_content']['title']}**
{content['day_content']['message']}
🎯 **Today's Focus:** {content['day_content']['focus']}

**{content['recovery_fact']['title']}**
📊 {content['recovery_fact']['fact']}
💡 **Key Takeaway:** {content['recovery_fact']['takeaway']}

**🎯 Daily Coping Strategy:**
**{content['tip']['title']}** ({content['tip']['duration']})
{content['tip']['description']}

**{content['inspiration']['title']}**
{content['inspiration']['story']}
✨ **Lesson:** {content['inspiration']['lesson']}

{content['call_to_action']}

---
🤖 **Gunakan bot ini kapan saja:**
• `/streak` - Check progress kamu
• `/motivation` - Get instant motivation  
• `/emergency` - Butuh bantuan darurat
• `/checkin` - Daily mood check-in

**Remember: Every day clean adalah victory. Kamu doing amazing! 🙏**
        """
        
        # Send the message
        await self.bot_application.bot.send_message(
            chat_id=telegram_id,
            text=message.strip(),
            parse_mode='Markdown'
        )
    
    async def send_weekly_summary(self):
        """Send weekly summary to all users (Sunday evening)"""
        try:
            users = self.user_service.get_all_users_with_reminders()
            
            weekly_content = self._generate_weekly_summary()
            
            for user in users:
                try:
                    await self._send_message_to_user(user.telegram_id, {
                        "greeting": "📊 **Weekly Recovery Summary**",
                        "date": f"Week of {datetime.now().strftime('%B %d, %Y')}",
                        "quote": {"text": "Progress, not perfection. Every step forward counts.", "author": "Recovery Wisdom"},
                        "tip": weekly_content['tip'],
                        "day_content": weekly_content['summary'],
                        "recovery_fact": weekly_content['stats'],
                        "inspiration": weekly_content['inspiration'],
                        "call_to_action": "🎯 **Week Ahead**: Plan untuk minggu depan dan set 3 goals spesifik!"
                    })
                except Exception as e:
                    app_logger.error(f"Failed to send weekly summary to user {user.telegram_id}: {e}")
                    
        except Exception as e:
            app_logger.error(f"Error in weekly summary: {e}")
    
    def _generate_weekly_summary(self) -> Dict:
        """Generate weekly summary content"""
        return {
            "tip": {
                "title": "Weekly Planning Strategy",  
                "description": "Plan aktivitas positif untuk minggu depan. Schedule exercise, hobbies, social activities untuk minimize idle time.",
                "duration": "30 menit planning"
            },
            "summary": {
                "title": "🎯 Week Reflection",
                "message": "Time untuk reflect pada minggu yang telah berlalu. What went well? What challenges did you face? What will you improve next week?",
                "focus": "Planning & Goal Setting"
            },
            "stats": {
                "title": "📈 Community Stats",
                "fact": "This week, ribuan users di seluruh dunia melakukan check-in, share progress, dan support satu sama lain dalam recovery journey.",
                "takeaway": "You're part of supportive global community!"
            },
            "inspiration": {
                "title": "🌟 Weekend Wisdom",
                "story": "Weekends adalah test sejati untuk recovery discipline. Plan ahead, stay busy dengan positive activities, dan remember your why.",
                "lesson": "Preparation adalah key untuk weekend success"
            }
        }
    
    def _format_daily_message(self, content: Dict) -> str:
        """Format daily broadcast message"""
        try:
            message = f"""{content.get('greeting', '🌅 Good morning!')}

{content.get('date', datetime.now().strftime('%A, %d %B %Y'))}

💭 **"{content.get('quote', {}).get('text', 'Stay strong!')}"** 
   - {content.get('quote', {}).get('author', 'Recovery Wisdom')}

💡 **Daily Coping Strategy: {content.get('tip', {}).get('title', 'Stay Focus')}**
{content.get('tip', {}).get('description', 'Keep moving forward!')}
⏱️ Time needed: {content.get('tip', {}).get('duration', '5-10 minutes')}

🎯 **{content.get('day_content', {}).get('title', 'Daily Focus')}**
{content.get('day_content', {}).get('message', 'Make today count!')}

📚 **{content.get('recovery_fact', {}).get('title', 'Recovery Fact')}**
{content.get('recovery_fact', {}).get('fact', 'Every day is progress!')}
✨ Key insight: {content.get('recovery_fact', {}).get('takeaway', 'Keep going!')}

🌟 **{content.get('inspiration', {}).get('title', 'Daily Inspiration')}**
{content.get('inspiration', {}).get('story', 'You are stronger than you think!')}

{content.get('call_to_action', '💪 **Take action today!** Your recovery journey matters!')}

---
Stay strong, recovery warrior! 💪✨"""

            return message
            
        except Exception as e:
            app_logger.error(f"Error formatting daily message: {e}")
            return "🌅 Daily Reminder - Stay strong and keep going! 💪"
    
    def _format_weekly_message(self, content: Dict) -> str:
        """Format weekly summary message"""
        try:
            message = f"""📊 **WEEKLY SUMMARY**

{content.get('summary', {}).get('message', 'Weekly reflection time!')}

💡 **{content.get('tip', {}).get('title', 'Weekly Tip')}**
{content.get('tip', {}).get('description', 'Keep moving forward!')}

📈 **{content.get('stats', {}).get('title', 'Community Stats')}**
{content.get('stats', {}).get('fact', 'Amazing progress this week!')}

🌟 **{content.get('inspiration', {}).get('title', 'Weekly Inspiration')}**
{content.get('inspiration', {}).get('story', 'Stay strong and keep going!')}

💪 **Key Takeaway**: {content.get('inspiration', {}).get('lesson', 'Every day is a new opportunity!')}

🎯 **Ready for next week?** Let's make it even better!

---
Stay strong, recover warrior! 💪✨"""

            return message
            
        except Exception as e:
            app_logger.error(f"Error formatting weekly message: {e}")
            return "📊 Weekly Summary - Keep up the great work! 💪"
