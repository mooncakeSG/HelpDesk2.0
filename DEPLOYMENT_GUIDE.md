# 🚀 IT Helpdesk System - Deployment Guide

## 📋 **System Overview**
Your IT Helpdesk system consists of:
- **Main Application**: Flask app with SQLiteCloud database (Port 5000)
- **Email Service**: Flask-Mail notification system (Port 5001)
- **Features**: Ticket submission, agent portal, priority management, email notifications

## 🌐 **Deployment Options**

### **1. Cloud Platform Deployment (Recommended)**

#### **A. Heroku (Easiest)**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile
echo "worker: python email_notifications.py" >> Procfile

# Deploy
git init
git add .
git commit -m "Initial deployment"
heroku create your-helpdesk-app
heroku config:set SQLITECLOUD_API_KEY=your_key
heroku config:set SQLITECLOUD_URL=your_url
heroku config:set MAIL_USERNAME=your_email
heroku config:set MAIL_PASSWORD=your_app_password
heroku config:set NOTIFY_EMAILS=team1@company.com,team2@company.com
git push heroku main
```

#### **B. Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway add
railway deploy
```

#### **C. Render**
```yaml
# render.yaml
services:
  - type: web
    name: helpdesk-main
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: SQLITECLOUD_API_KEY
        value: your_key
      - key: MAIL_USERNAME
        value: your_email
      - key: MAIL_PASSWORD
        value: your_app_password

  - type: worker
    name: helpdesk-email
    env: python
    buildCommand: pip install -r email_requirements.txt
    startCommand: python email_notifications.py
```

#### **D. DigitalOcean App Platform**
```yaml
# .do/app.yaml
name: it-helpdesk
services:
- name: web
  source_dir: /
  github:
    repo: your-username/helpdesk
    branch: main
  run_command: python app.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SQLITECLOUD_API_KEY
    value: your_key
  - key: MAIL_USERNAME
    value: your_email

- name: email-service
  source_dir: /
  github:
    repo: your-username/helpdesk
    branch: main
  run_command: python email_notifications.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

### **2. VPS/Server Deployment**

#### **A. Ubuntu/Debian Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx supervisor -y

# Create application directory
sudo mkdir -p /var/www/helpdesk
cd /var/www/helpdesk

# Clone your repository
git clone https://github.com/your-username/helpdesk.git .

# Install Python dependencies
pip3 install -r requirements.txt
pip3 install -r email_requirements.txt

# Create systemd services
sudo nano /etc/systemd/system/helpdesk-main.service
sudo nano /etc/systemd/system/helpdesk-email.service

# Configure Nginx
sudo nano /etc/nginx/sites-available/helpdesk

# Start services
sudo systemctl enable helpdesk-main
sudo systemctl enable helpdesk-email
sudo systemctl start helpdesk-main
sudo systemctl start helpdesk-email
```

#### **B. Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt email_requirements.txt ./
RUN pip install -r requirements.txt -r email_requirements.txt

COPY . .

EXPOSE 5000 5001

