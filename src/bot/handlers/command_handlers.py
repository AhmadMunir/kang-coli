from telegram import Update
from telegram.ext import ContextTypes
from src.services import UserService, StreakService, MotivationalService
from src.bot.keyboards import BotKeyboards
from src.utils.helpers import format_streak_message, get_user_info
from src.utils.logger import app_logger

class CommandHandlers:
    """Handler untuk commands bot"""
    
    def __init__(self):
        self.user_service = UserService()
        self.streak_service = StreakService()
        self.motivational_service = MotivationalService()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /start command"""
        user_info = get_user_info(update.effective_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        # Log user interaction
        app_logger.info(f"👤 /start command from user {user.telegram_id} (@{user.username or 'no_username'})")
        
        welcome_message = f"""
🌟 **Selamat datang di PMO Recovery Coach AI!** 🌟

Halo {user_info['first_name']}! Saya di sini untuk membantu Anda dalam journey recovery dari PMO dengan pendekatan yang empatis dan berbasis bukti ilmiah.

**Apa yang bisa saya bantu:**
• 📊 Tracking streak harian Anda
• 💪 Motivasi dan dukungan emotional
• 🆘 Bantuan darurat saat urge datang
• 📚 Edukasi tentang recovery process
• 📝 Journaling dan self-reflection
• 🎯 Tips coping yang efektif

**Remember:** Recovery adalah journey, bukan destination. Setiap hari adalah kesempatan baru untuk menjadi versi terbaik dari diri Anda.

Silakan pilih menu di bawah untuk memulai:
        """
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /help command"""
        help_message = """
🤖 **PMO Recovery Coach - Commands Help**

**Main Commands:**
/start - Mulai menggunakan bot
/help - Tampilkan help message
/streak - Cek current streak
/motivation - Dapatkan motivasi
/emergency - Mode darurat
/checkin - Daily check-in
/relapse - Lapor relapse
/stats - Lihat statistik recovery

**Tips Penggunaan:**
• Gunakan menu inline untuk navigasi yang mudah
• Lakukan check-in harian untuk tracking yang akurat
• Jangan ragu gunakan mode darurat saat butuh bantuan
• Journaling membantu memahami pattern dan trigger
• Recovery adalah proses - be patient with yourself

**Privacy & Security:**
• Data Anda tersimpan aman dan tidak dibagikan
• Bot hanya menyimpan data yang diperlukan untuk tracking
• Anda bisa hapus data kapan saja di settings

Butuh bantuan lebih lanjut? Gunakan menu bantuan di bot!
        """
        
        await update.message.reply_text(
            help_message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def streak_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /streak command"""
        user_info = get_user_info(update.effective_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        current_streak = self.streak_service.calculate_current_streak(user.telegram_id)
        stats = self.streak_service.get_streak_stats(user.telegram_id)
        milestones = self.streak_service.get_streak_milestones(current_streak)
        
        message = format_streak_message(current_streak, stats, milestones)
        
        await update.message.reply_text(
            message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def motivation_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /motivation command"""
        quote = self.motivational_service.get_daily_quote()
        user_info = get_user_info(update.effective_user)
        user = self.user_service.get_user(user_info['telegram_id'])
        
        if user:
            current_streak = self.streak_service.calculate_current_streak(user.telegram_id)
            encouragement = self.motivational_service.get_streak_encouragement(current_streak)
        else:
            encouragement = "🌟 Setiap journey dimulai dari langkah pertama!"
        
        message = f"""
💪 **Daily Motivation**

"{quote['text']}"
*- {quote['author']}*

{encouragement}

**Remember:** Kamu lebih kuat dari yang kamu kira. Setiap detik yang kamu bertahan adalah kemenangan!
        """
        
        await update.message.reply_text(
            message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def emergency_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /emergency command"""
        emergency_message = """
🚨 **EMERGENCY MODE ACTIVATED** 🚨

Saya mengerti kamu sedang dalam situasi sulit. Tarik napas dalam-dalam. Kamu BISA melewati ini!

**Immediate Actions:**
1. 🛑 STOP scrolling/browsing sekarang juga
2. 💨 Tinggalkan area/posisi sekarang
3. 🧘 Tarik napas dalam 4 detik, tahan 4 detik, hembuskan 6 detik
4. 💧 Minum air dingin atau basuh wajah
5. 📱 Hubungi teman/keluarga atau ke area publik

**Remember:**
• Urge ini akan berlalu dalam 10-20 menit
• Kamu sudah bertahan sejauh ini - jangan sia-siakan!
• Setiap kali kamu menolak, kamu semakin kuat

Pilih protokol emergency di bawah:
        """
        
        await update.message.reply_text(
            emergency_message,
            reply_markup=BotKeyboards.emergency_menu(),
            parse_mode='Markdown'
        )
    
    async def relapse_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /relapse command - with confirmation"""
        message = """
💙 **Relapse Report**

Saya memahami betapa sulitnya moment ini untuk kamu. Yang penting adalah kamu datang ke sini untuk honest dan mau bangkit lagi.

Apakah kamu yakin ingin melaporkan relapse? Ini akan mereset streak kamu, tapi remember - ini bukan akhir dari segalanya.

**Setelah melaporkan relapse:**
• Streak akan di-reset ke 0
• Data akan tersimpan untuk learning
• Kamu akan mendapat support message
• Journey recovery dimulai lagi dari hari ini

Relapse adalah bagian dari proses recovery bagi banyak orang. Yang penting adalah bangkit dan belajar dari pengalaman ini.
        """
        
        await update.message.reply_text(
            message,
            reply_markup=BotKeyboards.relapse_confirmation(),
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /stats command"""
        user_info = get_user_info(update.effective_user)
        user = self.user_service.get_user(user_info['telegram_id'])
        
        if not user:
            await update.message.reply_text(
                "Kamu belum terdaftar. Gunakan /start untuk memulai!",
                reply_markup=BotKeyboards.main_menu()
            )
            return
        
        stats = self.streak_service.get_streak_stats(user.telegram_id)
        
        message = f"""
📊 **Recovery Statistics**

**Current Status:**
• 🔥 Current Streak: {stats['current_streak']} hari
• 🏆 Longest Streak: {stats['longest_streak']} hari  
• 📈 Success Rate: {stats['success_rate']}%

**Journey Overview:**
• 📅 Total Days in Recovery: {stats['total_days']} hari
• 💔 Total Relapses: {stats['total_relapses']}
• 🌱 Recovery Start: {stats['clean_start_date'].strftime('%d %B %Y') if stats['clean_start_date'] else 'Tidak ada data'}

**Progress Analysis:**
{self._get_progress_analysis(stats)}

Keep going strong! Every day counts! 💪
        """
        
        await update.message.reply_text(
            message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    def _get_progress_analysis(self, stats: dict) -> str:
        """Generate progress analysis based on stats"""
        current = stats['current_streak']
        longest = stats['longest_streak']
        success_rate = stats['success_rate']
        
        if current == longest and current > 0:
            return "🌟 Kamu sedang di streak terbaik! Personal record!"
        elif current > longest * 0.8:
            return "🔥 Hampir mencapai personal record! Keep pushing!"
        elif success_rate > 80:
            return "💎 Success rate excellent! Konsistensi yang luar biasa!"
        elif success_rate > 60:
            return "📈 Progress yang solid! Terus tingkatkan konsistensi!"
        elif success_rate > 40:
            return "💪 Ada progress positif! Focus pada strategy yang work!"
        else:
            return "🌱 Recovery adalah journey. Setiap step forward adalah win!"
