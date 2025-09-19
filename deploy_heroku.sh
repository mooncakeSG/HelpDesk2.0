#!/bin/bash
# Heroku Deployment Script for IT Helpdesk System

echo "🚀 Deploying IT Helpdesk to Heroku"
echo "=================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku:"
    heroku login
fi

# Get app names
read -p "Enter name for main app (e.g., your-company-helpdesk): " MAIN_APP
read -p "Enter name for email service (e.g., your-company-helpdesk-email): " EMAIL_APP

echo "📱 Creating Heroku apps..."
heroku create $MAIN_APP
heroku create $EMAIL_APP

echo "⚙️  Setting up environment variables..."

# Main app environment variables
echo "Setting up main app environment variables..."
read -p "Enter SQLiteCloud API Key: " SQLITECLOUD_API_KEY
read -p "Enter SQLiteCloud URL: " SQLITECLOUD_URL

heroku config:set SQLITECLOUD_API_KEY="$SQLITECLOUD_API_KEY" -a $MAIN_APP
heroku config:set SQLITECLOUD_URL="$SQLITECLOUD_URL" -a $MAIN_APP
heroku config:set FLASK_ENV=production -a $MAIN_APP

# Email service environment variables
echo "Setting up email service environment variables..."
read -p "Enter Gmail username: " MAIL_USERNAME
read -p "Enter Gmail app password: " MAIL_PASSWORD
read -p "Enter notification emails (comma-separated): " NOTIFY_EMAILS

heroku config:set MAIL_USERNAME="$MAIL_USERNAME" -a $EMAIL_APP
heroku config:set MAIL_PASSWORD="$MAIL_PASSWORD" -a $EMAIL_APP
heroku config:set MAIL_DEFAULT_SENDER="IT Helpdesk <$MAIL_USERNAME>" -a $EMAIL_APP
heroku config:set NOTIFY_EMAILS="$NOTIFY_EMAILS" -a $EMAIL_APP
heroku config:set MAIL_SERVER=smtp.gmail.com -a $EMAIL_APP
heroku config:set MAIL_PORT=587 -a $EMAIL_APP
heroku config:set MAIL_USE_TLS=True -a $EMAIL_APP

echo "📄 Creating Procfile for main app..."
cat > Procfile << EOF
web: python app.py
EOF

echo "📄 Creating Procfile for email service..."
cat > Procfile.email << EOF
worker: python email_notifications.py
EOF

echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r email_requirements.txt

echo "🚀 Deploying main app..."
git init
git add .
git commit -m "Initial deployment"
git push heroku main

echo "📧 Deploying email service..."
cp Procfile.email Procfile
git add Procfile
git commit -m "Add email service"
git push heroku main -a $EMAIL_APP

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your apps are available at:"
echo "   Main App: https://$MAIN_APP.herokuapp.com"
echo "   Email Service: https://$EMAIL_APP.herokuapp.com"
echo ""
echo "📝 Next steps:"
echo "   1. Test the main app: https://$MAIN_APP.herokuapp.com"
echo "   2. Test email service: https://$EMAIL_APP.herokuapp.com/health"
echo "   3. Submit a test ticket to verify email notifications"
echo ""
echo "🔧 To update the apps later:"
echo "   git push heroku main -a $MAIN_APP"
echo "   git push heroku main -a $EMAIL_APP"
