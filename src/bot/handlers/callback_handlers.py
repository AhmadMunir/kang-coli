from telegram import Update
from telegram.ext import ContextTypes
from src.services import UserService, StreakService, MotivationalService, EmergencyService, JournalService
from src.bot.keyboards import BotKeyboards
from src.utils.helpers import get_user_info, format_streak_message
from src.utils.logger import app_logger

class CallbackHandlers:
    """Handler untuk inline keyboard callbacks"""
    
    def __init__(self):
        self.user_service = UserService()
        self.streak_service = StreakService()
        self.motivational_service = MotivationalService()
        self.emergency_service = EmergencyService()
        self.journal_service = JournalService()
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main callback handler - routes to specific handlers"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        user_info = get_user_info(query.from_user)
        
        # Log callback interaction
        app_logger.info(f"🔘 Callback '{callback_data}' from user {user_info['telegram_id']} (@{user_info.get('username', 'no_username')})")
        
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
        elif callback_data == "urge_surfing":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "trigger_analysis":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "immediate_distraction":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "mindfulness_protocol":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "emergency_contacts":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "accountability_check":
            await self._handle_emergency(query, context, callback_data)
        elif callback_data == "daily_checkin":
            await self._daily_checkin(query, context)
        elif callback_data == "journal_menu":
            await self._journal_menu(query, context)
        elif callback_data == "mood_analysis":
            await self._mood_analysis(query, context)
        elif callback_data == "trigger_journal":
            await self._trigger_analysis(query, context)
        elif callback_data.startswith("mood_"):
            await self._handle_mood_selection(query, context, callback_data)
        elif callback_data == "new_journal":
            await self._new_journal(query, context)
        elif callback_data == "read_journal":
            await self._read_journal(query, context)
        elif callback_data == "journal_save":
            await self._journal_save_callback(query, context)
        elif callback_data == "journal_cancel":
            await self._journal_cancel_callback(query, context)
        elif callback_data == "journal_edit":
            await self._journal_edit_callback(query, context)
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
🆘 **EMERGENCY MODE ACTIVATED** 🆘

**⚠️ SITUASI DARURAT PMO RECOVERY**

Kamu sedang mengalami urge atau craving yang kuat. TARIK NAPAS dan ikuti protokol emergency ini:

**🚨 IMMEDIATE RESPONSE (0-2 menit):**
1. **STOP** - Hentikan semua aktivitas sekarang
2. **BREATHE** - Tarik napas dalam 4 detik, tahan 4 detik, buang 4 detik
3. **MOVE** - Tinggalkan lokasi/posisi sekarang juga
4. **DISTRACT** - Alihkan perhatian dengan aktivitas fisik

**🔥 Ingat: Urge akan berlalu dalam 15-20 menit!**

**📱 PROTOKOL EMERGENCY OPTIONS:**

🌊 **Urge Surfing** - Teknik surf the urge tanpa melawan
🎯 **Trigger Analysis** - Identify immediate triggers
💨 **Immediate Distraction** - Quick distraction techniques  
🧘 **Mindfulness Protocol** - Emergency mindfulness practice
🆘 **Emergency Contacts** - Connect dengan support system
💬 **Accountability Check** - Report dan get support

**💡 QUICK REMINDERS:**
• Kamu sudah berhasil melewati urge sebelumnya
• Recovery is a journey, not perfection
• Setiap detik yang kamu tahan adalah kemenangan
• Your future self will thank you

**Pilih protokol yang paling sesuai dengan situasi kamu sekarang:**
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
🌊 **URGE SURFING PROTOCOL - EMERGENCY GUIDE**

**🏄‍♂️ Apa itu Urge Surfing?**
Urge surfing adalah teknik mindfulness untuk 'menunggangi' gelombang urge tanpa melawan atau menyerah. Seperti surfer menunggangi ombak, kamu observe urge sampai reda sendiri.

**🧠 Mengapa Efektif?**
• Urge memiliki siklus alami (naik-puncak-turun) dalam 15-20 menit
• Melawan urge malah memperkuat (ironic process theory)  
• Acceptance mengurangi kekuatan urge

**🏄‍♂️ LANGKAH URGE SURFING:**

**1. ACKNOWLEDGE (0-2 menit)**
"Aku sedang mengalami urge. Ini normal dalam recovery."
• Jangan panic atau judge diri sendiri
• Recognize: ini hanya temporary feeling

