#!/usr/bin/env python3
"""
Demo script for IT Helpdesk Email Notification System
Shows the email template and CSV generation without sending actual emails
"""

import os
import csv
import io
from datetime import datetime

def create_html_email_demo(ticket_data):
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

def create_csv_demo(ticket_data):
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

def demo_email_system():
    """Demonstrate the email notification system"""
    
    print("🎫 IT Helpdesk Email Notification System - Demo")
    print("=" * 60)
    print()
    
    # Sample ticket data
    ticket_data = {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@company.com",
        "subject": "VPN connection issues - cannot access remote files",
        "description": """Hi IT Team,

I'm experiencing problems with the VPN connection today. When I try to connect, I get an error message saying "Authentication failed" even though I'm using the correct credentials.

Details:
- VPN Client: Cisco AnyConnect
- Error: "Authentication failed - please check your credentials"
- Tried: Multiple times with same credentials that worked yesterday
- Network: Home WiFi (stable connection)
- Time: Started this morning around 9 AM

This is affecting my ability to access shared drives and work files. I have an important deadline tomorrow and need access to the project files.

Could someone please help me resolve this ASAP?

Thanks,
Sarah"""
    }
    
    print("📋 Sample Ticket Data:")
    print(f"   Name: {ticket_data['name']}")
    print(f"   Email: {ticket_data['email']}")
    print(f"   Subject: {ticket_data['subject']}")
    print(f"   Description: {len(ticket_data['description'])} characters")
    print()
    
    # Generate HTML email
    print("📧 Generating HTML Email Template...")
    html_content = create_html_email_demo(ticket_data)
    
    # Save HTML to file for preview
    with open('sample_email.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("   ✅ HTML email saved to 'sample_email.html'")
    print("   🌐 Open this file in your browser to see the email preview")
    print()
    
    # Generate CSV attachment
    print("📎 Generating CSV Attachment...")
    csv_content = create_csv_demo(ticket_data)
    
    # Save CSV to file
    with open('sample_ticket.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    print("   ✅ CSV attachment saved to 'sample_ticket.csv'")
    print()
    
    # Show CSV content
    print("📊 CSV Content Preview:")
    print("-" * 40)
    print(csv_content)
    print("-" * 40)
    print()
    
    # Show email configuration example
    print("⚙️  Email Configuration Example:")
    print("-" * 40)
    print("MAIL_SERVER=smtp.gmail.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=True")
    print("MAIL_USERNAME=your.email@gmail.com")
    print("MAIL_PASSWORD=yourapppassword")
    print("MAIL_DEFAULT_SENDER=IT Helpdesk <your.email@gmail.com>")
    print("NOTIFY_EMAILS=teammate1@gmail.com,teammate2@gmail.com,teammate3@gmail.com")
    print("-" * 40)
    print()
    
    # Show API usage example
    print("🔌 API Usage Example:")
    print("-" * 40)
    print("curl -X POST http://localhost:5001/submit_ticket \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "name": "John Smith",')
    print('    "email": "john@company.com",')
    print('    "subject": "Printer not working",')
    print('    "description": "The office printer is showing error messages..."')
    print("  }'")
    print("-" * 40)
    print()
    
    print("🚀 Next Steps:")
    print("   1. Configure your .env file with email settings")
    print("   2. Run: python email_notifications.py")
    print("   3. Test with: python test_email_notifications.py")
    print("   4. Open 'sample_email.html' to see the email design")
    print()
    
    print("📁 Generated Files:")
    print("   📧 sample_email.html - Email template preview")
    print("   📊 sample_ticket.csv - CSV attachment example")
    print()
    
    print("🎉 Demo completed successfully!")

if __name__ == "__main__":
    demo_email_system()
