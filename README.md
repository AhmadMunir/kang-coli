# PMO Recovery Coach Telegram Bot 🤖💪

Sebuah bot Telegram AI yang dirancang untuk membantu pengguna dalam proses recovery dari kebiasaan PMO (Pornography, Masturbation, Orgasm) dengan pendekatan yang empatis, suportif, dan berbasis bukti ilmiah.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Fitur Utama

### 📊 **Streak Tracking System**
- ✅ Real-time streak calculation
- 🏆 Longest streak records  
- 📈 Success rate analytics
- 🎯 Milestone celebrations dengan rewards
- 📅 Clean start date tracking

### 🌡️ **Mood Check-in & Analysis**
- 😊 Daily mood tracking (1-10 emoji scale)
- 📊 Energy, stress, sleep, and urge intensity tracking
- 📝 Personal notes & reflection
- 🧠 Pattern identification for triggers
- 🔄 Intelligent integration with broadcast system
- 📈 Comprehensive mood history & trends

### 💪 **Motivational Support**
- 📝 20+ inspirational quotes database
- 🌅 Daily motivation messages
- 🔥 Streak-based encouragement
- ✨ Recovery benefits timeline
- 💝 Supportive relapse recovery messages

### 🆘 **Emergency Intervention Mode**
- 🚨 Immediate crisis support
- 🌊 Urge surfing technique guide
- 🎯 Trigger analysis & prevention
- 🛡️ Multiple coping protocols
- 📞 Emergency contacts & resources

### 📚 **Educational Content**
- 🧠 Dopamine science & recovery
- 🔄 Neuroplasticity explanations
- ✨ NoFap benefits documentation
- 📈 Recovery timeline guidance
- 🔬 Evidence-based information

### 💾 **Advanced Backup & Recovery System**
- 🔄 Automated daily/weekly backups
- 📦 Manual backup creation
- 🚨 Emergency backup functionality
- 🔧 One-click data restore
- 📊 Database integrity monitoring
- ⚙️ Configurable retention policies
- 🛡️ Multiple backup formats (SQLite + JSON)

### �️ **Personalized Broadcast System**
- 🌅 Dynamic daily content
- 📚 Diverse message types (quotes, tips, facts, stories)
- 🎯 Day-specific focus areas
- 🌟 Motivational content rotation
- 🌡️ Smart mood check-in prompts
- 💬 Interactive engagement buttons