**2. OBSERVE SENSATIONS (2-5 menit)**  
• Dimana kamu merasakan urge di tubuh?
• Apakah ada tension, heat, tingling?
• Notice rhythm atau pulsing-nya

**3. BREATHE & SURF (5-15 menit)**
• Napas dalam dan slow
• Bayangkan urge sebagai gelombang
• Kamu adalah surfer di atas papan
• Ride the wave, don't fight it

**4. WAIT & WATCH (15-20 menit)**
• Watch intensity naik turun
• Notice peak, then natural decrease
• Stay curious, not judgmental

Remember: Urges are like waves - they rise, peak, and fall. Ride them out! 🌊
            """
        
        elif callback_data == "trigger_analysis":
            message = """
🎯 **EMERGENCY TRIGGER ANALYSIS**

**⚠️ SITUASI DARURAT - TRIGGER IDENTIFICATION**

**🔍 IMMEDIATE ASSESSMENT - ASK YOURSELF:**
1. **Dimana kamu sekarang?** (lokasi, ruangan, posisi)
2. **Jam berapa ini terjadi?** (time pattern awareness)
3. **Apa yang kamu lakukan sebelumnya?** (aktivitas trigger)
4. **Bagaimana mood kamu?** (emotional state)
5. **Apakah kamu sendiri?** (social context)

**📊 COMMON TRIGGER CATEGORIES:**

**🏠 ENVIRONMENTAL TRIGGERS:**
• Kamar sendirian, rumah kosong
• Device/gadget dengan internet access
• Tempat tidur, kamar mandi private
• Waktu tertentu (malam, weekend, boring moments)

**😔 EMOTIONAL TRIGGERS:**
• Stress, boredom, loneliness, anxiety
• Depression, overwhelm, frustration
• Low self-esteem, shame, anger
• Celebration atau sadness extremes

**💻 DIGITAL TRIGGERS:**
• Social media scrolling tanpa tujuan
• Random browsing, "harmless" content
• Gaming, streaming platforms
• Accidental exposure ke triggering content

**🧠 MENTAL TRIGGERS:**
• Fantasy, daydreaming, nostalgia
• "Just one peek" rationalization thoughts
• Testing willpower atau curiosity
• Bargaining dengan diri sendiri

**⚡ EMERGENCY ACTION PLAN:**

**RIGHT NOW:**
1. **Name it:** "I'm triggered by [specific trigger]"
2. **Remove it:** Leave/close/change immediately
3. **Replace:** 20 push-ups, cold shower, call friend
4. **Protect:** Block, move public, tell someone

**📝 FOR FUTURE PREVENTION:**
• Journal this trigger pattern recognition
• Create specific counter-plan for this trigger
• Modify environment to reduce exposure opportunities
• Build stronger defenses dan early warning systems

**🎯 REMEMBER:** Every trigger identified = growth opportunity!
            """
        
        elif callback_data == "emergency_contacts":
            message = """
🆘 **EMERGENCY SUPPORT CONTACTS**

**🔥 IMMEDIATE SUPPORT - REACH OUT NOW:**

**💬 PERSONAL SUPPORT (TEXT/CALL):**
• Accountability partner atau recovery buddy
• Trusted friend atau family member  
• Mentor, coach, atau counselor
• Someone who knows your recovery journey

**📱 PMO RECOVERY COMMUNITIES (24/7):**
• Reddit: r/NoFap, r/pornfree (active community)
• Discord recovery servers (real-time chat)
• Facebook support groups (private groups)
• Recovery apps with community features

**🇮🇩 INDONESIA CRISIS HOTLINES (24/7):**
• **SEJIWA (Suicide Prevention):** 119 ext 8
• **Halo Kemkes (Health Ministry):** 1500-567  
• **IBUNDA (Crisis Support):** 0800-1-696-969
• **Yayasan Pulih (Mental Health):** 021-788-42580

**🌍 INTERNATIONAL SUPPORT:**
• **Crisis Text Line:** Text HOME to 741741
• **SAMHSA National Helpline:** 1-800-662-4357
• **Lifeline:** 988 (US) atau local emergency number

**💻 ONLINE IMMEDIATE HELP:**
• 7cups.com - Anonymous emotional support
• BetterHelp crisis chat feature
• Recovery forums active 24/7
• PMO recovery Discord communities

