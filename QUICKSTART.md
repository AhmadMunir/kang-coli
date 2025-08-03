# Quick Start Guide - PMO Recovery Coach Bot

## 🚀 Quick Setup (5 menit)

### 1. Prerequisites
- Python 3.8+ installed
- Telegram account
- Basic command line knowledge

### 2. Get Bot Token
1. Open Telegram dan cari `@BotFather`
2. Kirim `/newbot`
3. Ikuti instruksi untuk buat bot baru
4. Copy token yang diberikan

### 3. Setup Project
```bash
# Clone/download project
cd pmo-recovery-bot

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dan tambahkan BOT_TOKEN kamu
```

### 4. Run Bot
```bash
# Test setup
python test_bot.py

# Run bot
python main.py
```

### 5. Test Bot
1. Buka Telegram
2. Cari username bot kamu
3. Kirim `/start`
4. Bot akan respond dengan menu utama

## 🎯 Core Features Terimplmentasi

### ✅ Streak Tracking
- **Current streak** calculation
- **Longest streak** record
- **Success rate** analytics
- **Milestone** celebrations

### ✅ Motivational Support  
- **Daily quotes** dari database
- **Streak encouragement** berdasarkan progress
- **Recovery benefits** info per tahap
- **Positive messaging** di semua interaksi

### ✅ Emergency Mode
- **Immediate intervention** protocols
- **Urge surfing** technique guide
- **Trigger analysis** dan prevention
- **Emergency contacts** resources
- **Coping strategies** by category

### ✅ Educational Content
- **Dopamine science** dan recovery process
- **Neuroplasticity** explanation
- **Benefits timeline** informasi
- **Recovery phases** guidance

### ✅ User Management
- **Auto user registration** saat first interaction
- **Streak calculation** real-time
- **Relapse recording** dengan support messages
- **User preferences** (reminders, timezone)

### ✅ Data Persistence
- **SQLite database** untuk local storage
- **User data** tracking
- **Journal entries** storage
- **Relapse history** records
- **Check-in data** tracking

## 🏗️ Architecture Overview

```
pmo-recovery-bot/
├── main.py              # Entry point
├── config/settings.py   # Configuration
├── src/
│   ├── database/        # Data models & DB connection
│   ├── services/        # Business logic
│   ├── bot/            # Telegram handlers & keyboards
│   └── utils/          # Helper functions
├── data/               # JSON data files
└── logs/              # Application logs
```

## 🔧 Customization

### Adding New Quotes
Edit `data/quotes.json`:
```json
{
  "text": "Your new motivational quote",
  "author": "Author Name"
}
```

### Adding New Tips
Edit `data/tips.json`:
```json
{
  "category": "physical",
  "title": "New Technique",
  "description": "How to do it...",
  "duration": "10-15 menit"
}
```

### Modifying Bot Messages
- Edit handlers di `src/bot/handlers/`
- Ubah keyboard layout di `src/bot/keyboards/`
- Customize constants di `src/utils/constants.py`

## 🚨 Troubleshooting

### Bot tidak respond?
1. Check BOT_TOKEN di `.env`
2. Verify internet connection
3. Check logs di `logs/pmo_bot.log`

### Database errors?
1. Check file permissions
2. Ensure `data/` directory exists
3. Run `python test_bot.py`

### Import errors?
1. Check Python version (3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check virtual environment

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot & show main menu |
| `/help` | Show help information |
| `/streak` | Check current streak |
| `/motivation` | Get daily motivation |
| `/emergency` | Emergency mode untuk urges |
| `/relapse` | Report relapse (with confirmation) |
| `/stats` | View detailed statistics |

## 🔐 Privacy & Security

- **Local storage** - data tersimpan di device kamu
- **No cloud sync** - data tidak dikirim ke server lain  
- **Secure tokens** - environment variables untuk sensitive data
- **User consent** - clear communication about data usage

## 🎨 Next Steps

Setelah bot running, kamu bisa:

1. **Test semua fitur** - coba setiap menu dan command
2. **Customize content** - edit quotes dan tips sesuai preferensi
3. **Deploy ke server** - ikuti `DEPLOYMENT.md` guide
4. **Add features** - lihat `CONTRIBUTING.md` untuk development
5. **Share feedback** - report bugs atau request features

## 💝 Support the Project

Bot ini dibuat untuk membantu community recovery. Jika helpful:

- ⭐ **Star** repository
- 🐛 **Report bugs** via Issues
- 💡 **Suggest features** via Discussions  
- 🤝 **Contribute** code atau content
- 📢 **Share** dengan yang membutuhkan

---

**Remember**: Recovery adalah journey, bukan destination. Bot ini adalah tool untuk membantu, tapi kekuatan sejati ada di dalam diri kamu. Stay strong! 💪
