#!/usr/bin/env python3
"""
IT Helpdesk Email Notification System
Flask backend that receives ticket submissions and sends styled HTML emails with CSV attachments
"""

from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import csv
import io
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'IT Helpdesk <noreply@company.com>')

# Initialize Flask-Mail
mail = Mail(app)

def create_html_email(ticket_data):
    """Create a professional HTML email template for ticket notifications"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New IT Helpdesk Ticket</title>
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        
        <!-- Header -->
        <div style="background-color: #0066cc; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 24px;">🎫 New Ticket Submitted</h1>
        </div>
        
        <!-- Ticket Information -->
        <div style="background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-top: none;">
            <div style="margin-bottom: 15px;">
                <strong style="color: #0066cc;">👤 Name:</strong> {ticket_data['name']}
            </div>
            <div style="margin-bottom: 15px;">
                <strong style="color: #0066cc;">📧 Email:</strong> {ticket_data['email']}
            </div>
            <div style="margin-bottom: 15px;">
                <strong style="color: #0066cc;">📋 Subject:</strong> {ticket_data['subject']}
            </div>
            <div style="margin-bottom: 15px;">
                <strong style="color: #0066cc;">📝 Description:</strong>
            </div>
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 5px; border-left: 4px solid #0066cc; margin-bottom: 15px;">
                {ticket_data['description'].replace(chr(10), '<br>')}
            </div>
            <div style="font-size: 12px; color: #6c757d;">
                <strong>⏰ Submitted:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 0 0 8px 8px; border: 1px solid #dee2e6; border-top: none; text-align: center;">
            <p style="margin: 0; font-size: 12px; color: #6c757d;">
                This is an automated ticket notification from the IT Helpdesk system.
            </p>
        </div>
        
    </body>
    </html>
    """
    return html_template

def create_csv_attachment(ticket_data):
    """Create a CSV attachment with ticket details"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Name', 'Email', 'Subject', 'Description', 'Submitted'])
    
    # Write ticket data
    writer.writerow([
        ticket_data['name'],
        ticket_data['email'],
        ticket_data['subject'],
        ticket_data['description'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ])
    
    # Get CSV content
    csv_content = output.getvalue()
    output.close()
    
    return csv_content

def get_notification_emails():
    """Get list of email addresses to notify"""
    emails_str = os.getenv('NOTIFY_EMAILS', '')
    if not emails_str:
        return []
    
    # Split by comma and clean up whitespace
    emails = [email.strip() for email in emails_str.split(',') if email.strip()]
    return emails

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    """Handle ticket submission and send email notifications"""
    try:
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'description']
        ticket_data = {}
        
        for field in required_fields:
            if field not in request.json:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
            
            value = request.json[field]
            if not value or not str(value).strip():
                return jsonify({
                    'error': f'Field {field} cannot be empty'
                }), 400
            
            ticket_data[field] = str(value).strip()
        
        # Get notification emails
        notification_emails = get_notification_emails()
        if not notification_emails:
            return jsonify({
                'error': 'No notification emails configured'
            }), 500
        
        # Create HTML email content
        html_content = create_html_email(ticket_data)
        
        # Create CSV attachment
        csv_content = create_csv_attachment(ticket_data)
        
        # Create email message
        msg = Message(
            subject=f"New IT Helpdesk Ticket: {ticket_data['subject']}",
            recipients=notification_emails,
            html=html_content
        )
        
        # Attach CSV file
        msg.attach(
            filename="ticket.csv",
            content_type="text/csv",
            data=csv_content
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({
            'success': True,
            'message': 'Ticket submitted successfully, email sent with CSV attachment',
            'recipients': len(notification_emails),
            'ticket_id': f"TICKET-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        })
        
    except Exception as e:
        app.logger.error(f"Error processing ticket submission: {str(e)}")
        return jsonify({
            'error': f'Failed to process ticket: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'IT Helpdesk Email Notifications',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'service': 'IT Helpdesk Email Notification System',
        'version': '1.0.0',
        'endpoints': {
            'POST /submit_ticket': 'Submit a new ticket and send email notifications',
            'GET /health': 'Health check endpoint'
        },
        'required_fields': ['name', 'email', 'subject', 'description']
    })

if __name__ == '__main__':
    # Validate email configuration
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("❌ Error: MAIL_USERNAME and MAIL_PASSWORD must be set in environment variables")
        exit(1)
    
    if not get_notification_emails():
        print("❌ Error: NOTIFY_EMAILS must be set in environment variables")
        exit(1)
    
    print("🚀 Starting IT Helpdesk Email Notification System...")
    print(f"📧 Email server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
    print(f"👤 Sender: {app.config['MAIL_DEFAULT_SENDER']}")
    print(f"📬 Notification emails: {len(get_notification_emails())} configured")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