### �🎛️ **Smart Features**
- 🤖 Auto user registration
- 📝 Personal journaling system
- ✅ Daily check-ins
- 🌡️ Mood tracking integration
- ⚙️ Customizable settings
- 🔔 Optional daily reminders

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram Bot Token dari [@BotFather](https://t.me/BotFather)

### Installation
```bash
# 1. Clone repository
git clone https://github.com/AhmadMunir/kang-coli.githttps://github.com/AhmadMunir/kang-coli.git
cd pmo-recovery-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env dan tambahkan BOT_TOKEN

# 4. Setup backup system (optional)
python setup_backup_system.py

# 5. Test setup
python test_bot.py

# 6. Run bot
python main.py
```

**📖 Detailed guide:** [QUICKSTART.md](QUICKSTART.md)

## 🌡️ Fitur Mood Check-in

Sistem mood check-in adalah enhancement terbaru yang mengintegrasikan tracking mood dengan broadcast system.

### 🎯 Cara Kerja
1. **Daily broadcast** akan mendeteksi jika pengguna belum melakukan check-in mood
2. **Prompt dikirimkan** dengan pilihan quick check-in atau detailed check-in
3. **Skala mood 1-10** dengan emoji yang sesuai untuk pengalaman yang intuitif
4. **Feedback personalisasi** berdasarkan skor mood
5. **Opsional pendalaman** dengan energy, stress, sleep, dan urge tracking
6. **Data disimpan** untuk analisis pola dan tren

### 💡 Manfaat untuk Recovery
- **Awareness yang lebih baik** tentang faktor emotional dalam recovery
- **Identifikasi trigger** berdasarkan pola mood
- **Personalisasi intervensi** sesuai kebutuhan pengguna
- **Streak continuity** terlepas dari partisipasi mood check-in
- **Engagement yang lebih tinggi** dengan interaksi yang meaningful

**📖 Detail implementation:** [MOOD_CHECKIN_ENHANCEMENT.md](docs/MOOD_CHECKIN_ENHANCEMENT.md)

## 📁 Struktur Project

```
pmo-recovery-bot/
├── main.py                   # Entry point aplikasi
├── run_bot.py                # Script untuk menjalankan bot
├── requirements.txt          # Dependencies Python
├── requirements-dev.txt      # Dependencies untuk development
├── .env.example              # Template environment variables
├── .gitignore                # Git ignore file
├── README.md                 # Dokumentasi project
├── QUICKSTART.md             # Panduan memulai
├── CONTRIBUTING.md           # Panduan kontribusi
├── DEPLOYMENT.md             # Panduan deployment
├── LICENSE                   # Lisensi project
├── config/
│   └── settings.py           # Konfigurasi aplikasi
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers/         # Bot handlers (command, callback, message)
│   │   └── keyboards/        # Inline keyboards & markup
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py       # Database connection & session
│   │   └── models.py         # SQLAlchemy models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── broadcast_service.py     # Personalized broadcast system
│   │   ├── backup_service.py        # Backup & recovery management
│   │   ├── emergency_service.py     # Crisis intervention
│   │   ├── journal_service.py       # Journaling functionality
│   │   ├── motivational_service.py  # Quotes & encouragement
│   │   ├── streak_service.py        # Streak calculations
│   │   └── user_service.py          # User management & mood tracking
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py        # Helper functions
│       └── logger.py         # Custom logging setup
├── data/
│   ├── database.db           # SQLite database
│   ├── quotes.json           # Quotes database
│   └── tips.json             # Tips & coping strategies
├── docs/
│   ├── ADMIN_GUIDE.md                  # Admin documentation
│   ├── MOOD_CHECKIN_ENHANCEMENT.md     # Mood check-in feature docs
│   └── BROADCAST_SYSTEM_SUMMARY.md     # Broadcast system docs
├── logs/
│   ├── pmo_bot.log           # Application logs
│   └── errors.log            # Error logs
├── backups/                  # Automated & manual backups
└── tests/
    ├── __init__.py
    ├── test_broadcast_mood.py     # Broadcast with mood check-in tests
    ├── test_mood_enhancement.py   # Mood tracking feature tests
    └── [other test files]         # Various component tests
│   │   ├── handlers/     # Bot message handlers
│   │   ├── keyboards/    # Inline keyboards
│   │   └── middleware/   # Bot middleware
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py     # Database models
│   │   └── database.py   # Database connection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py      # User management
│   │   ├── streak_service.py    # Streak calculation
│   │   ├── motivational_service.py # Quotes & tips
│   │   ├── backup_service.py    # Backup & restore
│   │   ├── backup_scheduler.py  # Automated backups
│   │   └── emergency_service.py # Emergency mode
│   └── utils/
│       ├── __init__.py
│       ├── logger.py     # Logging configuration
│       ├── helpers.py    # Helper functions
│       ├── recovery_tool.py # Database recovery
│       └── constants.py  # App constants
├── backups/             # Automatic backups storage
│   ├── daily/          # Daily backups
│   ├── weekly/         # Weekly backups
│   ├── manual/         # Manual backups
│   └── emergency/      # Emergency backups
├── recovery/           # Recovery tools & reports
├── backup_manager.py   # CLI backup management
├── backup_manager.bat  # Windows backup script
├── setup_backup_system.py # Backup system setup
│   │   └── emergency_service.py # Emergency mode
│   └── utils/
│       ├── __init__.py
│       ├── logger.py     # Logging configuration
│       ├── helpers.py    # Helper functions
│       └── constants.py  # App constants
└── data/
    ├── quotes.json       # Motivational quotes
    ├── tips.json         # Coping strategies
    └── database.db       # SQLite database
```

## 🤖 Cara Menggunakan Bot

1. Start bot dengan mengirim `/start`
2. Setup profil recovery dengan `/setup`
3. Laporkan relapse dengan `/relapse`
4. Cek streak dengan `/streak`
5. Dapatkan motivasi dengan `/motivation`
6. Mode darurat dengan `/emergency`
7. Check-in harian dengan `/checkin`
8. Mood tracking dengan `/mood`
9. Jurnal pribadi dengan `/journal`
10. **Backup management (Admin)** dengan `/backup`

### 💾 Data Backup & Recovery
- **Automated Backups**: Daily (3AM) & Weekly (Sunday 2AM)
- **Manual Backups**: Create anytime via `/backup` command
- **CLI Management**: Use `python backup_manager.py` or `backup_manager.bat`
- **One-Click Restore**: Full data recovery from any backup
- **Health Monitoring**: Automatic database integrity checks

## 🛠️ Development

### Prerequisites
- Python 3.8+
- pip
- SQLite3

### Running in Development
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with debug mode
python main.py --debug
```

## 🧪 Testing

Comprehensive test suite tersedia untuk verify functionality dan ensure quality. Semua test files telah diorganisir dalam folder `tests/` untuk struktur yang lebih rapi.

### Test Structure
```
tests/
├── 🚀 Quick Tests
│   ├── quick_check.py           # Simple import dan dependency check
│   ├── quick_test.py            # Quick functionality verification  
│   └── simple_test.py           # Basic import testing
├── 🤖 Bot Tests
│   ├── test_bot.py              # General bot functionality
│   ├── test_handlers.py         # Message handlers testing
│   ├── test_emergency.py        # Emergency mode testing
│   └── test_emergency_nav.py    # Emergency navigation testing
├── 💾 **Backup System Tests**
│   ├── test_backup_system.py    # Complete backup system testing
│   ├── test_backup_creation.py  # Backup creation functionality
│   ├── test_restore_process.py  # Data restore verification
│   └── test_database_recovery.py # Database repair testing
└── 🌡️ **Mood & Broadcast Tests**
    ├── test_broadcast_mood.py    # Broadcast with mood check-in tests
    ├── test_mood_enhancement.py  # Mood check-in feature tests
    └── test_mood_analysis.py     # Mood data analysis testing

## 📋 Changelog

### v1.3.0 (August 2025)
- ✨ **Added:** Mood check-in enhancement
- 🌟 **Added:** Enhanced broadcast system with personalized content
- 🔄 **Improved:** Logger implementation unified across modules
- 📊 **Added:** User statistics reporting tools
- 🎯 **Improved:** Testing structure organization
- 📝 **Updated:** Documentation

### v1.2.0 (July 2025)
- 💾 **Added:** Advanced backup & recovery system
- 🚨 **Added:** Emergency backup functionality 
- 🔧 **Added:** One-click restore process
- 📊 **Added:** Database integrity monitoring

### v1.1.0 (June 2025)
- 📝 **Added:** Journal system
- 🎯 **Added:** Trigger analysis
- 🆘 **Improved:** Emergency intervention system
- 📈 **Improved:** Streak analytics

### v1.0.0 (May 2025)
- 🚀 Initial release

## 📞 Contact & Support

For questions, support, or contributions, please contact:
- **Developer:** Ahmad Munir
- **Email:** developer@example.com
- **GitHub:** [AhmadMunir](https://github.com/AhmadMunir)
- **Support Group:** [t.me/PMORecoveryBotSupport](https://t.me/PMORecoveryBotSupport)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
│   └── test_handlers.py         # Handler functionality testing
├── 🆘 Emergency Tests
│   ├── test_emergency.py        # Emergency callback routing
│   ├── test_emergency_nav.py    # Emergency navigation enhancement
│   └── test_enhanced_emergency_protocols.py  # Enhanced protocols
├── 📊 Database Tests
│   ├── test_direct_database.py  # Database connectivity tests
│   └── test_journal_database.py # Journal-specific DB operations  
├── 📝 Journal Tests
│   ├── test_journal.py          # JournalService methods
│   ├── test_complete_journal.py # Complete journal workflow
│   └── test_journal_handlers.py # Journal callback handlers
└── 📋 Test Runners
    ├── run_all_tests.py         # Master test runner
    └── run_category_tests.py    # Category-specific runner
```

### Running Tests
```bash
# Run all tests dengan master runner
python tests/run_all_tests.py

# Run tests by category
python tests/run_category_tests.py quick     # Quick tests only
python tests/run_category_tests.py bot       # Bot functionality tests
python tests/run_category_tests.py emergency # Emergency system tests
python tests/run_category_tests.py database  # Database tests
python tests/run_category_tests.py journal   # Journal functionality tests

# Run individual tests
python tests/test_bot.py                     # Single test file
python tests/test_direct_database.py
python tests/test_complete_journal_workflow.py
python tests/test_journal_handlers.py

# Run with pytest (if installed)
pytest tests/ -v
```

### Test Coverage
- ✅ **Database Operations**: SQLite connectivity, CRUD operations, schema validation
- ✅ **Service Layer**: Business logic, data validation, error handling
- ✅ **Bot Handlers**: User interaction, state management, message processing
- ✅ **Integration**: End-to-end workflows, component integration
- ✅ **Quality Assurance**: Error recovery, data integrity, user experience

### Test Reports
Recent test results menunjukkan:
- 💾 Database storage: ✅ Working
- 📝 Journal system: ✅ Working
- 🤖 Bot handlers: ✅ Working
- 📊 Statistics: ✅ Working
- 🔄 Workflows: ✅ Working

## 📝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Bot ini dirancang sebagai alat bantu dan tidak menggantikan konsultasi profesional. Jika Anda mengalami masalah serius terkait kecanduan, disarankan untuk mencari bantuan profesional.

## 🤝 Support

Jika Anda memiliki pertanyaan atau butuh bantuan:
- Buka Issue di GitHub
- Hubungi maintainer

---

**Ingat: Recovery adalah perjalanan, bukan destinasi. Setiap hari adalah kesempatan baru untuk menjadi lebih baik.**
