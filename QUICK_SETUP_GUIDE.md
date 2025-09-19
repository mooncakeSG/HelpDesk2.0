# 🚀 Quick Setup Guide - IT Helpdesk Email Notifications

## ✅ **Issue Fixed!**
The syntax error in `email_notifications.py` has been resolved. The server is now ready to run.

## 🛠️ **Quick Setup (5 minutes)**

### 1. **Install Dependencies** (if not already done)
```bash
pip install -r email_requirements.txt
```

### 2. **Configure Email Settings**
Create a `.env` file in the project directory:

```env
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Your Gmail credentials (use App Password!)
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=yourapppassword

# Email sender configuration
MAIL_DEFAULT_SENDER=IT Helpdesk <your.email@gmail.com>

# Team notification emails (comma-separated)
NOTIFY_EMAILS=teammate1@gmail.com,teammate2@gmail.com,teammate3@gmail.com
```

### 3. **Get Gmail App Password**
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google Account Settings](https://myaccount.google.com/security)
3. Click "App passwords" under "Signing in to Google"
4. Generate a new app password for "Mail"
5. Use this 16-character password (not your regular Gmail password)

### 4. **Start the Server**
```bash
python email_notifications.py
```
Server will start on `http://localhost:5001`

### 5. **Test the System**
```bash
python test_email_notifications.py
```

## 🧪 **Test Results**
✅ Syntax error fixed  
✅ Server imports successfully  
✅ HTML email generation works  
✅ CSV attachment generation works  
✅ Flask app configuration loaded  

## 📧 **What Happens When You Submit a Ticket**

1. **API Call**: `POST http://localhost:5001/submit_ticket`
2. **Email Sent**: Professional HTML email to all team members
3. **CSV Attached**: Complete ticket details in CSV format
4. **Response**: JSON confirmation with ticket ID

## 🔌 **API Example**
```bash
curl -X POST http://localhost:5001/submit_ticket \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john@company.com", 
    "subject": "Printer not working",
    "description": "The office printer is showing error messages..."
  }'
```

## 📁 **Generated Files**
- `sample_email.html` - Email template preview
- `sample_ticket.csv` - CSV attachment example

## 🎯 **Ready to Use!**
The email notification system is now fully functional and ready for production use!
