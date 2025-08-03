from telegram import Update
from telegram.ext import ContextTypes
from src.services import UserService, JournalService
from src.utils.helpers import get_user_info
from src.utils.logger import app_logger
from datetime import datetime

class MessageHandlers:
    """Handler untuk text messages"""
    
    def __init__(self):
        self.user_service = UserService()
        self.journal_service = JournalService()
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages based on user state"""
        
        user_info = get_user_info(update.effective_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        # Check if user is in journal writing mode
        user_state = context.user_data.get('state')
        journal_step = context.user_data.get('journal_step')
        
        # Log user text message dengan state info
        message_preview = update.message.text[:50] + "..." if len(update.message.text) > 50 else update.message.text
        app_logger.info(f"💬 Text message from user {user.telegram_id}: '{message_preview}' (state: {user_state}, step: {journal_step})")
        
        if user_state == 'input_journal':
            if journal_step == 'waiting_for_text':
                await self._handle_journal_input(update, context, user)
            else:
                # If in journal mode but wrong step, guide user
                await update.message.reply_text(
                    "📝 **Journal Mode Aktif**\n\n"
                    "Kamu sedang dalam mode journal. Gunakan tombol yang tersedia atau ketik /start untuk reset.",
                    parse_mode='Markdown'
                )
        else:
            # Default response for random text
            await self._handle_general_text(update, context, user)
    
    async def _handle_journal_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user):
        """Handle initial journal entry text input"""
        journal_text = update.message.text.strip()
        
        # Basic validation
        if len(journal_text) < 10:
            app_logger.info(f"⚠️ Journal entry too short from user {user.telegram_id}: {len(journal_text)} chars")
            await update.message.reply_text(
                "📝 **Journal entry terlalu pendek**\n\n"
                "Untuk mendapatkan manfaat maksimal dari journaling, coba tulis setidaknya 10 karakter tentang:\n"
                "• Bagaimana perasaanmu hari ini\n"
                "• Apa yang terjadi hari ini\n"
                "• Challenges atau victories yang dialami\n"
                "• Goals atau intentions untuk besok\n\n"
                "Silakan tulis lagi entry yang lebih detail! ✍️",
                parse_mode='Markdown'
            )
            return
        
        # Store journal text in context for confirmation
        context.user_data['journal_text'] = journal_text
        context.user_data['journal_step'] = 'waiting_for_confirmation'
        
        # Calculate stats
        word_count = len(journal_text.split())
        char_count = len(journal_text)
        
        # Log successful input
        app_logger.info(f"📝 Journal input received from user {user.telegram_id}: {word_count} words, {char_count} chars")
        
        # Show confirmation message dengan preview dan tombol
        preview = journal_text[:200] + "..." if len(journal_text) > 200 else journal_text
        
        confirmation_message = f"""
✅ **Journal Entry Siap Disimpan**

**📊 Statistik Entry:**
• **Jumlah kata**: {word_count} kata
• **Jumlah karakter**: {char_count} karakter
• **Waktu**: {datetime.now().strftime("%d/%m/%Y %H:%M")}

**📄 Preview Entry:**
"{preview}"

**💾 Pilih tindakan:**
        """
        
        from src.bot.keyboards.inline_keyboards import BotKeyboards
        
        await update.message.reply_text(
            confirmation_message,
            reply_markup=BotKeyboards.journal_confirmation(),
            parse_mode='Markdown'
        )
    
    async def _handle_general_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user):
        """Handle general text messages"""
        message = """
🤖 **PMO Recovery Coach AI**

Halo! Saya melihat kamu mengirim pesan text. 

**📝 Untuk menulis journal entry:**
1. Pilih "📖 Journal" dari menu utama
2. Klik "✍️ Tulis Entry Baru"  
3. Ketik entry journal kamu

**💡 Atau gunakan commands:**
• `/start` - Menu utama
• `/help` - Bantuan commands
• `/motivation` - Quick motivation
• `/emergency` - Mode darurat

**🎯 Tips:**
Bot ini bekerja dengan menu dan commands. Gunakan /start untuk akses semua fitur!
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
