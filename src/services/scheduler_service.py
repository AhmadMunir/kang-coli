import asyncio
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.settings import settings
from src.services.broadcast_service import BroadcastService
from src.utils.logger import app_logger

class SchedulerService:
    """Service untuk mengatur jadwal broadcast dan task otomatis"""
    
    def __init__(self, bot_application=None):
        self.scheduler = AsyncIOScheduler()
        self.broadcast_service = BroadcastService(bot_application)
        self.bot_application = bot_application
        
    def start_scheduler(self):
        """Start the scheduler dengan semua scheduled tasks"""
        try:
            # Daily broadcast - setiap hari jam yang ditentukan di settings
            reminder_time = settings.DAILY_REMINDER_TIME.split(':')
            hour = int(reminder_time[0])
            minute = int(reminder_time[1])
            
            # Daily morning broadcast
            self.scheduler.add_job(
                func=self.broadcast_service.send_daily_broadcast,
                trigger=CronTrigger(hour=hour, minute=minute),
                id='daily_broadcast',
                name='Daily Morning Broadcast',
                misfire_grace_time=3600  # 1 hour grace time
            )
            
            # Weekly summary - setiap Minggu jam 18:00
            self.scheduler.add_job(
                func=self.broadcast_service.send_weekly_summary,
                trigger=CronTrigger(day_of_week='sun', hour=18, minute=0),
                id='weekly_summary',
                name='Weekly Summary Broadcast',
                misfire_grace_time=3600
            )
            
            # Motivational boost - setiap hari jam 15:00 (afternoon motivation)
            self.scheduler.add_job(
                func=self._send_afternoon_boost,
                trigger=CronTrigger(hour=15, minute=0),
                id='afternoon_boost',
                name='Afternoon Motivation Boost',
                misfire_grace_time=1800  # 30 minutes grace time
            )
            
            # Evening reflection - setiap hari jam 20:00
            self.scheduler.add_job(
                func=self._send_evening_reflection,
                trigger=CronTrigger(hour=20, minute=0),
                id='evening_reflection',
                name='Evening Reflection',
                misfire_grace_time=1800
            )
            
            # Start the scheduler
            self.scheduler.start()
            app_logger.info("Scheduler started successfully with all broadcast tasks")
            
        except Exception as e:
            app_logger.error(f"Failed to start scheduler: {e}")
            raise
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown()
            app_logger.info("Scheduler stopped successfully")
        except Exception as e:
            app_logger.error(f"Error stopping scheduler: {e}")
    
    async def _send_afternoon_boost(self):
        """Send afternoon motivation boost to active users"""
        try:
            from src.services import UserService
            user_service = UserService()
            users = user_service.get_all_users_with_reminders()
            
            boost_message = self._generate_afternoon_boost()
            
            sent_count = 0
            for user in users:
                try:
                    await self.bot_application.bot.send_message(
                        chat_id=user.telegram_id,
                        text=boost_message,
                        parse_mode='Markdown'
                    )
                    sent_count += 1
                except Exception as e:
                    app_logger.error(f"Failed to send afternoon boost to {user.telegram_id}: {e}")
            
            app_logger.info(f"Afternoon boost sent to {sent_count} users")
            
        except Exception as e:
            app_logger.error(f"Error in afternoon boost: {e}")
    
    async def _send_evening_reflection(self):
        """Send evening reflection prompt to users"""
        try:
            from src.services import UserService
            user_service = UserService()
            users = user_service.get_all_users_with_reminders()
            
            reflection_message = self._generate_evening_reflection()
            
            sent_count = 0
            for user in users:
                try:
                    await self.bot_application.bot.send_message(
                        chat_id=user.telegram_id,
                        text=reflection_message,
                        parse_mode='Markdown'
                    )
                    sent_count += 1
                except Exception as e:
                    app_logger.error(f"Failed to send evening reflection to {user.telegram_id}: {e}")
            
            app_logger.info(f"Evening reflection sent to {sent_count} users")
            
        except Exception as e:
            app_logger.error(f"Error in evening reflection: {e}")
    
    def _generate_afternoon_boost(self) -> str:
        """Generate afternoon motivation boost message"""
        import random
        
        boost_messages = [
            """
⚡ **Afternoon Power Boost!** ⚡

Tengah hari adalah waktu critical - energy mulai drop, focus menurun. Perfect time untuk small wins!

🎯 **Quick Wins (pilih satu):**
• 10 push-ups atau stretching
• Minum segelas air dan deep breathing
• Write down 3 things you're grateful for
• Send encouraging message ke teman
• Clean up workspace/surroundings

💪 **Afternoon Affirmation:**
"I am in control of my choices. I choose progress over pleasure, growth over instant gratification."

Keep pushing forward! Sore ini akan jadi productive! 🔥
            """,
            
            """
🌅 **Midday Check-in!** 🌅

How's your day going so far? Remember: setiap moment adalah opportunity untuk make good choices.

🧠 **Mental Health Reminder:**
• Progress > Perfection
• You're stronger than your urges
• This too shall pass
• Focus on the next right choice

🎯 **Afternoon Challenge:**
Do something that your future self will thank you for. Could be learning, exercise, organizing, atau connecting with loved ones.

You've got this, warrior! 💪
            """,
            
            """
🔋 **Energy Recharge Time!** 🔋

Feeling low energy? That's normal! Here's how to naturally boost your afternoon:

✨ **Natural Energy Boosters:**
• 5-minute walk outside (sunlight + movement)
• Drink cold water + lemon
• Listen to upbeat music
• Do breathing exercise (4-7-8 technique)
• Laugh! Watch funny video atau chat with friend

🎯 **Reminder:** Urges often peak when energy is low. Keep yourself energized and busy!

Stay strong! Evening akan datang dengan sense of accomplishment! 🌟
            """
        ]
        
        return random.choice(boost_messages).strip()
    
    def _generate_evening_reflection(self) -> str:
        """Generate evening reflection message"""
        import random
        
        reflection_messages = [
            """
🌙 **Evening Reflection Time** 🌙

Day is winding down. Perfect time untuk reflect dan prepare untuk tomorrow.

🤔 **Today's Reflection Questions:**
• What went well today?
• What challenge did you overcome?
• How did you grow as a person?
• What are you grateful for?

📝 **Tomorrow's Intention:**
Set satu specific goal untuk besok. Could be:
• Exercise routine
• Learning something new  
• Connecting with someone important
• Creative project

💤 **Sleep Well Reminder:**
Quality sleep = strong willpower tomorrow. Create calming bedtime routine.

Good night, recovery warrior! Tomorrow is another opportunity to shine! ✨
            """,
            
            """
🕯️ **Day's End Gratitude** 🕯️

Another day of recovery journey completed. Every day clean adalah victory worth celebrating!

🙏 **Gratitude Practice:**
Think of 3 things you're grateful for today:
1. One person who made your day better
2. One moment that brought you joy  
3. One achievement (however small)

💪 **Strength Recognition:**
Acknowledge every time today you:
• Made a healthy choice
• Resisted temptation
• Helped someone else
• Learned something new

🌟 **Tomorrow's Promise:**
"Tomorrow I will continue my journey of growth, one choice at a time."

Rest well, champion! 😴
            """,
            
            """
🌆 **Sunset Wisdom** 🌆

As the day ends, remember: progress isn't always linear, but every day you try is a day you succeed.

📊 **Day Assessment (rate 1-10):**
• How was your mental state?
• How well did you handle stress?
• Did you stick to healthy habits?
• How connected did you feel with others?

🎯 **Tomorrow's Game Plan:**
• One thing to continue doing
• One thing to improve
• One new thing to try

💙 **Self-Compassion:**
Be kind to yourself. Recovery is marathon, not sprint. You're doing better than you think.

Sweet dreams, and tomorrow we rise stronger! 🌅
            """
        ]
        
        return random.choice(reflection_messages).strip()
    
    def add_custom_broadcast(self, cron_expression: str, message: str, job_id: str):
        """Add custom scheduled broadcast"""
        try:
            # Parse cron expression dan add job
            self.scheduler.add_job(
                func=self._send_custom_broadcast,
                trigger=CronTrigger.from_crontab(cron_expression),
                args=[message],
                id=job_id,
                name=f'Custom Broadcast: {job_id}',
                misfire_grace_time=1800
            )
            
            app_logger.info(f"Custom broadcast added: {job_id}")
            
        except Exception as e:
            app_logger.error(f"Failed to add custom broadcast: {e}")
            raise
    
    async def _send_custom_broadcast(self, message: str):
        """Send custom broadcast message"""
        try:
            from src.services import UserService
            user_service = UserService()
            users = user_service.get_all_users_with_reminders()
            
            sent_count = 0
            for user in users:
                try:
                    await self.bot_application.bot.send_message(
                        chat_id=user.telegram_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    sent_count += 1
                except Exception as e:
                    app_logger.error(f"Failed to send custom broadcast to {user.telegram_id}: {e}")
            
            app_logger.info(f"Custom broadcast sent to {sent_count} users")
            
        except Exception as e:
            app_logger.error(f"Error in custom broadcast: {e}")
    
    def list_scheduled_jobs(self) -> list:
        """Get list of all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time,
                'trigger': str(job.trigger)
            })
        return jobs
