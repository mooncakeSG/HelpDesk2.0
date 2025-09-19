#!/usr/bin/env python3
"""
Test sending email to the same Gmail address to verify delivery
"""

import requests
import json

def test_same_email():
    """Test sending email to the same Gmail address"""
    
    print("🧪 Testing Email to Same Gmail Address")
    print("=" * 50)
    
    # Test data - sending to the same Gmail address
    ticket_data = {
        "name": "Test User",
        "email": "keawinkoesnel804@gmail.com",  # Same as sender
        "subject": "Test Email - Same Address",
        "description": """This is a test email to verify delivery to the same Gmail address.

If you receive this email, the system is working correctly.

Test details:
- Sender: keawinkoesnel804@gmail.com
- Recipient: keawinkoesnel804@gmail.com
- Time: Test email
- Purpose: Verify email delivery

Please check your inbox and spam folder."""
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/submit_ticket",
            json=ticket_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test email sent successfully!")
            print(f"📬 Email sent to: {result.get('recipients', 'Unknown')} recipients")
            print(f"🎫 Ticket ID: {result.get('ticket_id', 'Unknown')}")
            print()
            print("📧 Check your Gmail inbox and spam folder for the test email")
            print("   Subject: 'New IT Helpdesk Ticket: Test Email - Same Address'")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_same_email()
