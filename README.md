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

### 🎛️ **Smart Features**
- 🤖 Auto user registration
- 📝 Personal journaling system
- ✅ Daily check-ins
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

# 4. Test setup
python test_bot.py

# 5. Run bot
python main.py
```

**📖 Detailed guide:** [QUICKSTART.md](QUICKSTART.md)

## 📁 Struktur Project

```
pmo-recovery-bot/
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Dependencies Python
├── .env.example           # Template environment variables
├── .gitignore            # Git ignore file
├── README.md             # Dokumentasi project
├── config/
│   └── settings.py       # Konfigurasi aplikasi
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
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
│   ├── test_bot.py              # Comprehensive bot setup testing
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
