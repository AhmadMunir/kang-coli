from telegram import Update
from telegram.ext import ContextTypes
from config.settings import settings
from src.services import BroadcastService, SchedulerService
from src.utils.logger import app_logger

class AdminHandlers:
    """Handler untuk admin commands"""
    
    def __init__(self, scheduler_service: SchedulerService = None):
        self.broadcast_service = BroadcastService()
        self.scheduler_service = scheduler_service
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        admin_id = settings.ADMIN_USER_ID
        if not admin_id:
            return False
        return str(user_id) == str(admin_id)
    
    async def broadcast_now_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send immediate broadcast to all users - ADMIN ONLY"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        try:
            await self.broadcast_service.send_daily_broadcast()
            await update.message.reply_text("✅ Daily broadcast sent to all users!")
        except Exception as e:
            app_logger.error(f"Broadcast error: {e}")
            await update.message.reply_text(f"❌ Broadcast failed: {str(e)}")
    
    async def broadcast_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show broadcast statistics - ADMIN ONLY"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        try:
            from src.services import UserService
            user_service = UserService()
            
            # Get user statistics
            total_users = len(user_service.get_all_users_with_reminders())
            
            # Get scheduler info
            jobs = []
            if self.scheduler_service:
                jobs = self.scheduler_service.list_scheduled_jobs()
            
            stats_message = f"""
📊 **Broadcast Statistics**

👥 **Users with Daily Reminders:** {total_users}

⏰ **Scheduled Jobs:**
"""
            
            for job in jobs:
                stats_message += f"• **{job['name']}** (ID: {job['id']})\n"
                stats_message += f"  Next run: {job['next_run']}\n\n"
            
            if not jobs:
                stats_message += "No scheduled jobs found.\n"
            
            await update.message.reply_text(stats_message, parse_mode='Markdown')
            
        except Exception as e:
            app_logger.error(f"Stats error: {e}")
            await update.message.reply_text(f"❌ Error getting stats: {str(e)}")
    
    async def custom_broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send custom broadcast message - ADMIN ONLY"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        # Check if message provided
        if not context.args:
            await update.message.reply_text(
                "Usage: /custombroadcast <message>\n\n"
                "Example: /custombroadcast **Special Announcement** Important update for all users!"
            )
            return
        
        try:
            # Join all arguments as message
            custom_message = " ".join(context.args)
            
            # Send to all users
            from src.services import UserService
            user_service = UserService()
            users = user_service.get_all_users_with_reminders()
            
            sent_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"📢 **Admin Announcement**\n\n{custom_message}",
                        parse_mode='Markdown'
                    )
                    sent_count += 1
                except Exception as e:
                    failed_count += 1
                    app_logger.error(f"Failed to send to user {user.telegram_id}: {e}")
            
            await update.message.reply_text(
                f"✅ Custom broadcast sent!\n"
                f"📤 Sent: {sent_count}\n"
                f"❌ Failed: {failed_count}"
            )
            
        except Exception as e:
            app_logger.error(f"Custom broadcast error: {e}")
            await update.message.reply_text(f"❌ Broadcast failed: {str(e)}")
    
    async def test_broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send test broadcast to admin only"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        try:
            # Generate test content
            test_content = {
                "greeting": "🧪 **TEST BROADCAST**",
                "date": "This is a test message",
                "quote": {"text": "Testing is the key to reliable software.", "author": "Developer Wisdom"},
                "tip": {
                    "title": "Test Coping Strategy",
                    "description": "This is a test description for coping strategy.",
                    "duration": "Test duration"
                },
                "day_content": {
                    "title": "Test Day Content",
                    "message": "This is test day-specific content.",
                    "focus": "Testing & Debugging"
                },
                "recovery_fact": {
                    "title": "Test Recovery Fact",
                    "fact": "This is a test recovery fact.",
                    "takeaway": "Testing is important!"
                },
                "inspiration": {
                    "title": "Test Inspiration",
                    "story": "This is a test inspirational story.",
                    "lesson": "Always test your code!"
                },
                "call_to_action": "🧪 **Test Action**: This is a test call to action."
            }
            
            # Send test message to admin
            await self.broadcast_service._send_message_to_user(
                update.effective_user.id, 
                test_content
            )
            
            await update.message.reply_text("✅ Test broadcast sent to you!")
            
        except Exception as e:
            app_logger.error(f"Test broadcast error: {e}")
            await update.message.reply_text(f"❌ Test failed: {str(e)}")
    
    async def weekly_summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send weekly summary immediately - ADMIN ONLY"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        try:
            await self.broadcast_service.send_weekly_summary()
            await update.message.reply_text("✅ Weekly summary sent to all users!")
        except Exception as e:
            app_logger.error(f"Weekly summary error: {e}")
            await update.message.reply_text(f"❌ Weekly summary failed: {str(e)}")
    
    async def admin_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin commands help"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        help_message = """