**📝 SCRIPT FOR REACHING OUT:**
"Hi, I'm having a tough moment in my recovery and could use some support. Can we talk for a few minutes?"

**🤝 ACCOUNTABILITY MESSAGE TEMPLATE:**
"I'm experiencing strong urges right now. I'm reaching out instead of acting on them. Can you help remind me why this recovery matters to me?"

**💡 REMEMBER - REACHING OUT IS STRENGTH:**
• Most people WANT to help when asked directly
• 5-minute conversation can completely change trajectory
• You've probably helped others too - let them return favor
• Building support network is part of recovery

**🏆 AFTER GETTING SUPPORT:**
• Thank them for being available
• Update them later on your progress
• Offer to be there for them too
• Strengthen the relationship for future

🚨 **IF IN MENTAL HEALTH CRISIS:** Don't hesitate to contact professional help immediately.

Your life and wellbeing matter more than anything else! 💙
            """
        
        elif callback_data == "immediate_distraction":
            message = """
💨 **IMMEDIATE DISTRACTION PROTOCOL**

**🚨 EMERGENCY DISTRACTION - ACT NOW!**

**⚡ 0-2 MENIT (IMMEDIATE ACTION):**
1. **STAND UP** - Get vertical immediately (disrupts thought pattern)
2. **LEAVE LOCATION** - Exit current room/position now
3. **INTENSE MOVEMENT** - 20 jumping jacks atau run in place
4. **COLD SHOCK** - Splash cold water on face/drink ice water

**💪 2-5 MENIT (PHYSICAL ENGAGEMENT):**
• **Push-ups** - Do as many as you can (exhaustion stops urges)
• **Squats/Burpees** - 30 quick reps (intense physical activity)
• **Cold shower** - 2-3 minutes minimum (shock to system)
• **Run outside** - Around block atau in place if needed

**🎵 5-10 MENIT (SENSORY OVERLOAD):**
• **Loud energetic music** - Motivational/pump up songs
• **Call someone immediately** - Friend, family, accountability partner
• **Educational content** - Motivational podcast/YouTube
• **Sing/dance aggressively** - Engage multiple senses

**🎮 10-15 MENIT (MENTAL ENGAGEMENT):**
• **Action videogames** - NOT browser-based (console/mobile)
• **Active hobbies** - Guitar, drawing, cooking, reading
• **Cleaning/organizing** - Physical environment improvement
• **Learn new skill** - Tutorial, language, instrument practice

**🧠 DISTRACTION SCIENCE WHY IT WORKS:**
• Brain can only intensely focus on one thing at a time
• Physical activity rapidly changes brain chemistry (endorphins)
• Cold exposure triggers alertness and mental clarity
• Social connection releases oxytocin (bonding hormone)

**⏰ SURVIVAL TIME GOAL:** First 15-20 minutes are critical!

**🏆 SUCCESS REMINDER:** Every urge you resist makes the next one significantly easier to handle!
            """
            
        elif callback_data == "mindfulness_protocol":
            message = """
🧘 **EMERGENCY MINDFULNESS PROTOCOL**

**🎯 MINDFUL EMERGENCY INTERVENTION**

**💺 SETUP (1 minute):**
• Find alert sitting position (NOT lying down)
• Both feet on floor, hands on knees
• Spine straight but relaxed
• Set timer 10-15 minutes if available

**👁️ STEP 1: AWARENESS (3 minutes)**
• Notice: "I am having urge right now"
• Observe without judgment: "This is what urge feels like"  
• Remember: "I am NOT my urges, I am the observer"

**🫁 STEP 2: BREATHING ANCHOR (5 minutes)**
• **Box Breathing:** In 4 counts → Hold 4 → Out 4 → Hold 4
• Feel breath in nostrils, chest expansion, belly rise
• When mind wanders to urge, gently return to breath
• Mental mantra: "Breathing in calm, breathing out urge"

**🌊 STEP 3: URGE OBSERVATION (5 minutes)**
• Where exactly do you feel urge in your body?
• Is sensation hot/cold, tight/loose, moving/still?
• Rate intensity 1-10, watch it naturally change
• Don't try to change it, just witness with curiosity

**💭 STEP 4: THOUGHT WATCHING (3 minutes)**
• Notice urge-related thoughts arising
• Label them: "Urge thought," "Rationalization," "Fantasy"
• Don't engage with or fight the thoughts
• Let them pass like clouds across sky

