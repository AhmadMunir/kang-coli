from telegram import Update
from telegram.ext import ContextTypes
from src.services import UserService, StreakService, MotivationalService, EmergencyService
from src.bot.keyboards import BotKeyboards
from src.utils.helpers import get_user_info, format_streak_message

class CallbackHandlers:
    """Handler untuk inline keyboard callbacks"""
    
    def __init__(self):
        self.user_service = UserService()
        self.streak_service = StreakService()
        self.motivational_service = MotivationalService()
        self.emergency_service = EmergencyService()
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main callback handler - routes to specific handlers"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        # Route to appropriate handler
        if callback_data == "main_menu":
            await self._main_menu(query, context)
        elif callback_data == "check_streak":
            await self._check_streak(query, context)
        elif callback_data == "get_motivation":
            await self._get_motivation(query, context)
        elif callback_data == "emergency_mode":
            await self._emergency_mode(query, context)
        elif callback_data == "coping_tips":
            await self._coping_tips_menu(query, context)
        elif callback_data.startswith("tips_"):
            await self._handle_coping_tips(query, context, callback_data)
        elif callback_data == "education_menu":
            await self._education_menu(query, context)
        elif callback_data.startswith("edu_"):
            await self._handle_education(query, context, callback_data)
        elif callback_data == "settings_menu":
            await self._settings_menu(query, context)
        elif callback_data == "report_relapse":
            await self._report_relapse(query, context)
        elif callback_data == "confirm_relapse":
            await self._confirm_relapse(query, context)
        elif callback_data == "cancel_relapse":
            await self._cancel_relapse(query, context)
        elif callback_data.startswith("emergency_"):
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "daily_checkin":
            await self._daily_checkin(query, context)
        elif callback_data == "journal_menu":
            await self._journal_menu(query, context)
        elif callback_data.startswith("mood_"):
            await self._handle_mood_selection(query, context, callback_data)
        else:
            await query.edit_message_text("Menu tidak dikenali. Kembali ke menu utama.", 
                                        reply_markup=BotKeyboards.main_menu())
    
    async def _main_menu(self, query, context):
        """Show main menu"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_or_create_user(**user_info)
        current_streak = self.streak_service.calculate_current_streak(user.telegram_id)
        
        message = f"""
🌟 **PMO Recovery Coach AI**

Halo {user_info['first_name']}! 

📊 Current Streak: **{current_streak} hari**
💪 Apa yang ingin kamu lakukan hari ini?

Pilih menu di bawah:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def _check_streak(self, query, context):
        """Handle check streak callback"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        current_streak = self.streak_service.calculate_current_streak(user.telegram_id)
        stats = self.streak_service.get_streak_stats(user.telegram_id)
        milestones = self.streak_service.get_streak_milestones(current_streak)
        
        message = format_streak_message(current_streak, stats, milestones)
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _get_motivation(self, query, context):
        """Handle get motivation callback"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_user(user_info['telegram_id'])
        
        quote = self.motivational_service.get_daily_quote()
        
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

Remember: Kamu lebih kuat dari yang kamu kira! 🔥
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _emergency_mode(self, query, context):
        """Handle emergency mode callback"""
        message = """
🚨 **EMERGENCY MODE ACTIVATED** 🚨

Tarik napas dalam-dalam. Kamu BISA melewati ini!

**Quick Actions:**
• 🛑 Stop browsing sekarang juga
• 💨 Tinggalkan area/posisi sekarang  
• 🧘 Fokus pada pernapasan
• 💧 Minum air atau basuh wajah

Pilih protokol emergency:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.emergency_menu(),
            parse_mode='Markdown'
        )
    
    async def _coping_tips_menu(self, query, context):
        """Handle coping tips menu"""
        message = """
🎯 **Coping Strategies**

Pilih kategori tips yang ingin kamu pelajari:

**Physical** - Aktivitas fisik untuk mengalihkan energi
**Mental** - Teknik mental dan cognitive strategies  
**Distraction** - Pengalihan perhatian yang efektif
**Mindfulness** - Teknik mindfulness dan meditation
**Productive** - Channel energi ke aktivitas produktif

Atau pilih **Random Tip** untuk mendapat strategi acak!
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.coping_tips_menu(),
            parse_mode='Markdown'
        )
    
    async def _handle_coping_tips(self, query, context, callback_data):
        """Handle specific coping tips"""
        category_map = {
            "tips_physical": "physical",
            "tips_mental": "mental", 
            "tips_distraction": "distraction",
            "tips_mindfulness": "mindfulness",
            "tips_productive": "productive",
            "tips_random": None
        }
        
        category = category_map.get(callback_data)
        tip = self.motivational_service.get_coping_tip(category)
        
        message = f"""
🎯 **{tip['title']}**

**Kategori:** {tip['category'].title()}
**Durasi:** {tip['duration']}

**Cara melakukan:**
{tip['description']}

**Pro Tip:** Konsistensi lebih penting dari perfection. Coba technique ini setiap kali urge datang untuk membangun new neural pathways!
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _education_menu(self, query, context):
        """Handle education menu"""
        message = """
