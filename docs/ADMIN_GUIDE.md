# 🔧 Admin Guide: Broadcast System

## Overview
Sistem broadcast memungkinkan admin untuk mengirim pesan harian, mingguan, dan custom kepada semua pengguna yang mengaktifkan daily reminders.

## Setup Admin Access

### 1. Mendapatkan Telegram User ID
Untuk mendapatkan User ID Telegram Anda:

1. Kirim pesan ke bot [@userinfobot](https://t.me/userinfobot)
2. Bot akan membalas dengan informasi termasuk User ID Anda
3. Copy angka User ID (contoh: `123456789`)

### 2. Set Environment Variable
Tambahkan User ID ke file `.env`:
```bash
ADMIN_USER_ID=123456789
```

### 3. Restart Bot
Restart bot untuk memuat konfigurasi admin:
```bash
python main.py
```

## Admin Commands

### 📡 Broadcast Management

#### `/adminhelp`
Menampilkan daftar semua command admin yang tersedia.

#### `/broadcastnow`
Mengirim daily broadcast secara langsung ke semua users yang mengaktifkan daily reminders.

**Example:**
```
/broadcastnow
```
**Output:** ✅ Daily broadcast sent to all users!

#### `/testbroadcast` 
Mengirim test broadcast hanya kepada admin untuk testing format dan konten.

**Example:**
```
/testbroadcast
```

#### `/custombroadcast <message>`
Mengirim pesan custom kepada semua users yang mengaktifkan daily reminders.

**Examples:**
```
/custombroadcast **Important Update** Bot akan maintenance selama 1 jam mulai pukul 14:00 WIB
/custombroadcast 🎉 **Congratulations!** Komunitas kita sudah mencapai 1000 users!
/custombroadcast ⚠️ **Reminder** Jangan lupa untuk daily check-in hari ini!
```

**Features:**
- Supports Markdown formatting (**bold**, *italic*)
- Supports emojis
- Automatic "Admin Announcement" header
- Reports success/failure counts

#### `/weeklysummary`
Mengirim weekly summary secara langsung ke semua users.

### 📊 Statistics & Monitoring

#### `/broadcaststats`
Menampilkan statistik broadcast system.

**Shows:**
- Jumlah users dengan daily reminders aktif
- Daftar scheduled jobs
- Next run time untuk setiap job

#### `/adminstats`
Menampilkan statistik admin yang detail.

**Shows:**
- Total users, active users, engagement rate
- Streak statistics (average, maximum, milestones)
- Recovery statistics (relapses, averages)
- System status information

## Scheduled Broadcasts

### Automatic Daily Schedule
Bot akan secara otomatis mengirim broadcast pada waktu-waktu berikut (configurable via .env):

- **Daily Broadcast**: 08:00 WIB (DAILY_REMINDER_TIME)
- **Afternoon Boost**: 15:00 WIB (AFTERNOON_BOOST_TIME)  
- **Evening Reflection**: 21:00 WIB (EVENING_REFLECTION_TIME)
- **Weekly Summary**: Sunday 10:00 WIB (WEEKLY_SUMMARY_DAY & TIME)

### Mengubah Jadwal
Edit file `.env` dan restart bot:
```bash
# Format: HH:MM (24-hour)
DAILY_REMINDER_TIME=09:00
AFTERNOON_BOOST_TIME=16:00
EVENING_REFLECTION_TIME=22:00

# Day: 0=Monday, 6=Sunday
WEEKLY_SUMMARY_DAY=6
WEEKLY_SUMMARY_TIME=11:00
```

## Content System

### Daily Broadcast Content
Setiap daily broadcast berisi:
- **Greeting & Date**: Personalized greeting dengan tanggal
- **Motivational Quote**: Quote inspiratif dari database
- **Daily Coping Strategy**: Tips praktis untuk recovery
- **Day-specific Content**: Konten khusus per hari (Monday Focus, Tuesday Tips, etc.)
- **Recovery Fact**: Fakta edukatif tentang recovery
- **Daily Inspiration**: Story inspiratif singkat
- **Call to Action**: Ajakan untuk action

### Day-Specific Themes
- **Monday**: 💪 Monday Motivation - Semangat memulai minggu
- **Tuesday**: 🎯 Tuesday Tips - Tips praktis dan actionable
- **Wednesday**: 🤝 Wednesday Wisdom - Kebijaksanaan dan insight
- **Thursday**: 💡 Thursday Thoughts - Refleksi dan mindfulness
- **Friday**: 🔥 Friday Focus - Fokus dan determination
- **Saturday**: 🌈 Saturday Self-Care - Self-care dan relaksasi
- **Sunday**: 🙏 Sunday Reflection - Refleksi dan planning

### Weekly Summary Content
Weekly summary berisi:
- **Week Reflection**: Review minggu yang berlalu
- **Weekly Planning Strategy**: Tips untuk planning minggu depan
- **Community Stats**: Statistik dan progress komunitas
- **Weekend Wisdom**: Tips khusus untuk weekend

## Best Practices

### 1. Testing Before Broadcasting
Selalu gunakan `/testbroadcast` sebelum mengirim broadcast besar:
```
/testbroadcast
```

### 2. Custom Message Guidelines
- Gunakan **bold** untuk judul important
- Gunakan emoji untuk visual appeal
- Keep message concise tapi informative
- Test format dengan `/testbroadcast` dulu

### 3. Monitoring Engagement
- Check `/broadcaststats` regular untuk monitor engagement
- Check `/adminstats` untuk insight user behavior
- Monitor logs untuk error atau issues

### 4. Scheduling Considerations
- Avoid broadcasting pada jam tidur (23:00-06:00)
- Consider timezone users (mayoritas Asia/Jakarta)
- Special events bisa override schedule normal

## Troubleshooting

### Common Issues

#### 1. "Unauthorized" Error
**Problem:** Command tidak work, show unauthorized  
**Solution:** 
- Pastikan ADMIN_USER_ID sudah set correct di .env
- Restart bot setelah update .env
- Check User ID dengan @userinfobot

#### 2. Broadcast Failed
**Problem:** Broadcast gagal terkirim  
**Solution:**
- Check bot token still valid
- Check network connectivity
- Monitor logs untuk specific error
- Test dengan `/testbroadcast` dulu

#### 3. No Users Receiving Messages
**Problem:** Broadcast sent tapi no users receive  
**Solution:**
- Check dengan `/broadcaststats` berapa users yang ada
- Users harus `/start` bot dulu dan enable daily reminders
- Check users belum block bot

#### 4. Scheduler Not Working
**Problem:** Automated broadcasts tidak jalan  
**Solution:**
- Check logs untuk scheduler errors
- Verify timezone setting di .env
- Restart bot to reinitialize scheduler

### Logs Monitoring
Monitor file `logs/app.log` untuk:
- Broadcast success/failure
- User interaction errors
- Scheduler execution
- Database issues

## Security Considerations

### Admin Access
- Hanya share ADMIN_USER_ID dengan trusted people
- Regularly monitor admin command usage
- Consider implementing command logging untuk audit

### Message Content
- Avoid sensitive information di broadcasts
- Follow content policy guidelines
- Test messages untuk ensure appropriate tone

### Rate Limiting
- Bot automatically handles Telegram rate limits
- Large broadcasts akan di-queue otomatis
- Monitor failed message counts

## Advanced Features

### Custom Scheduling (Future Enhancement)
Untuk custom scheduling, bisa extend `SchedulerService`:
```python
scheduler_service.schedule_custom_broadcast(
    message="Custom message",
    send_time="14:30",
    send_date="2024-01-15"
)
```

### Analytics Integration (Future Enhancement)
Untuk detailed analytics:
- Track message open rates  
- User engagement metrics
- A/B testing untuk message formats

---

## Quick Reference

### Essential Commands
```bash
/adminhelp          # Show all admin commands
/testbroadcast      # Test broadcast format
/broadcastnow       # Send daily broadcast now
/broadcaststats     # Check system stats
/custombroadcast <msg>  # Send custom message
```

### Configuration Files  
```bash
.env                # Environment variables
logs/app.log        # Application logs
data/quotes.json    # Motivational quotes
data/tips.json      # Coping strategies
```

### Support
Untuk questions atau issues, check:
1. Application logs
2. Database connectivity
3. Bot token validity
4. User permissions

---
**Last Updated:** August 2025  
**Version:** 1.0.0