**💪 STEP 5: VALUES RECONNECTION (2 minutes)**
• Why did you start PMO recovery journey?
• What kind of person do you want to become?
• How will you feel about yourself if you stay strong?
• Connect deeply with your higher purpose

**🌟 MINDFULNESS MANTRAS:**
• "This too shall pass naturally"
• "I am not my urges or thoughts" 
• "I choose my response consciously"
• "Present moment awareness is power"

**🧠 THE NEUROSCIENCE:**
• Increases prefrontal cortex activity (self-control center)
• Decreases amygdala reactivity (emotional overwhelm)
• Creates space between stimulus and automatic response
• Builds long-term resilience and emotional regulation

**✨ POST-SESSION:** Rate urge intensity before/after. Notice any decrease? Either way, you practiced not acting = SUCCESS!
            """
            
        elif callback_data == "accountability_check":
            message = """
💬 **EMERGENCY ACCOUNTABILITY CHECK**

**🎯 IMMEDIATE SELF-ACCOUNTABILITY PROTOCOL**

**📋 REALITY CHECK - ASK YOURSELF:**
1. **Current streak:** How many days clean am I?
2. **1-hour future:** How will I feel if I relapse right now?
3. **Original reasons:** Why did I start recovery?
4. **Important people:** Who am I doing this for?
5. **Progress lost:** What will I lose if I give in?

**💪 STRENGTH EVIDENCE REVIEW:**
• You've already resisted urges successfully before
• Every day clean is PROOF of your inner strength
• You chose recovery for important, valid reasons
• You're measurably stronger now than when you started

**📊 PROGRESS ACKNOWLEDGMENT:**
• Count your streak days - that's REAL measurable progress
• Remember challenges you've already successfully overcome
• Compare how you feel now vs when you first started
• Notice concrete improvements in your life since quitting

**🎯 GOAL RECONNECTION:**
• **Today:** Just make it through right now, this moment
• **This week:** Reach next weekly milestone confidently
• **This month:** 30/60/90 day targets (major milestones)
• **Life vision:** Person you're becoming, future relationships

**💔 RELAPSE REALITY (if you give in now):**
• Streak immediately resets to 0
• Intense guilt, shame, disappointment cascade
• Must restart entire recovery process from beginning
• Lose momentum and hard-earned confidence
• Reinforce neural pathways you're trying to break

**🏆 STAYING STRONG REALITY (if you resist now):**
• Streak continues growing and compounds
• Pride, accomplishment, self-respect feelings
• Momentum builds exponentially toward next milestone
• Confidence in ability increases dramatically
• Reinforce healthy neural pathway development

**🔥 ACCOUNTABILITY MANTRAS:**
• "I am accountable to my future self"
• "My commitments to myself matter most"
• "I honor my word and build integrity"
• "I am actively becoming who I want to be"

**🎉 CELEBRATE THIS MOMENT:** 
You're doing accountability check instead of relapsing - that shows incredible growth and self-awareness already!
            """
        
        else:
            # Fallback for any other emergency protocols
            message = """
🚨 **EMERGENCY SUPPORT ACTIVATED**

**⚠️ YOU'RE IN EMERGENCY MODE**
Kamu sedang mengalami situasi darurat dalam recovery. Ini NORMAL dan kamu absolutely pasti bisa melewatinya!

**🚨 IMMEDIATE EMERGENCY ACTIONS:**
1. **BREATHE DEEPLY** - 3 slow, deep breaths right now
2. **CHANGE LOCATION** - Leave where you are immediately  
3. **PHYSICAL MOVEMENT** - Do jumping jacks, push-ups, cold shower
4. **REACH OUT** - Contact support system, accountability partner

**💪 EMERGENCY REMINDERS:**
• This urge WILL pass (average 15-20 minutes)
• You've survived urges before and gotten stronger
• Every moment you resist is building your recovery muscle
• Your future self will thank you for staying strong

**📱 QUICK ACCESS:**
Use emergency menu buttons for specific protocols:
• 🌊 Urge Surfing - Mindful observation technique
• 🎯 Trigger Analysis - Identify what triggered this
• 💨 Immediate Distraction - Physical intervention methods
• 🧘 Mindfulness Protocol - Calm, centered approach
• 🆘 Emergency Contacts - Reach out for human support
• 💬 Accountability Check - Reconnect with your why