📚 **Recovery Education Center**

Belajar tentang science di balik PMO recovery:

**🧠 Dopamine & Recovery** - Bagaimana dopamine bekerja dan recovery process

**✨ Benefits NoFap** - Manfaat yang dilaporkan oleh banyak orang

**🔄 Neuroplasticity** - Bagaimana otak bisa berubah dan heal

**📈 Recovery Timeline** - Apa yang diharapkan dalam timeline recovery

Knowledge is power! Semakin kamu understand prosesnya, semakin mudah untuk tetap motivated.
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.education_menu(),
            parse_mode='Markdown'
        )
    
    async def _handle_education(self, query, context, callback_data):
        """Handle education content"""
        topic_map = {
            "edu_dopamine": "dopamine",
            "edu_benefits": "benefits",
            "edu_neuroplasticity": "neuroplasticity",
            "edu_timeline": "general"
        }
        
        topic = topic_map.get(callback_data, "general")
        content = self.motivational_service.get_educational_content(topic)
        
        message = f"""
{content['title']}

{content['content']}

Remember: Understanding the process helps you stay committed to recovery! 💪
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _settings_menu(self, query, context):
        """Handle settings menu"""
        message = """
⚙️ **Settings & Preferences**

**🔔 Reminder Settings** - Atur daily reminders
**🌍 Timezone** - Set timezone untuk accurate tracking
**📊 Lihat Stats** - Detailed recovery statistics  
**🗑️ Reset Data** - Reset semua data (permanent!)

Atur preferences sesuai kebutuhanmu untuk experience yang optimal.
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.settings_menu(),
            parse_mode='Markdown'
        )
    
    async def _report_relapse(self, query, context):
        """Handle report relapse"""
        message = """
💙 **Relapse Report**

Saya memahami betapa sulitnya moment ini. Yang penting adalah kamu honest dan mau bangkit lagi.

Apakah kamu yakin ingin melaporkan relapse?

**Yang akan terjadi:**
• Streak akan di-reset ke 0  
• Data tersimpan untuk learning
• Kamu dapat support dan guidance
• Journey baru dimulai hari ini

Relapse adalah bagian dari recovery journey bagi banyak orang. Yang penting adalah bangkit dan belajar! 💪
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.relapse_confirmation(),
            parse_mode='Markdown'
        )
    
    async def _confirm_relapse(self, query, context):
        """Handle confirm relapse"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_user(user_info['telegram_id'])
        
        if user:
            # Record the relapse
            success = self.streak_service.record_relapse(user.telegram_id)
            
            if success:
                support_message = self.motivational_service.get_relapse_support()
                
                message = f"""
💙 **Relapse Recorded**

{support_message}

**New Journey Starts Now:**
• Streak reset to 0 days
• Learn from this experience  
• Identify triggers and patterns
• Strengthen your strategy
• You're stronger than before

**Next Steps:**
1. Don't dwell on guilt - focus forward
2. Analyze what led to this moment  
3. Adjust your prevention strategy
4. Get back to healthy routines
5. Use this bot for daily support

Tomorrow is a new day. You've got this! 🌅
                """
                
                await query.edit_message_text(
                    message,
                    reply_markup=BotKeyboards.main_menu(),
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    "Terjadi error. Silakan coba lagi atau hubungi support.",
                    reply_markup=BotKeyboards.main_menu()
                )
        else:
            await query.edit_message_text(
                "User tidak ditemukan. Gunakan /start untuk register.",
                reply_markup=BotKeyboards.main_menu()
            )
    
    async def _cancel_relapse(self, query, context):
        """Handle cancel relapse"""
        message = """
💪 **That's the Spirit!**

Bagus! Kamu masih kuat dan belum menyerah!

**Keep Fighting:**
• Gunakan coping strategies
• Alihkan perhatian ke aktivitas positif
• Remember your why
• Take it one hour at a time

Kamu sudah membuktikan mental strength dengan tidak melaporkan false relapse. Keep that energy! 🔥
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.main_menu(),
            parse_mode='Markdown'
        )
    
    async def _handle_emergency(self, query, context, callback_data):
        """Handle emergency protocols"""
        if callback_data == "urge_surfing":
            guide = self.emergency_service.get_urge_surfing_guide()
            
            steps_text = "\n".join([
                f"**Step {step['step']}: {step['instruction']}**\n{step['detail']}"
                for step in guide['steps']
            ])
            
            key_points = "\n".join([f"• {point}" for point in guide['key_points']])
            
            message = f"""
{guide['title']}

{guide['description']}

**Steps to Follow:**
{steps_text}

**Key Points:**
{key_points}