🔧 **Admin Commands**

**Broadcast Management:**
/broadcastnow - Send daily broadcast immediately
/custombroadcast <message> - Send custom message to all users
/testbroadcast - Send test broadcast to admin only
/weeklysummary - Send weekly summary immediately

**Statistics & Monitoring:**
/broadcaststats - Show broadcast statistics
/adminstats - Show detailed admin statistics

**System Commands:**
/adminhelp - Show this help message

**Usage Examples:**
• `/custombroadcast **Emergency Notice** Bot will be down for maintenance in 1 hour`
• `/broadcastnow` - Sends today's daily broadcast
• `/testbroadcast` - Test broadcast format

**Note:** All admin commands require proper authentication.
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def admin_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed admin statistics"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Unauthorized. Admin access required.")
            return
        
        try:
            from src.services import UserService, StreakService
            from src.database.models import User, RelapseRecord
            from src.database.database import db
            from sqlalchemy import func
            from datetime import datetime, timedelta
            
            session = db.get_session()
            
            try:
                # User statistics
                total_users = session.query(User).count()
                users_with_reminders = session.query(User).filter(User.daily_reminders == True).count()
                
                # Active users (users who interacted in last 7 days)
                week_ago = datetime.utcnow() - timedelta(days=7)
                active_users = session.query(User).filter(User.updated_at >= week_ago).count()
                
                # Streak statistics
                avg_current_streak = session.query(func.avg(User.current_streak)).scalar() or 0
                max_streak = session.query(func.max(User.longest_streak)).scalar() or 0
                
                # Relapse statistics
                total_relapses = session.query(RelapseRecord).count()
                relapses_this_week = session.query(RelapseRecord).filter(
                    RelapseRecord.created_at >= week_ago
                ).count()
                
                stats_message = f"""
📈 **Detailed Admin Statistics**

**👥 User Statistics:**
• Total Users: {total_users}
• Users with Daily Reminders: {users_with_reminders}
• Active Users (7 days): {active_users}
• Reminder Engagement: {(users_with_reminders/total_users*100) if total_users > 0 else 0:.1f}%

**🔥 Streak Statistics:**
• Average Current Streak: {avg_current_streak:.1f} days
• Highest Streak Ever: {max_streak} days
• Users with 30+ day streaks: {session.query(User).filter(User.current_streak >= 30).count()}
• Users with 90+ day streaks: {session.query(User).filter(User.current_streak >= 90).count()}

**📊 Recovery Statistics:**
• Total Relapses Recorded: {total_relapses}
• Relapses This Week: {relapses_this_week}
• Average Relapses per User: {(total_relapses/total_users) if total_users > 0 else 0:.1f}

**🤖 System Info:**
• Bot Uptime: Running
• Database Status: Connected
• Scheduler Status: Active
• Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                await update.message.reply_text(stats_message, parse_mode='Markdown')
                
            finally:
                db.close_session(session)
                
        except Exception as e:
            app_logger.error(f"Admin stats error: {e}")
            await update.message.reply_text(f"❌ Error getting admin stats: {str(e)}")