**🏆 YOU'VE GOT THIS!** Choose your emergency protocol below.
            """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.emergency_protocol_menu(),
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
📖 **Personal Journal System**

**Apa itu Journal Feature?**
Journal adalah tools powerful untuk self-reflection dan progress tracking dalam recovery journey. Fitur ini membantu build self-awareness dan emotional intelligence.

**🎯 Manfaat Journaling:**
• **Self-Awareness** - Understand thoughts, feelings, dan behaviors
• **Progress Tracking** - Monitor growth dan improvement over time
• **Trigger Identification** - Recognize patterns dan warning signs
• **Emotional Processing** - Safe space untuk express dan work through feelings
• **Goal Setting** - Clarify objectives dan track achievements
• **Stress Relief** - Therapeutic outlet untuk mental health

**📝 Available Features:**

**✍️ Tulis Entry Baru** - Write personal reflections, thoughts, feelings, daily experiences. Include mood, challenges, victories, goals.

**📖 Baca Entries** - Review past entries to see progress dan patterns (Coming Soon)

**🎯 Analisis Mood** - AI-powered mood pattern analysis dari entries (Coming Soon)

**🔍 Analisis Trigger** - Identify triggers dan risk factors dari journal content (Coming Soon)

**💡 Journaling Tips:**
• Write consistently, even if just few sentences
• Be honest dan authentic dalam expression
• Include both challenges dan positive moments
• Note triggers, coping strategies, dan lessons learned
• Set intentions atau goals untuk future

Start dengan "✍️ Tulis Entry Baru" untuk begin your journaling journey!
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
    
    async def _new_journal(self, query, context):
        """Handle new journal entry - set user state for text input"""
        
        # Set user state to expect journal input
        context.user_data['state'] = 'input_journal'
        context.user_data['journal_step'] = 'waiting_for_text'
        
        # Log state change
        user_info = get_user_info(query.from_user)
        app_logger.info(f"📝 User {user_info['telegram_id']} entered journal input mode (state: input_journal)")
        
        message = """
📝 **Tulis Entry Journal Baru**

**🎯 Status: Menunggu Input Journal** 

Bot sekarang siap menerima entry journal dari kamu. Ketik pesan berikutnya sebagai journal entry.

**💡 Apa yang bisa kamu tulis:**
• **Perasaan hari ini** - Bagaimana mood dan emotional state
• **Events & experiences** - Apa yang terjadi hari ini  
• **Challenges** - Difficulties atau struggles yang dihadapi
• **Victories** - Achievements atau positive moments
• **Triggers** - Situasi yang challenging untuk recovery
• **Coping strategies** - Techniques yang kamu gunakan
• **Gratitude** - Hal-hal yang kamu syukuri
• **Goals & intentions** - Plans untuk besok atau future
• **Reflections** - Insights atau lessons learned

**✍️ Tips untuk effective journaling:**
• Write dari hati, be honest dan authentic
• Include both positive dan challenging aspects
• Mention specific events, feelings, dan thoughts
• Note any patterns atau insights
• Set intentions atau goals untuk moving forward
• Aim untuk minimal 10 karakter untuk meaningful reflection

**📝 Format bebas** - tulis natural seperti diary personal.

**Contoh entry:**
"Hari ini cukup challenging karena stress di kantor, tapi saya berhasil manage dengan breathing exercises. Mood sekitar 3/5. Grateful untuk support dari keluarga. Besok ingin focus pada morning routine yang lebih konsisten."

