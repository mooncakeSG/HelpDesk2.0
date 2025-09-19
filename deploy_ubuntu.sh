#!/bin/bash
# Ubuntu Server Deployment Script for IT Helpdesk System

echo "🐧 Deploying IT Helpdesk on Ubuntu Server"
echo "========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
apt install -y python3 python3-pip python3-venv nginx supervisor curl git

# Create application directory
echo "📁 Creating application directory..."
mkdir -p /var/www/helpdesk
cd /var/www/helpdesk

# Get application files
echo "📥 Getting application files..."
if [ -d ".git" ]; then
    echo "Updating existing repository..."
    git pull
else
    echo "Please copy your application files to /var/www/helpdesk"
    echo "Or clone your repository:"
    echo "git clone https://github.com/your-username/helpdesk.git ."
    read -p "Press Enter when files are ready..."
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
pip install -r email_requirements.txt

# Create application user
echo "👤 Creating application user..."
useradd -r -s /bin/false helpdesk || echo "User already exists"
chown -R helpdesk:helpdesk /var/www/helpdesk

# Create systemd service files
echo "⚙️  Creating systemd services..."

# Main application service
cat > /etc/systemd/system/helpdesk-main.service << 'EOF'
[Unit]
Description=IT Helpdesk Main Application
After=network.target

[Service]
Type=simple
User=helpdesk
Group=helpdesk
WorkingDirectory=/var/www/helpdesk
Environment=PATH=/var/www/helpdesk/venv/bin
ExecStart=/var/www/helpdesk/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Email service
cat > /etc/systemd/system/helpdesk-email.service << 'EOF'
[Unit]
Description=IT Helpdesk Email Service
After=network.target

[Service]
Type=simple
User=helpdesk
Group=helpdesk
WorkingDirectory=/var/www/helpdesk
Environment=PATH=/var/www/helpdesk/venv/bin
ExecStart=/var/www/helpdesk/venv/bin/python email_notifications.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/helpdesk << 'EOF'
server {
    listen 80;
    server_name _;

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
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/helpdesk /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Create environment file
echo "⚙️  Creating environment configuration..."
cat > /var/www/helpdesk/.env << 'EOF'
# Database Configuration
SQLITECLOUD_API_KEY=your_sqlitecloud_api_key_here
SQLITECLOUD_URL=your_sqlitecloud_url_here

# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=IT Helpdesk <your_email@gmail.com>
NOTIFY_EMAILS=team1@company.com,team2@company.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
EOF

echo "Please update /var/www/helpdesk/.env with your actual configuration"
read -p "Press Enter when you've updated the .env file..."

# Set proper permissions
chown -R helpdesk:helpdesk /var/www/helpdesk
chmod 600 /var/www/helpdesk/.env

# Enable and start services
echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable helpdesk-main
systemctl enable helpdesk-email
systemctl enable nginx

systemctl start helpdesk-main
systemctl start helpdesk-email
systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
systemctl status helpdesk-main --no-pager
systemctl status helpdesk-email --no-pager
systemctl status nginx --no-pager

# Test endpoints
echo "🧪 Testing endpoints..."
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Main app is running on http://localhost:5000"
else
    echo "❌ Main app is not responding"
fi

if curl -f http://localhost:5001/health > /dev/null 2>&1; then
    echo "✅ Email service is running on http://localhost:5001"
else
    echo "❌ Email service is not responding"
fi

if curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ Nginx proxy is working on http://localhost"
else
    echo "❌ Nginx proxy is not responding"
fi

echo ""
echo "✅ Ubuntu deployment completed!"
echo ""
echo "🌐 Your services are available at:"
echo "   Main App: http://localhost:5000"
echo "   Email Service: http://localhost:5001"
echo "   Nginx Proxy: http://localhost"
echo ""
echo "📝 Useful commands:"
echo "   View logs: journalctl -u helpdesk-main -f"
echo "   View email logs: journalctl -u helpdesk-email -f"
echo "   Restart main app: systemctl restart helpdesk-main"
echo "   Restart email service: systemctl restart helpdesk-email"
echo "   Restart nginx: systemctl restart nginx"
echo ""
echo "🔧 To update the application:"
echo "   1. cd /var/www/helpdesk"
echo "   2. git pull (if using git)"
echo "   3. systemctl restart helpdesk-main helpdesk-email"
echo ""
echo "🔒 Security recommendations:"
echo "   1. Set up SSL certificate with Let's Encrypt"
echo "   2. Configure fail2ban for additional security"
echo "   3. Regular system updates"
echo "   4. Monitor logs for suspicious activity"