CMD ["sh", "-c", "python email_notifications.py & python app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  helpdesk-main:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SQLITECLOUD_API_KEY=${SQLITECLOUD_API_KEY}
      - SQLITECLOUD_URL=${SQLITECLOUD_URL}
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
      - NOTIFY_EMAILS=${NOTIFY_EMAILS}
    command: python app.py

  helpdesk-email:
    build: .
    ports:
      - "5001:5001"
    environment:
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
      - NOTIFY_EMAILS=${NOTIFY_EMAILS}
    command: python email_notifications.py

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - helpdesk-main
      - helpdesk-email
```

### **3. Local Network Deployment**

#### **A. Windows Server**
```powershell
# Install Python
# Download and install Python 3.11+

# Install dependencies
pip install -r requirements.txt
pip install -r email_requirements.txt

# Create Windows Services
sc create "HelpdeskMain" binPath="python C:\path\to\app.py" start=auto
sc create "HelpdeskEmail" binPath="python C:\path\to\email_notifications.py" start=auto

# Start services
sc start HelpdeskMain
sc start HelpdeskEmail
```

#### **B. Raspberry Pi**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip -y

# Install dependencies
pip3 install -r requirements.txt
pip3 install -r email_requirements.txt

# Create startup script
sudo nano /etc/systemd/system/helpdesk.service

# Enable and start
sudo systemctl enable helpdesk
sudo systemctl start helpdesk
```

## 🔧 **Configuration Files**

### **Nginx Configuration**
```nginx
# /etc/nginx/sites-available/helpdesk
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /email/ {
        proxy_pass http://localhost:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Systemd Service Files**
```ini
# /etc/systemd/system/helpdesk-main.service
[Unit]
Description=IT Helpdesk Main Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/helpdesk
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/helpdesk-email.service
[Unit]
Description=IT Helpdesk Email Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/helpdesk
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 email_notifications.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔒 **Security Considerations**

### **Environment Variables**
```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-super-secret-key
export SQLITECLOUD_API_KEY=your-api-key
export SQLITECLOUD_URL=your-database-url
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
export NOTIFY_EMAILS=team1@company.com,team2@company.com
```

### **SSL/HTTPS Setup**
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### **Firewall Configuration**
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Or iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 📊 **Monitoring & Maintenance**

### **Log Management**
```bash
# Create log directories
sudo mkdir -p /var/log/helpdesk
sudo chown www-data:www-data /var/log/helpdesk

# Log rotation
sudo nano /etc/logrotate.d/helpdesk
```

### **Health Checks**
```bash
# Create health check script
#!/bin/bash
curl -f http://localhost:5000/ || exit 1
curl -f http://localhost:5001/health || exit 1
```

### **Backup Strategy**
```bash
# Database backup (if using local SQLite)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/helpdesk/tickets.db /backup/tickets_$DATE.db
```

## 💰 **Cost Comparison**

| Platform | Monthly Cost | Features | Best For |
|----------|-------------|----------|----------|
| **Heroku** | $7-25 | Easy deployment, auto-scaling | Small teams |
| **Railway** | $5-20 | Modern platform, good DX | Startups |
| **Render** | $7-25 | Free tier available | Budget-conscious |
| **DigitalOcean** | $12-24 | Full control, VPS | Growing teams |
| **AWS/GCP** | $10-50+ | Enterprise features | Large organizations |
| **VPS** | $5-20 | Full control, custom setup | Technical teams |

## 🚀 **Quick Start Deployment**

### **Option 1: Heroku (5 minutes)**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create apps
heroku create your-helpdesk-main
heroku create your-helpdesk-email

# Set environment variables
heroku config:set SQLITECLOUD_API_KEY=your_key -a your-helpdesk-main
heroku config:set MAIL_USERNAME=your_email -a your-helpdesk-email
heroku config:set MAIL_PASSWORD=your_app_password -a your-helpdesk-email

# Deploy
git push heroku main
```

### **Option 2: Railway (3 minutes)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway add
railway deploy
```

## 📞 **Support & Troubleshooting**

### **Common Issues**
1. **Port conflicts**: Ensure ports 5000 and 5001 are available
2. **Environment variables**: Check all required variables are set
3. **Email delivery**: Verify Gmail App Password and SMTP settings
4. **Database connection**: Test SQLiteCloud API connectivity

### **Debug Commands**
```bash
# Check service status
systemctl status helpdesk-main
systemctl status helpdesk-email

# View logs
journalctl -u helpdesk-main -f
journalctl -u helpdesk-email -f

# Test connectivity
curl http://localhost:5000/
curl http://localhost:5001/health
```

## 🎯 **Recommended Deployment Path**

### **For Small Teams (1-10 users)**
1. **Start with**: Heroku or Railway
2. **Cost**: $10-20/month
3. **Setup time**: 10 minutes

### **For Medium Teams (10-50 users)**
1. **Start with**: DigitalOcean App Platform
2. **Cost**: $20-40/month
3. **Setup time**: 30 minutes

### **For Large Teams (50+ users)**
1. **Start with**: AWS/GCP with load balancer
2. **Cost**: $50-200/month
3. **Setup time**: 2-4 hours

Choose the deployment option that best fits your team size, budget, and technical requirements!