**⌨️ Ketik entry journal kamu sekarang dan tekan Enter!** ⬇️
        """
        
        await query.edit_message_text(
            message,
            parse_mode='Markdown'
        )
    
    async def _read_journal(self, query, context):
        """Handle read journal entries"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        # Get recent entries from database
        entries = self.journal_service.get_user_entries(user.telegram_id, limit=5)
        stats = self.journal_service.get_entry_stats(user.telegram_id)
        
        if not entries:
            message = """
📖 **Baca Journal Entries**

**Belum ada journal entries!** �

Kamu belum menulis journal entry apapun. Mari mulai journaling journey!

**🎯 Get Started:**
• Klik "✍️ Tulis Entry Baru" untuk start
• Write about perasaan, thoughts, experiences hari ini
• Build habit journaling untuk maximum benefit

**💡 Benefits dari regular journaling:**
• Self-awareness dan emotional intelligence
• Progress tracking dalam recovery journey
• Trigger identification dan pattern recognition
• Therapeutic outlet untuk stress relief

Start writing your first entry today! ✍️
            """
        else:
            # Format recent entries
            entries_text = ""
            for i, entry in enumerate(entries, 1):
                date_str = entry.created_at.strftime("%d/%m/%Y %H:%M")
                preview = entry.entry_text[:100] + "..." if len(entry.entry_text) > 100 else entry.entry_text
                entries_text += f"\n**{i}. {date_str}**\n{preview}\n"
            
            message = f"""
📖 **Your Journal Entries**

**📊 Journal Statistics:**
• **Total entries:** {stats.get('total_entries', 0)}
• **Total words:** {stats.get('total_words', 0):,}
• **Average words per entry:** {stats.get('average_words', 0)}
• **First entry:** {stats.get('first_entry').strftime('%d/%m/%Y') if stats.get('first_entry') else 'N/A'}
• **Last entry:** {stats.get('last_entry').strftime('%d/%m/%Y') if stats.get('last_entry') else 'N/A'}

**� Recent Entries (Last 5):**
{entries_text}

**🎯 Amazing Progress!** You've been consistently documenting your recovery journey.

**💡 Keep Going:**
• Continue writing regularly untuk build rich data
• Notice patterns dalam entries untuk insights
• Use entries untuk reflect on growth over time

Great work maintaining your journaling habit! 💪✨
            """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _mood_analysis(self, query, context):
        """Handle mood analysis"""
        message = """
🎯 **Analisis Mood**

**Advanced Feature Coming Soon!** 📊

Fitur analisis mood akan memberikan insights mendalam tentang emotional patterns Anda:

**📈 Mood Analytics akan include:**
• **Mood Trends** - Grafik mood dari waktu ke waktu
• **Pattern Recognition** - Identify recurring mood patterns
• **Trigger Correlation** - Connection antara events dan mood changes
• **Weekly/Monthly Reports** - Comprehensive mood summaries
• **Improvement Suggestions** - Personalized tips based pada patterns
• **Mood Forecasting** - Predict challenging periods

**🎨 Visualization Features:**
• Color-coded mood calendar
• Trend lines dan charts
• Mood distribution graphs
• Correlation matrices

**🔍 Current Alternatives:**
• Use daily check-in untuk track mood harian
• Note mood dalam journal entries
• Observe personal patterns manually
• Use emergency mode saat mood rendah

**💡 Self-Analysis Tips:**
• Track mood consistently every day
• Note external factors yang influence mood
• Identify time patterns (morning vs evening mood)
• Connect mood dengan sleep, exercise, activities

Continue dengan daily check-ins untuk build data yang berguna untuk future analysis!
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode='Markdown'
        )
    
    async def _trigger_analysis(self, query, context):
        """Handle trigger analysis"""
        message = """
🔍 **Analisis Trigger**

**Smart Trigger Detection Coming Soon!** 🎯

Fitur ini akan help identify dan analyze triggers dalam recovery journey:

**🧠 Trigger Analysis akan include:**
• **Automatic Trigger Detection** - AI-powered identification dari journal entries
• **Trigger Categories** - Emotional, situational, social, environmental triggers
• **Risk Assessment** - Severity rating untuk different triggers
• **Coping Strategy Matching** - Personalized tips untuk each trigger type
• **Prevention Planning** - Proactive strategies untuk anticipated triggers
• **Success Tracking** - Monitor progress dalam managing triggers

**📊 Analysis Features:**
• Trigger frequency charts
• Time-based trigger patterns
• Emotion-trigger correlations
• Success rate dalam handling triggers

**🛠️ Current Tools Available:**
• **Emergency Mode** - Immediate support saat trigger muncul
• **Coping Tips** - Strategies untuk manage urges
• **Daily Check-in** - Monitor emotional state
• **Journal Writing** - Document trigger experiences

**💪 Manual Trigger Awareness:**
• Note situasi yang challenging dalam journal
• Use emergency mode immediately saat urge muncul
• Practice coping strategies regularly
• Identify patterns dalam timing dan circumstances

**🎯 Build Trigger Awareness Now:**
1. Document trigger situations dalam journal
2. Use emergency mode untuk immediate help
3. Practice mindfulness untuk early detection
4. Build strong coping strategy toolkit

