"""
Mood Check-in Handlers for PMO Recovery Bot
Handles daily mood tracking and check-in functionality
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import json

from ...services.user_service import UserService
from ...database.models import MoodEntry
from ...bot.keyboards.inline_keyboards import BotKeyboards
from ...utils.logger import app_logger

logger = app_logger

class MoodCheckInHandlers:
    """Handlers for mood check-in functionality"""
    
    def __init__(self):
        self.user_service = UserService()
    
    async def handle_mood_checkin_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start mood check-in process"""
        user_id = update.effective_user.id
        
        # Check if already checked in today
        if self.user_service.has_checked_in_today(user_id):
            await update.callback_query.edit_message_text(
                "✅ **Kamu sudah check-in hari ini!**\n\n"
                "Terima kasih sudah konsisten tracking mood. "
                "Check-in berikutnya tersedia besok.\n\n"
                "💡 **Tip:** Consistency adalah kunci untuk memahami pattern mood dan recovery progress-mu!",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
                ]]),
                parse_mode='Markdown'
            )
            return
        
        # Show mood selection
        message = (
            "🌡️ **Daily Mood Check-in**\n\n"
            "Bagaimana perasaanmu hari ini? Rating mood-mu dari 1-10:\n\n"
            "1-3: Challenging day 😞\n"
            "4-5: Neutral/OK 😐\n"
            "6-7: Good day 😊\n"
            "8-10: Excellent day! 🌟\n\n"
            "Tracking mood membantu kamu understand pattern dan trigger recovery."
        )
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=BotKeyboards.mood_checkin_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_mood_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle mood score selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        # Extract mood score from callback data
        mood_score = int(query.data.split('_')[1])
        
        # Store mood score in context for later use
        context.user_data['current_mood_score'] = mood_score
        context.user_data['mood_checkin_started'] = datetime.now()
        
        # Get mood emoji and description
        mood_info = self._get_mood_info(mood_score)
        
        message = (
            f"✅ **Mood tercatat: {mood_score}/10** {mood_info['emoji']}\n\n"
            f"**{mood_info['description']}**\n\n"
            f"{mood_info['message']}\n\n"
            "Ingin menambahkan detail lain untuk tracking yang lebih komprehensif?"
        )
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.mood_details_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_quick_mood_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle quick mood response from broadcast"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        # Extract mood score from callback data
        mood_score = int(query.data.split('_')[2])
        
        # Record mood check-in
        success = self.user_service.record_mood_checkin(user_id, mood_score)
        
        if success:
            mood_info = self._get_mood_info(mood_score)
            message = (
                f"✅ **Quick Check-in Berhasil!**\n\n"
                f"Mood hari ini: {mood_score}/10 {mood_info['emoji']}\n"
                f"**{mood_info['description']}**\n\n"
                f"{mood_info['quick_tip']}\n\n"
                "Terima kasih sudah check-in! Consistency is key untuk recovery success! 💪"
            )
            
            keyboard = [[
                InlineKeyboardButton("📊 Lihat Progress", callback_data="view_mood_progress"),
                InlineKeyboardButton("🎯 Daily Goals", callback_data="daily_goals")
            ]]
        else:
            message = "❌ Gagal menyimpan check-in. Silakan coba lagi."
            keyboard = [[
                InlineKeyboardButton("🔄 Coba Lagi", callback_data="daily_checkin")
            ]]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_detailed_checkin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle request for detailed check-in"""
        message = (
            "📝 **Detail Check-in**\n\n"
            "Bagaimana perasaanmu hari ini? Mari kita lakukan check-in yang lebih detail "
            "untuk tracking yang optimal.\n\n"
            "Rating mood-mu dari 1-10:"
        )
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=BotKeyboards.mood_checkin_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_skip_mood_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle skip mood check-in for today"""
        message = (
            "⏭️ **Check-in Di-skip untuk Hari Ini**\n\n"
            "No worries! Kamu bisa check-in kapan saja ketika siap.\n\n"
            "💡 **Remember:** Regular mood tracking membantu kamu understand pattern "
            "dan identify trigger lebih baik.\n\n"
            "Streak kamu tetap berjalan selama tidak ada relapse! 💪"
        )
        
        keyboard = [[
            InlineKeyboardButton("📊 Cek Streak", callback_data="check_streak"),
            InlineKeyboardButton("💪 Motivasi", callback_data="get_motivation")
        ]]
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_finish_checkin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Finish mood check-in process"""
        user_id = update.effective_user.id
        mood_score = context.user_data.get('current_mood_score')
        
        if not mood_score:
            await update.callback_query.answer("❌ Error: Mood score tidak ditemukan")
            return
        
        # Get additional data if available
        energy_level = context.user_data.get('energy_level')
        stress_level = context.user_data.get('stress_level')
        sleep_quality = context.user_data.get('sleep_quality')
        urge_intensity = context.user_data.get('urge_intensity')
        notes = context.user_data.get('mood_notes', '')
        
        # Record comprehensive mood check-in
        success = self._record_detailed_mood_checkin(
            user_id, mood_score, energy_level, stress_level, 
            sleep_quality, urge_intensity, notes
        )
        
        if success:
            mood_info = self._get_mood_info(mood_score)
            
            # Create summary message
            summary_parts = [
                f"✅ **Check-in Berhasil Disimpan!**\n",
                f"📅 **Tanggal:** {datetime.now().strftime('%d %B %Y')}",
                f"🌡️ **Mood:** {mood_score}/10 {mood_info['emoji']}",
            ]
            
            if energy_level:
                summary_parts.append(f"⚡ **Energy:** {energy_level}/10")
            if stress_level:
                summary_parts.append(f"😰 **Stress:** {stress_level}/10")
            if sleep_quality:
                summary_parts.append(f"😴 **Sleep:** {sleep_quality}/10")
            if urge_intensity:
                summary_parts.append(f"🔥 **Urges:** {urge_intensity}/10")
            if notes:
                summary_parts.append(f"📝 **Notes:** {notes}")
            
            summary_parts.extend([
                f"\n**{mood_info['description']}**",
                f"{mood_info['message']}",
                "\n💪 **Keep it up!** Consistency dalam tracking = clarity dalam recovery!"
            ])
            
            message = "\n".join(summary_parts)
            
            keyboard = [[
                InlineKeyboardButton("📊 Mood Trends", callback_data="view_mood_trends"),
                InlineKeyboardButton("🎯 Set Goals", callback_data="daily_goals")
            ], [
                InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")
            ]]
        else:
            message = "❌ Gagal menyimpan check-in. Silakan coba lagi."
            keyboard = [[
                InlineKeyboardButton("🔄 Coba Lagi", callback_data="daily_checkin")
            ]]
        
        # Clear context data
        context.user_data.clear()
        
        await update.callback_query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    def _get_mood_info(self, mood_score: int) -> dict:
        """Get mood information based on score"""
        mood_data = {
            1: {
                "emoji": "😢",
                "description": "Sangat Challenging",
                "message": "Hari yang berat, tapi kamu masih di sini dan itu sudah luar biasa strong! 💪",
                "quick_tip": "🛡️ Focus pada satu small win hari ini. Every moment survived adalah victory!"
            },
            2: {
                "emoji": "😞", 
                "description": "Hari yang Sulit",
                "message": "Feeling down itu normal dalam recovery journey. Kamu tidak sendirian! 🤗",
                "quick_tip": "🌱 Try 5-minute breathing exercise atau short walk untuk mood boost."
            },
            3: {
                "emoji": "😕",
                "description": "Kurang Optimal",
                "message": "Ups and downs adalah bagian dari healing. Patience dengan diri sendiri ya! 🌈",
                "quick_tip": "💡 Connect dengan support system atau lakukan activity yang biasanya bikin happy."
            },
            4: {
                "emoji": "😐",
                "description": "Biasa Saja",
                "message": "Neutral day adalah progress juga! Stability adalah foundation yang strong. 🏗️",
                "quick_tip": "⚡ Perfect time untuk small productive activities atau self-care."
            },
            5: {
                "emoji": "🙂",
                "description": "Netral-Positif",
                "message": "Balanced feeling! Ini adalah sweet spot untuk building positive momentum. 📈",
                "quick_tip": "🎯 Channel this stable energy untuk plan atau achieve small goals."
            },
            6: {
                "emoji": "😊",
                "description": "Lumayan Baik",
                "message": "Good vibes! Kamu ada di track yang benar. Keep this positive energy flowing! ✨",
                "quick_tip": "🌟 Share positivity dengan orang lain atau tackle challenges dengan confidence ini."
            },
            7: {
                "emoji": "😄",
                "description": "Hari yang Baik",
                "message": "Excellent mood! Recovery progress kamu terasa ya. Celebrate this feeling! 🎉",
                "quick_tip": "🚀 Perfect time untuk push boundaries atau try something new dan positive."
            },
            8: {
                "emoji": "😁",
                "description": "Sangat Baik",
                "message": "Amazing energy! Ini adalah reward dari consistency dan hard work kamu! 🏆",
                "quick_tip": "💫 Use this peak state untuk inspiration dan motivate others dalam journey mereka."
            },
            9: {
                "emoji": "🤩",
                "description": "Luar Biasa",
                "message": "Outstanding day! Kamu experience natural high dari healthy living. This is the goal! 🎯",
                "quick_tip": "🌈 Document this feeling dan remember what got you here untuk replicate di future."
            },
            10: {
                "emoji": "🌟",
                "description": "Perfect Day",
                "message": "Absolutely incredible! Ini adalah peak recovery state - clarity, joy, purpose! 💎",
                "quick_tip": "✨ Treasure this moment dan use energy ini untuk inspire dan help others."
            }
        }
        
        return mood_data.get(mood_score, mood_data[5])  # Default to neutral if invalid score
    
    def _record_detailed_mood_checkin(self, user_id: int, mood_score: int, 
                                    energy_level: int = None, stress_level: int = None,
                                    sleep_quality: int = None, urge_intensity: int = None,
                                    notes: str = None) -> bool:
        """Record detailed mood check-in to database"""
        try:
            from ...database.database import db
            
            session = db.get_session()
            try:
                # Check if already checked in today
                today = datetime.now().date()
                existing_entry = session.query(MoodEntry).filter(
                    MoodEntry.user_id == user_id,
                    MoodEntry.created_at >= datetime.combine(today, datetime.min.time()),
                    MoodEntry.created_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
                ).first()
                
                if existing_entry:
                    # Update existing entry
                    existing_entry.mood_score = mood_score
                    existing_entry.energy_level = energy_level
                    existing_entry.stress_level = stress_level
                    existing_entry.sleep_quality = sleep_quality
                    existing_entry.urge_intensity = urge_intensity
                    existing_entry.notes = notes
                    existing_entry.updated_at = datetime.utcnow()
                else:
                    # Create new entry
                    mood_entry = MoodEntry(
                        user_id=user_id,
                        mood_score=mood_score,
                        energy_level=energy_level,
                        stress_level=stress_level,
                        sleep_quality=sleep_quality,
                        urge_intensity=urge_intensity,
                        notes=notes
                    )
                    session.add(mood_entry)
                
                session.commit()
                return True
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Error recording detailed mood check-in for user {user_id}: {e}")
            return False

# Global instance
mood_checkin_handlers = MoodCheckInHandlers()
