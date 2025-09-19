# IT Helpdesk Email Notification System

A Flask backend service that receives ticket submissions and sends professional HTML email notifications with CSV attachments to multiple team members.

## 🚀 Features

- **Professional HTML Emails**: Styled email templates with company branding
- **CSV Attachments**: Automatic CSV file generation with ticket details
- **Multi-Recipient Support**: Send notifications to multiple team members
- **Error Handling**: Comprehensive validation and error reporting
- **RESTful API**: Simple JSON-based ticket submission endpoint
- **Health Monitoring**: Built-in health check endpoint

## 📋 Requirements

- Python 3.7+
- Gmail account with App Password (or other SMTP provider)
- Flask and Flask-Mail dependencies

## 🛠️ Installation

1. **Install Dependencies**
   ```bash
   pip install -r email_requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp email_env_template.txt .env
   # Edit .env with your email settings
   ```

3. **Gmail App Password Setup**
   - Enable 2-Factor Authentication on your Google account
   - Go to Google Account settings > Security > App passwords
   - Generate a new app password for "Mail"
   - Use this 16-character password in your .env file

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Your Gmail credentials
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=yourapppassword

# Email sender configuration
MAIL_DEFAULT_SENDER=IT Helpdesk <your.email@gmail.com>

# Team notification emails (comma-separated)
NOTIFY_EMAILS=teammate1@gmail.com,teammate2@gmail.com,teammate3@gmail.com
```

## 🚀 Usage

### Start the Server

```bash
python email_notifications.py
```

The server will start on `http://localhost:5001`

### Submit a Ticket

**Endpoint**: `POST /submit_ticket`

**Request Body**:
```json
{
  "name": "John Smith",
  "email": "john.smith@company.com",
  "subject": "Laptop won't start - urgent",
  "description": "My laptop suddenly stopped working this morning..."
}
```

**Response**:
```json
{
  "success": true,
  "message": "Ticket submitted successfully, email sent with CSV attachment",
  "recipients": 5,
  "ticket_id": "TICKET-20241218-143022"
}
```

### Test the System

```bash
python test_email_notifications.py
```

## 📧 Email Template

The system sends professional HTML emails with:

- **Header**: Blue banner with "New Ticket Submitted"
- **Ticket Info**: Name, Email, Subject, Description
- **Description Box**: Light grey box with proper formatting
- **Footer**: Automated notification disclaimer
- **CSV Attachment**: Complete ticket details in CSV format

## 🔧 API Endpoints

### `POST /submit_ticket`
Submit a new ticket and send email notifications.

**Required Fields**:
- `name` (string): User's full name
- `email` (string): User's email address
- `subject` (string): Brief ticket subject
- `description` (string): Detailed issue description

### `GET /health`
Health check endpoint for monitoring.

### `GET /`
API information and available endpoints.

## 📁 File Structure

```
├── email_notifications.py      # Main Flask application
├── email_requirements.txt      # Python dependencies
├── email_env_template.txt      # Environment configuration template
├── test_email_notifications.py # Test script
└── EMAIL_NOTIFICATIONS_README.md # This file
```

## 🧪 Testing

The included test script demonstrates:

1. **Health Check**: Verify service is running
2. **API Information**: Get available endpoints
3. **Ticket Submission**: Submit a sample ticket

Run tests:
```bash
python test_email_notifications.py
```

## 🔒 Security Notes

- Use App Passwords instead of regular Gmail passwords
- Keep your .env file secure and never commit it to version control
- Consider using environment variables in production
- Validate all input data (built into the system)

## 🚀 Production Deployment

For production deployment:

1. **Environment Variables**: Set via your hosting platform
2. **HTTPS**: Use SSL/TLS for secure communication
3. **Error Logging**: Configure proper logging
4. **Monitoring**: Set up health check monitoring
5. **Rate Limiting**: Consider adding rate limiting for the API

## 🔄 Integration Examples

### cURL Example
```bash
curl -X POST http://localhost:5001/submit_ticket \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@company.com",
    "subject": "Printer not working",
    "description": "The office printer is showing error messages..."
  }'
```

### JavaScript Example
```javascript
fetch('http://localhost:5001/submit_ticket', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John Smith',
    email: 'john@company.com',
    subject: 'Email issues',
    description: 'Cannot send emails from Outlook...'
  })
})
.then(response => response.json())
.then(data => console.log('Success:', data));
```

## 🐛 Troubleshooting

### Common Issues

1. **"No notification emails configured"**
   - Check NOTIFY_EMAILS in your .env file
   - Ensure emails are comma-separated

2. **"Authentication failed"**
   - Verify MAIL_USERNAME and MAIL_PASSWORD
   - Use App Password, not regular Gmail password
   - Check 2FA is enabled on Gmail

3. **"Connection refused"**
   - Ensure server is running on port 5001
   - Check firewall settings

4. **Emails not received**
   - Check spam/junk folders
   - Verify recipient email addresses
   - Check Gmail sending limits

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your .env configuration
3. Test with the included test script
4. Check server logs for detailed error messages

## 🔮 Future Enhancements

Potential improvements:
- Database integration for ticket tracking
- Slack/Teams notifications
- Email templates customization
- Ticket status updates
- User authentication
- Dashboard interface
- Advanced filtering and search