Emergency mode tersedia 24/7 untuk immediate trigger support!
        """
        
        await query.edit_message_text(
            message,
            reply_markup=BotKeyboards.journal_menu(),
            parse_mode='Markdown'
        )
    
    async def _journal_save_callback(self, query, context):
        """Handle journal save button callback"""
        user_info = get_user_info(query.from_user)
        user = self.user_service.get_or_create_user(**user_info)
        
        # Get journal text from context
        journal_text = context.user_data.get('journal_text')
        
        if not journal_text:
            app_logger.error(f"❌ No journal text found for user {user.telegram_id}")
            await query.edit_message_text(
                "❌ **Error: No journal text found**\n\n"
                "Please start again with journal menu.",
                reply_markup=BotKeyboards.journal_menu()
            )
            context.user_data.clear()
            return
        
        try:
            # Save to database using JournalService
            success = self.journal_service.create_journal_entry(
                telegram_id=user.telegram_id,
                entry_text=journal_text
            )
            
            if not success:
                app_logger.error(f"❌ Failed to save journal entry for user {user.telegram_id}")
                await query.edit_message_text(
                    "❌ **Error menyimpan journal entry**\n\n"
                    "Maaf, terjadi error saat menyimpan ke database.",
                    reply_markup=BotKeyboards.journal_menu()
                )
                return
            
            # Calculate stats
            from datetime import datetime
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            word_count = len(journal_text.split())
            char_count = len(journal_text)
            
            # Get user's total entries count
            total_entries = self.journal_service.get_entry_count(user.telegram_id)
            
            # Clear the state
            context.user_data.clear()
            
            # Log successful save
            app_logger.info(f"✅ Journal entry saved for user {user.telegram_id}: entry #{total_entries}")
            
            # Send success confirmation
            success_message = f"""
🎉 **Journal Entry Berhasil Disimpan!**

**📅 Detail Penyimpanan:**
• **Timestamp**: {timestamp}
• **Statistik**: {word_count} kata, {char_count} karakter
• **Entry ke**: #{total_entries}
• **Status**: ✅ Tersimpan dalam database

**📊 Progress Kamu:**
• **Total entries**: {total_entries} journal entries
• **Konsistensi**: Excellent work maintaining journaling habit!

**💡 Benefits yang kamu dapatkan:**
• **Self-awareness** - Better understanding of thoughts dan feelings
• **Progress tracking** - Documented recovery journey
• **Emotional processing** - Healthy outlet untuk feelings
• **Pattern recognition** - Data untuk identify triggers dan growth

**🏆 Achievement Unlocked**: {total_entries} journal entries completed! 💪✨
            """
            
            await query.edit_message_text(
                success_message, 
                reply_markup=BotKeyboards.journal_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            app_logger.error(f"💥 Exception saving journal entry for user {user.telegram_id}: {e}")
            await query.edit_message_text(
                "❌ **Error menyimpan journal entry**\n\n"
                "Maaf, terjadi error teknis.",
                reply_markup=BotKeyboards.journal_menu()
            )
            context.user_data.clear()
    
    async def _journal_cancel_callback(self, query, context):
        """Handle journal cancel button callback"""
        user_info = get_user_info(query.from_user)
        app_logger.info(f"🚫 Journal entry canceled by user {user_info['telegram_id']}")
        
        # Clear state
        context.user_data.clear()
        
        await query.edit_message_text(
            "🚫 **Journal Entry Dibatalkan**\n\n"
            "Entry tidak disimpan. Kamu bisa mulai menulis journal lagi kapan saja.",
            reply_markup=BotKeyboards.journal_menu(),
            parse_mode='Markdown'
        )
    
    async def _journal_edit_callback(self, query, context):
        """Handle journal edit button callback"""
        user_info = get_user_info(query.from_user)
        app_logger.info(f"✏️ Journal entry edit requested by user {user_info['telegram_id']}")
        
        # Reset to input mode
        context.user_data['state'] = 'input_journal'
        context.user_data['journal_step'] = 'waiting_for_text'
        context.user_data.pop('journal_text', None)  # Remove stored text
        
        await query.edit_message_text(
            "✏️ **Edit Journal Entry**\n\n"
            "Silakan ketik ulang journal entry kamu. Entry sebelumnya sudah dihapus.\n\n"
            "**⌨️ Ketik journal entry baru:**",
            parse_mode='Markdown'
        )
