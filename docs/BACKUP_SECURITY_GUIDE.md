# Security Guide - Backup & Recovery System

## 🔐 Security Overview

Sistem backup PMO Recovery Bot dirancang dengan keamanan berlapis untuk melindungi data sensitif pengguna. Dokumen ini menjelaskan langkah-langkah keamanan yang harus diimplementasikan.

## 🛡️ Security Measures Implemented

### 1. Access Control
- **Admin-Only Access**: Hanya admin yang dapat mengakses fungsi backup/restore
- **User ID Verification**: Validasi ketat berdasarkan Telegram user ID
- **Command Authorization**: Setiap command backup memerlukan otorisasi admin
- **Callback Query Protection**: Semua callback query divalidasi

### 2. Data Protection
- **Integrity Checks**: Validasi integritas database sebelum dan sesudah backup
- **Secure File Handling**: Penggunaan temporary directories dengan cleanup otomatis
- **Encryption Ready**: Struktur siap untuk implementasi enkripsi
- **Metadata Protection**: Informasi sensitif tidak disimpan dalam metadata

### 3. Backup Security
- **ZIP Compression**: Semua backup dikompres untuk efisiensi dan keamanan
- **Secure Storage**: Backup disimpan di direktori dengan permission terbatas
- **Retention Policies**: Automatic cleanup untuk mencegah akumulasi data lama
- **Version Control**: Tracking versi backup untuk audit trail

## ⚙️ Security Configuration

### 1. Admin User Configuration
Edit file `src/bot/handlers/backup_handlers.py`:

```python
# CRITICAL: Update with your actual admin user IDs
ADMIN_USER_IDS = {
    123456789,  # Primary admin - Replace with your Telegram user ID
    987654321,  # Secondary admin (optional)
}

def is_admin(user_id: int) -> bool:
    """Enhanced admin verification with logging"""
    is_authorized = user_id in ADMIN_USER_IDS
    
    if not is_authorized:
        logger.warning(f"Unauthorized backup access attempt from user: {user_id}")
    
    return is_authorized
```

### 2. File System Security
```bash
# Set proper permissions for backup directories
chmod 700 backups/
chmod 700 recovery/
chmod 600 config/settings.py

# Restrict access to database
chmod 600 data/pmo_recovery.db
```

### 3. Environment Security
```bash
# Secure environment variables
export BOT_TOKEN="your_bot_token_here"  # Never hardcode in files
export ADMIN_USER_IDS="123456789,987654321"  # Optional: environment-based config

# Secure database path
export DATABASE_PATH="/secure/path/to/database.db"
```

## 🔒 Advanced Security Features

### 1. Backup Encryption (Recommended)
Add encryption to backup files:

```python
# Add to backup_service.py
import cryptography
from cryptography.fernet import Fernet

class SecureBackupService(BackupService):
    def __init__(self, encryption_key: bytes = None):
        super().__init__()
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
    
    async def create_encrypted_backup(self, backup_type: str):
        # Create regular backup
        success, backup_path = await self.create_full_backup(backup_type)
        
        if success:
            # Encrypt backup file
            encrypted_path = await self._encrypt_backup_file(backup_path)
            return True, encrypted_path
        
        return success, backup_path
    
    async def _encrypt_backup_file(self, backup_path: str) -> str:
        with open(backup_path, 'rb') as f:
            backup_data = f.read()
        
        encrypted_data = self.cipher.encrypt(backup_data)
        
        encrypted_path = backup_path.replace('.zip', '.encrypted')
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Remove unencrypted backup
        os.remove(backup_path)
        
        return encrypted_path
```

### 2. Audit Logging
Enhanced logging for security events:

```python
# Add to backup_handlers.py
import logging
from datetime import datetime

security_logger = logging.getLogger('security')

async def log_security_event(event_type: str, user_id: int, details: str = ""):
    """Log security-related events"""
    security_logger.info(f"SECURITY_EVENT: {event_type} | User: {user_id} | Details: {details} | Time: {datetime.now()}")

# Usage in handlers
await log_security_event("BACKUP_ACCESS_ATTEMPT", user_id, "Backup menu accessed")
await log_security_event("BACKUP_CREATED", user_id, f"Manual backup: {backup_path}")
await log_security_event("RESTORE_INITIATED", user_id, f"Restore from: {backup_file}")
```

### 3. IP Whitelisting (Server Level)
If running on server, implement IP whitelisting:

```bash
# UFW firewall rules
sudo ufw allow from YOUR_IP_ADDRESS to any port 22
sudo ufw allow from ADMIN_IP_1 to any port 8080
sudo ufw deny from any to any port 8080
```

## 🚨 Security Incident Response

### 1. Unauthorized Access Detection
```python
# Automatic security alerts for suspicious activity
async def detect_suspicious_activity(user_id: int):
    """Detect and respond to suspicious activity"""
    
    # Check for rapid successive backup attempts
    recent_attempts = await get_recent_backup_attempts(user_id)
    if len(recent_attempts) > 5:  # More than 5 attempts in 1 hour
        await alert_security_incident("RAPID_BACKUP_ATTEMPTS", user_id)
    
    # Check for unusual access patterns
    if user_id not in ADMIN_USER_IDS:
        await alert_security_incident("UNAUTHORIZED_ACCESS_ATTEMPT", user_id)

async def alert_security_incident(incident_type: str, user_id: int):
    """Alert administrators of security incidents"""
    message = f"🚨 SECURITY ALERT: {incident_type}\nUser ID: {user_id}\nTime: {datetime.now()}"
    
    for admin_id in ADMIN_USER_IDS:
        await context.bot.send_message(admin_id, message)
```

### 2. Emergency Security Procedures
```python
# Emergency backup lockdown
async def emergency_lockdown():
    """Emergency procedure to lock down backup system"""
    
    # Disable all backup functions
    global BACKUP_SYSTEM_ENABLED
    BACKUP_SYSTEM_ENABLED = False
    
    # Create emergency backup
    await backup_service.create_full_backup("emergency")
    
    # Alert all admins
    for admin_id in ADMIN_USER_IDS:
        await context.bot.send_message(
            admin_id, 
            "🚨 EMERGENCY LOCKDOWN ACTIVATED\nBackup system temporarily disabled"
        )
```

## 📋 Security Checklist

### Initial Setup
- [ ] Update `ADMIN_USER_IDS` with correct Telegram user IDs
- [ ] Set proper file system permissions
- [ ] Configure secure environment variables
- [ ] Test admin access verification
- [ ] Enable security logging

### Regular Maintenance
- [ ] Review admin access list monthly
- [ ] Monitor security logs weekly
- [ ] Test backup/restore process monthly
- [ ] Update dependencies regularly
- [ ] Rotate encryption keys (if using encryption)

### Security Monitoring
- [ ] Monitor failed backup attempts
- [ ] Check for unusual access patterns
- [ ] Review backup file integrity
- [ ] Audit admin activities
- [ ] Monitor disk space usage

## 🔍 Security Testing

### 1. Access Control Testing
```bash
# Test unauthorized access
python -c "
from src.bot.handlers.backup_handlers import is_admin
print('Unauthorized user test:', is_admin(999999999))  # Should be False
print('Authorized admin test:', is_admin(YOUR_ADMIN_ID))  # Should be True
"
```

### 2. Backup Integrity Testing
```bash
# Test backup integrity
python backup_manager.py backup --type manual
python backup_manager.py diagnose
```

### 3. Recovery Testing
```bash
# Test full recovery process
python tests/test_backup_system.py
```

## ⚠️ Security Warnings

### Critical Security Notes:
1. **Never commit admin user IDs to version control**
2. **Use environment variables for sensitive configuration**
3. **Regularly audit backup access logs**
4. **Test restore procedures in safe environment first**
5. **Keep backup files in secure locations**
6. **Monitor for unauthorized access attempts**
7. **Implement rate limiting for backup operations**
8. **Use encryption for sensitive backups**

### Common Security Mistakes:
- Hardcoding admin user IDs in public repositories
- Not setting proper file permissions
- Ignoring failed access attempt logs
- Not testing restore procedures
- Storing backups in unsecured locations
- Not implementing audit logging
- Using weak authentication methods

## 📞 Emergency Contacts

### Security Incident Response:
1. **Immediate Actions:**
   - Run emergency lockdown if needed
   - Create emergency backup
   - Review security logs
   - Identify breach scope

2. **Contact Procedures:**
   - Alert all admin users
   - Document incident details
   - Preserve evidence (logs, backups)
   - Follow incident response plan

### Recovery Procedures:
1. **Data Recovery:**
   - Use most recent clean backup
   - Verify backup integrity
   - Test restored data
   - Monitor for anomalies

2. **System Hardening:**
   - Review and update security measures
   - Change credentials if compromised
   - Update access controls
   - Implement additional monitoring

---

**🔒 Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update security measures based on new threats and requirements.