Remember: Urges are like waves - they rise, peak, and fall. Ride them out! 🌊
            """
        
        elif callback_data == "trigger_analysis":
            analysis = self.emergency_service.get_trigger_analysis()
            message = f"""
{analysis['title']}

**Common Triggers:**

**Emotional:**
{chr(10).join([f"• {trigger}" for trigger in analysis['common_triggers']['emotional']])}

**Environmental:**  
{chr(10).join([f"• {trigger}" for trigger in analysis['common_triggers']['environmental']])}

**Physical:**
{chr(10).join([f"• {trigger}" for trigger in analysis['common_triggers']['physical']])}

**Action Plan:**
{chr(10).join([f"{i+1}. {action}" for i, action in enumerate(analysis['action_plan'])])}
            """
        
        elif callback_data == "emergency_contacts":
            contacts = self.emergency_service.get_emergency_contacts()
            message = f"""
{contacts['title']}

**Immediate Help Options:**
{chr(10).join([f"• {option}" for option in contacts['immediate_help']])}

**Crisis Hotlines (Indonesia):**
• SEJIWA: {contacts['hotlines']['indonesia']['sejiwa']}
• Halo Kemkes: {contacts['hotlines']['indonesia']['halo_kemkes']}

**Online Communities:**
{chr(10).join([f"• {community}" for community in contacts['online_communities']])}

{contacts['reminder']} 💙
            """
        
        else:
            # Handle other emergency protocols
            intervention = self.emergency_service.get_emergency_intervention()
            protocol = intervention['protocol']
            
            steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(protocol['steps'])])
            
            message = f"""
{protocol['title']}

**Duration:** {protocol['duration']}

**Steps to Follow:**
{steps_text}

**Emergency Message:**
{intervention['alert_message']}

{intervention['reminder']}
            """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _daily_checkin(self, query, context):
        """Handle daily check-in"""
        message = """
📝 **Daily Check-in**

Bagaimana perasaanmu hari ini?

Rate mood kamu dari 1-5:
1 = Sangat buruk, 5 = Sangat baik

Pilih angka di bawah:
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.mood_scale(),
            parse_mode='Markdown'
        )
    
    async def _journal_menu(self, query, context):
        """Handle journal menu"""
        message = """
📖 **Personal Journal**

**✍️ Tulis Entry Baru** - Catat thoughts dan feelings hari ini
**📖 Baca Entries** - Review journal entries sebelumnya  
**🎯 Analisis Mood** - Pattern mood dari journal entries
**🔍 Analisis Trigger** - Identify triggers dari entries

Journaling membantu self-awareness dan memahami patterns dalam recovery journey!
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.journal_menu(),
            parse_mode='Markdown'
        )
    
    async def _handle_mood_selection(self, query, context, callback_data):
        """Handle mood selection from daily check-in"""
        # Extract mood value from callback_data (mood_1, mood_2, etc.)
        mood_value = int(callback_data.split("_")[1])
        
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        # Create mood descriptions
        mood_descriptions = {
            1: "😢 Sangat buruk",
            2: "😔 Kurang baik", 
            3: "😐 Netral",
            4: "😊 Baik",
            5: "😄 Sangat baik"
        }
        
        mood_desc = mood_descriptions.get(mood_value, "Unknown")
        
        # Save mood data (you can extend this to save to database)
        # For now, just show confirmation and encouragement
        
        if mood_value <= 2:
            # Low mood - provide extra support
            message = f"""
📝 **Check-in Completed**

Mood hari ini: {mood_desc} ({mood_value}/5)

Saya melihat kamu sedang merasa kurang baik hari ini. Itu normal dan ok! 💙

🤗 **Tips untuk hari ini:**
• Ingat bahwa perasaan ini temporary
• Coba lakukan satu hal kecil yang membuatmu senang
• Reach out ke teman atau keluarga
• Consider light exercise atau jalan-jalan

💪 **Remember:** Bad days tidak menghapus progress yang sudah kamu buat!

Butuh bantuan lebih? Gunakan Mode Darurat di menu utama.
            """
        elif mood_value == 3:
            # Neutral mood
            message = f"""
📝 **Check-in Completed**

Mood hari ini: {mood_desc} ({mood_value}/5)

Hari yang cukup netral! Sometimes that's exactly what we need. 😌

🎯 **Suggestion untuk hari ini:**
• Coba satu aktivitas yang biasanya kamu enjoy
• Set small achievable goal untuk sisa hari
• Practice gratitude - list 3 hal yang kamu syukuri

Keep going, you're doing great! 💪
            """
        else:
            # Good mood
            message = f"""
📝 **Check-in Completed**

Mood hari ini: {mood_desc} ({mood_value}/5)

Wonderful! Senang mendengar kamu merasa baik hari ini! 🌟

✨ **Cara maintain good mood:**
• Share positivity dengan orang lain
• Gunakan energi ini untuk productive activities
• Reflect on apa yang membuat hari ini special
• Set intention untuk besok

Keep up the great work! You're thriving! 🚀
            """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
