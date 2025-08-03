# Backup and Restore System - PMO Recovery Bot

## 📋 Overview

Sistem backup dan restore yang komprehensif untuk PMO Recovery Bot, dirancang untuk melindungi data pengguna dari kehilangan dan memastikan keamanan data dengan recovery yang mudah.

## ✨ Fitur Utama

### 🔄 Automated Backup System
- **Daily Backup**: Backup otomatis harian pada pukul 03:00
- **Weekly Backup**: Backup mingguan setiap hari Minggu pukul 02:00  
- **Manual Backup**: Backup manual yang dapat dibuat kapan saja
- **Emergency Backup**: Backup darurat untuk situasi kritis

### 🛡️ Data Protection
- **Database Integrity Checks**: Validasi integritas database sebelum dan sesudah backup
- **Multiple Backup Formats**: SQLite database + JSON export untuk keamanan ganda
- **Metadata Tracking**: Informasi lengkap setiap backup (waktu, ukuran, jumlah user, dll)
- **Retention Policy**: Penghapusan otomatis backup lama sesuai kebijakan

### 🔧 Recovery Tools  
- **Database Diagnosis**: Deteksi otomatis masalah database
- **Automatic Repair**: Perbaikan otomatis database yang rusak
- **Data Export**: Export data ke format JSON yang mudah dibaca
- **Restore Validation**: Validasi backup sebelum restore

### 📊 Monitoring & Management
- **Real-time Status**: Status sistem backup dan scheduler
- **Backup Statistics**: Statistik backup yang detail
- **Admin Interface**: Interface Telegram untuk management backup
- **Command-line Tools**: Tools CLI untuk management server

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Admin Access
Edit file `src/bot/handlers/backup_handlers.py`:
```python
ADMIN_USER_IDS = {
    123456789,  # Your Telegram User ID
    987654321,  # Another admin if needed
}
```

### 3. Create Backup Directories
```bash
mkdir -p backups/{daily,weekly,manual,emergency}
mkdir -p recovery
```

## 📱 Telegram Commands (Admin Only)

### `/backup` - Main Backup Menu
Menampilkan menu utama backup management dengan opsi:
- 📦 Create Manual Backup
- 🔄 Create Emergency Backup  
- 📋 List Backups
- 📊 Backup Status
- ⚙️ Scheduler Settings
- 🔧 Restore Menu

### Example Usage:
```
/backup
```

## 💻 Command Line Tools

### Backup Manager Script
```bash
python backup_manager.py [command] [options]
```

#### Available Commands:

**Create Backup:**
```bash
python backup_manager.py backup --type manual
python backup_manager.py backup --type emergency
```

**List Backups:**
```bash
python backup_manager.py list
```

**System Status:**
```bash
python backup_manager.py status
```

**Database Diagnosis:**
```bash
python backup_manager.py diagnose
```

**Restore from Backup:**
```bash
python backup_manager.py restore path/to/backup.zip --confirm
```

**Start Scheduler:**
```bash
python backup_manager.py scheduler
```

### Windows Batch File
Untuk pengguna Windows, jalankan:
```cmd
backup_manager.bat
```

## 📂 Directory Structure

```
backups/
├── daily/          # Daily backups (7 days retention)
├── weekly/         # Weekly backups (4 weeks retention)  
├── manual/         # Manual backups (10 backups retention)
└── emergency/      # Emergency backups (3 backups retention)

recovery/
├── data_export_*/  # Exported data for recovery
├── recovered_*.db  # Recovered database files
└── *.json         # Recovery reports
```

## 🔄 Backup Process

### 1. Pre-Backup Validation
- Database integrity check
- Disk space validation
- Permission verification

### 2. Data Collection
- **Database**: SQLite file + SQL export + JSON export
- **Configuration**: settings.py, requirements.txt
- **Data Files**: quotes.json, tips.json
- **Recent Logs**: Last 30 days of log files

### 3. Backup Creation
- Create temporary directory
- Copy all files with verification
- Generate metadata
- Create ZIP archive
- Cleanup temporary files

### 4. Post-Backup Tasks
- Verify backup integrity
- Update backup statistics
- Cleanup old backups per retention policy
- Log backup completion

## 🛠️ Recovery Scenarios

### Scenario 1: Database Corruption
```bash
# 1. Diagnose the issue
python backup_manager.py diagnose

# 2. Attempt automatic repair
# (This will be suggested in diagnosis)

# 3. If repair fails, restore from backup
python backup_manager.py restore backups/daily/latest_backup.zip --confirm
```

