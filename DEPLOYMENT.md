# Deployment Guide

## 🚀 Deployment Options

### 1. VPS Deployment (Recommended)

#### Requirements:
- Ubuntu 20.04+ or similar Linux distro
- Python 3.8+
- 1GB RAM minimum
- 10GB storage

#### Steps:

1. **Setup server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install git
sudo apt install git -y
```

2. **Clone and setup project:**
```bash
# Clone repository
git clone <repository-url>
cd pmo-recovery-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configuration:**
```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
# Add your BOT_TOKEN and other configurations
```

4. **Setup systemd service:**
```bash
# Create service file
sudo nano /etc/systemd/system/pmo-bot.service
```

Add this content:
```ini
[Unit] 
Description=PMO Recovery Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pmo-recovery-bot
Environment=PATH=/home/ubuntu/pmo-recovery-bot/venv/bin
ExecStart=/home/ubuntu/pmo-recovery-bot/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

5. **Start service:**
```bash
# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable pmo-bot
sudo systemctl start pmo-bot

# Check status
sudo systemctl status pmo-bot
```

### 2. Railway Deployment

1. **Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py"
  }
}
```

2. **Connect to Railway:**
- Login to railway.app
- Connect GitHub repository
- Add environment variables in Railway dashboard
- Deploy automatically

### 3. Heroku Deployment

1. **Create `Procfile`:**
```
worker: python main.py
```

2. **Create `runtime.txt`:**
```
python-3.10.11
```

3. **Deploy:**
```bash
# Install Heroku CLI
# Login and create app
heroku create pmo-recovery-bot

# Set environment variables
heroku config:set BOT_TOKEN=your_token_here

# Deploy
git push heroku main
```

### 4. Docker Deployment

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

2. **Create `docker-compose.yml`:**
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

3. **Deploy:**
```bash
# Build and run
docker-compose up -d
```

## 🔐 Security Best Practices

1. **Environment Variables:**
   - Never commit `.env` file
   - Use strong, unique tokens
   - Rotate tokens regularly

2. **Server Security:**
   - Setup firewall (UFW)
   - Use SSH keys instead of passwords
   - Keep system updated
   - Monitor logs regularly

3. **Database Security:**
   - Regular backups
   - Secure file permissions
   - Monitor database size

## 📊 Monitoring

1. **Logs monitoring:**
```bash
# View bot logs
tail -f logs/pmo_bot.log

# View system logs
sudo journalctl -u pmo-bot -f
```

2. **Health checks:**
```bash
# Check bot status
sudo systemctl status pmo-bot

# Check resource usage
htop
```

## 🔄 Maintenance

1. **Updates:**
```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart pmo-bot
```

2. **Backups:**
```bash
# Backup database
cp data/database.db backups/database_$(date +%Y-%m-%d).db

# Backup logs
tar -czf backups/logs_$(date +%Y-%m-%d).tar.gz logs/
```

## 🆘 Troubleshooting

### Common Issues:

1. **Bot not responding:**
   - Check token validity
   - Verify internet connection
   - Check bot logs

2. **Database errors:**
   - Check file permissions
   - Verify database path
   - Check disk space

3. **Memory issues:**
   - Monitor memory usage
   - Increase server resources
   - Optimize code if needed

### Getting Help:

- Check logs first: `tail -f logs/pmo_bot.log`
- Verify configuration: `.env` file
- Test locally before deploying
- Check Telegram Bot API status
