#!/bin/bash
# Docker Deployment Script for IT Helpdesk System

echo "🐳 Deploying IT Helpdesk with Docker"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "📄 Creating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt email_requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r email_requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 5000 5001

# Default command (can be overridden)
CMD ["python", "app.py"]
EOF

echo "📄 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  helpdesk-main:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SQLITECLOUD_API_KEY=${SQLITECLOUD_API_KEY}
      - SQLITECLOUD_URL=${SQLITECLOUD_URL}
      - FLASK_ENV=production
    command: python app.py
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  helpdesk-email:
    build: .
    ports:
      - "5001:5001"
    environment:
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
      - MAIL_DEFAULT_SENDER=${MAIL_DEFAULT_SENDER}
      - NOTIFY_EMAILS=${NOTIFY_EMAILS}
      - MAIL_SERVER=smtp.gmail.com
      - MAIL_PORT=587
      - MAIL_USE_TLS=True
    command: python email_notifications.py
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - helpdesk-main
      - helpdesk-email
    restart: unless-stopped
EOF

echo "📄 Creating nginx.conf..."
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream helpdesk_main {
        server helpdesk-main:5000;
    }

    upstream helpdesk_email {
        server helpdesk-email:5001;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://helpdesk_main;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /email/ {
            proxy_pass http://helpdesk_email/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

echo "📄 Creating .env file..."
cat > .env << 'EOF'
# Database Configuration
SQLITECLOUD_API_KEY=your_sqlitecloud_api_key_here
SQLITECLOUD_URL=your_sqlitecloud_url_here

# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=IT Helpdesk <your_email@gmail.com>
NOTIFY_EMAILS=team1@company.com,team2@company.com
EOF

echo "📄 Creating .dockerignore..."
cat > .dockerignore << 'EOF'
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.md
!README.md
EOF

echo "⚙️  Setting up environment variables..."
echo "Please update the .env file with your actual configuration:"
echo "   - SQLiteCloud API Key and URL"
echo "   - Gmail credentials"
echo "   - Notification email addresses"

read -p "Press Enter when you've updated the .env file..."

echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service health..."
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

echo ""
echo "✅ Docker deployment completed!"
echo ""
echo "🌐 Your services are available at:"
echo "   Main App: http://localhost:5000"
echo "   Email Service: http://localhost:5001"
echo "   Nginx Proxy: http://localhost:80"
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update services: docker-compose pull && docker-compose up -d"
echo ""
echo "🔧 To update the application:"
echo "   1. Make your changes"
echo "   2. Run: docker-compose build"
echo "   3. Run: docker-compose up -d"
