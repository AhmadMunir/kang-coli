from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BotKeyboards:
    """Telegram inline keyboards untuk bot"""
    
    @staticmethod
    def main_menu():
        """Main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Cek Streak", callback_data="check_streak"),
                InlineKeyboardButton("💪 Motivasi", callback_data="get_motivation")
            ],
            [
                InlineKeyboardButton("📝 Check-in Harian", callback_data="daily_checkin"),
                InlineKeyboardButton("📖 Journal", callback_data="journal_menu")
            ],
            [
                InlineKeyboardButton("🆘 Mode Darurat", callback_data="emergency_mode"),
                InlineKeyboardButton("🎯 Tips Coping", callback_data="coping_tips")
            ],
            [
                InlineKeyboardButton("📚 Edukasi", callback_data="education_menu"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu")
            ],
            [
                InlineKeyboardButton("💔 Lapor Relapse", callback_data="report_relapse")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def settings_menu():
        """Settings menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔔 Reminder Settings", callback_data="reminder_settings"),
                InlineKeyboardButton("� Language / Bahasa", callback_data="language_settings")
            ],
            [
                InlineKeyboardButton("�🌍 Timezone", callback_data="timezone_settings"),
                InlineKeyboardButton("📊 Lihat Stats", callback_data="view_stats")
            ],
            [
                InlineKeyboardButton("🗑️ Reset Data", callback_data="reset_data"),
                InlineKeyboardButton("� Kembali", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def reminder_settings_menu():
        """Reminder settings keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Enable Daily Reminders", callback_data="enable_reminders"),
                InlineKeyboardButton("❌ Disable Reminders", callback_data="disable_reminders")
            ],
            [
                InlineKeyboardButton("⏰ Set Reminder Time", callback_data="set_reminder_time"),
                InlineKeyboardButton("� Reminder Frequency", callback_data="reminder_frequency")
            ],
            [
                InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def language_settings_menu():
        """Language settings keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_english"),
                InlineKeyboardButton("🇮🇩 Bahasa Indonesia", callback_data="lang_indonesian")
            ],
            [
                InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def reminder_frequency_menu():
        """Reminder frequency selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📅 Daily", callback_data="freq_daily"),
                InlineKeyboardButton("📊 Every 3 Days", callback_data="freq_3days")
            ],
            [
                InlineKeyboardButton("📈 Weekly", callback_data="freq_weekly"),
                InlineKeyboardButton("🎯 Custom", callback_data="freq_custom")
            ],
            [
                InlineKeyboardButton("🔙 Back to Reminders", callback_data="reminder_settings")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def emergency_menu():
        """Emergency mode keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🌊 Urge Surfing", callback_data="urge_surfing"),
                InlineKeyboardButton("🎯 Trigger Analysis", callback_data="trigger_analysis")
            ],
            [
                InlineKeyboardButton("💨 Immediate Distraction", callback_data="immediate_distraction"),
                InlineKeyboardButton("🧘 Mindfulness Protocol", callback_data="mindfulness_protocol")
            ],
            [
                InlineKeyboardButton("🆘 Emergency Contacts", callback_data="emergency_contacts"),
                InlineKeyboardButton("💬 Accountability Check", callback_data="accountability_check")
            ],
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def emergency_protocol_menu():
        """Emergency protocol keyboard with back to emergency option"""
        keyboard = [
            [
                InlineKeyboardButton("🆘 Kembali ke Emergency Mode", callback_data="emergency_mode"),
                InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def education_menu():
        """Education menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🧠 Dopamine & Recovery", callback_data="edu_dopamine"),
                InlineKeyboardButton("✨ Benefits NoFap", callback_data="edu_benefits")
            ],
            [
                InlineKeyboardButton("🔄 Neuroplasticity", callback_data="edu_neuroplasticity"),
                InlineKeyboardButton("📈 Recovery Timeline", callback_data="edu_timeline")
            ],
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def journal_menu():
        """Journal menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✍️ Tulis Entry Baru", callback_data="new_journal"),
                InlineKeyboardButton("📖 Baca Entries", callback_data="read_journal")
            ],
            [
                InlineKeyboardButton("🎯 Analisis Mood", callback_data="mood_analysis"),
                InlineKeyboardButton("🔍 Analisis Trigger", callback_data="trigger_journal")
            ],
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def journal_confirmation():
        """Journal entry confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💾 SIMPAN", callback_data="journal_save"),
                InlineKeyboardButton("✏️ EDIT", callback_data="journal_edit")
            ],
            [
                InlineKeyboardButton("🚫 BATAL", callback_data="journal_cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def coping_tips_menu():
        """Coping tips categories keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💪 Physical", callback_data="tips_physical"),
                InlineKeyboardButton("🧠 Mental", callback_data="tips_mental")
            ],
            [
                InlineKeyboardButton("🎯 Distraction", callback_data="tips_distraction"),
                InlineKeyboardButton("🧘 Mindfulness", callback_data="tips_mindfulness")
            ],
            [
                InlineKeyboardButton("📝 Productive", callback_data="tips_productive"),
                InlineKeyboardButton("🎲 Random Tip", callback_data="tips_random")
            ],
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirmation_keyboard(action: str):
        """Generic confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Ya", callback_data=f"confirm_{action}"),
                InlineKeyboardButton("❌ Tidak", callback_data=f"cancel_{action}")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def relapse_confirmation():
        """Relapse confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💔 Ya, Saya Relapse", callback_data="confirm_relapse"),
                InlineKeyboardButton("💪 Tidak, Masih Kuat", callback_data="cancel_relapse")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def mood_scale():
        """Mood scale keyboard (1-5)"""
        keyboard = []
        row = []
        for i in range(1, 6):  # Changed from 1-10 to 1-5
            row.append(InlineKeyboardButton(str(i), callback_data=f"mood_{i}"))
        keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_main():
        """Simple back to main menu keyboard"""
        keyboard = [[InlineKeyboardButton("🔙 Kembali ke Menu", callback_data="main_menu")]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_settings():
        """Back to settings keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
