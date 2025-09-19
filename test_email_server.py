#!/usr/bin/env python3
"""
Test script to verify the email notification server can start without errors
"""

import os
import sys

def test_email_server():
    """Test if the email server can be imported and configured"""
    print("🧪 Testing Email Notification Server...")
    print("=" * 50)
    
    try:
        # Test import
        print("1. Testing import...")
        import email_notifications
        print("   ✅ Import successful")
        
        # Test Flask app creation
        print("2. Testing Flask app creation...")
        app = email_notifications.app
        print("   ✅ Flask app created")
        
        # Test email configuration (without actual credentials)
        print("3. Testing email configuration...")
        print(f"   📧 Mail server: {app.config.get('MAIL_SERVER', 'Not set')}")
        print(f"   🔌 Mail port: {app.config.get('MAIL_PORT', 'Not set')}")
        print(f"   🔒 Use TLS: {app.config.get('MAIL_USE_TLS', 'Not set')}")
        print("   ✅ Configuration loaded")
        
        # Test HTML email generation
        print("4. Testing HTML email generation...")
        test_ticket = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'description': 'Test description with\nmultiple lines'
        }
        html_content = email_notifications.create_html_email(test_ticket)
        print(f"   ✅ HTML email generated ({len(html_content)} characters)")
        
        # Test CSV generation
        print("5. Testing CSV generation...")
        csv_content = email_notifications.create_csv_attachment(test_ticket)
        print(f"   ✅ CSV attachment generated ({len(csv_content)} characters)")
        
        print()
        print("🎉 All tests passed! The email server is ready to run.")
        print()
        print("📝 Next steps:")
        print("   1. Configure your .env file with email settings")
        print("   2. Run: python email_notifications.py")
        print("   3. Test with: python test_email_notifications.py")
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Make sure Flask-Mail is installed: pip install Flask-Mail")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_email_server()
    sys.exit(0 if success else 1)