### Scenario 2: Complete Data Loss
```bash
# 1. Check available backups
python backup_manager.py list

# 2. Restore from most recent backup
python backup_manager.py restore backups/emergency/backup_file.zip --confirm
```

### Scenario 3: Partial Data Recovery
```bash
# 1. Export recoverable data
python backup_manager.py diagnose
# This creates JSON exports in recovery/ directory

# 2. Manual data import (if needed)
# Use the exported JSON files to manually recover data
```

## ⚙️ Configuration

### Backup Schedule
Edit `src/services/backup_scheduler.py` untuk mengubah jadwal:
```python
# Daily backup at 3 AM
schedule.every().day.at("03:00").do(self._run_daily_backup)

# Weekly backup on Sunday at 2 AM  
schedule.every().sunday.at("02:00").do(self._run_weekly_backup)
```

### Retention Policy
Edit backup retention di `backup_service.py`:
```python
retention_days = {
    "daily": 7,      # Keep 7 daily backups
    "weekly": 4,     # Keep 4 weekly backups
    "manual": 10,    # Keep 10 manual backups
    "emergency": 3   # Keep 3 emergency backups
}
```

## 📊 Monitoring

### System Status Check
```bash
python backup_manager.py status
```

Output example:
```
📊 Backup System Status

🗄️ DATABASE:
  Path: data/pmo_recovery.db
  Exists: ✅ Yes
  Size: 2.34 MB
  Integrity: ✅ OK

💾 BACKUPS:
  Total backups: 15
  Storage used: 45.67 MB

🕒 LATEST BACKUP:
  Type: Daily
  Created: 2025-08-03 03:00:15
  Size: 2.89 MB

⚙️ SCHEDULER:
  Status: 🟢 Running
  Successful backups: 25
  Failed backups: 0
  Next daily backup: 2025-08-04 03:00:00
```

### Database Health Check
```bash
python backup_manager.py diagnose
```

## 🚨 Emergency Procedures

### Quick Emergency Backup
```bash
python backup_manager.py backup --type emergency
```

### Immediate Data Export (if database is corrupted)
```bash
python backup_manager.py diagnose
# Check recovery/ directory for exported data
```

### Fast Restore from Latest Backup
```bash
# Find latest backup
python backup_manager.py list

# Restore (replace with actual backup path)
python backup_manager.py restore backups/daily/pmo_recovery_backup_daily_20250803_030015.zip --confirm
```

## 📝 Best Practices

### 1. Regular Monitoring
- Check backup status weekly via `/backup` command
- Monitor log files for backup failures
- Verify database integrity monthly

### 2. Test Restore Process
- Test restore process quarterly with old backups
- Verify data integrity after restore
- Document any issues found

### 3. Multiple Backup Locations
- Consider copying critical backups to external storage
- Use cloud storage for additional redundancy
- Keep offline backups for maximum security

### 4. Admin Access Security
- Limit admin user IDs to trusted users only
- Regularly review admin access list
- Use strong authentication for server access

## 🔍 Troubleshooting

### Common Issues:

**1. Backup Creation Fails**
```bash
# Check disk space
df -h

# Check permissions
ls -la data/

# Check database integrity
python backup_manager.py diagnose
```

**2. Scheduler Not Running**
```bash
# Check scheduler status
python backup_manager.py status

# Restart scheduler
python backup_manager.py scheduler
```

**3. Restore Fails**
```bash
# Verify backup file
unzip -t backup_file.zip

# Check backup contents
unzip -l backup_file.zip

# Try manual extraction and inspection
```

**4. Database Corruption**
```bash
# Run full diagnosis
python backup_manager.py diagnose

# Attempt repair
# (Follow recommendations from diagnosis)

# Last resort: restore from backup
python backup_manager.py restore latest_backup.zip --confirm
```

## 📞 Support

### Log Files
- **Application logs**: `logs/pmo_bot.log`
- **Error logs**: `logs/errors.log`
- **Backup logs**: Check application logs for backup-related entries

### Recovery Reports
- Automatic recovery reports are saved in `recovery/` directory
- Contains detailed diagnosis and repair recommendations
- Include these reports when seeking support

## 🔄 Updates & Maintenance

### Regular Tasks:
1. **Weekly**: Check backup status and review logs
2. **Monthly**: Test restore process and verify integrity
3. **Quarterly**: Review and update retention policies
4. **Annually**: Update backup procedures and documentation

### System Updates:
- Keep Python and dependencies updated
- Test backup system after major updates
- Update documentation as needed

---

**⚠️ Important**: Always test backup and restore procedures in a safe environment before relying on them in production. Keep multiple backup copies and consider external/cloud storage for critical data protection.
