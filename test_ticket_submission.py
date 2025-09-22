#!/usr/bin/env python3
"""
Test ticket submission through the main application
"""

import requests
import json

def test_ticket_submission():
    """Test submitting a ticket through the main application"""
    
    print("🧪 Testing Ticket Submission Integration")
    print("=" * 40)
    
    # Test data
    ticket_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'issue': 'Testing ticket submission integration',
        'priority': 'Medium'
    }
    
    try:
        print("📤 Submitting ticket to main application...")
        response = requests.post(
            "https://it-helpdesk-main.onrender.com/ticket",
            data=ticket_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Ticket submitted successfully!")
            print("   - Status: 200 OK")
            print("   - Response: Ticket submitted")
            return True
        elif response.status_code == 302:
            print("✅ Ticket submitted successfully!")
            print("   - Status: 302 Redirect (normal for form submission)")
            print("   - Response: Redirected to home page")
            return True
        else:
            print(f"❌ Ticket submission failed!")
            print(f"   - Status: {response.status_code}")
            print(f"   - Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_email_service_direct():
    """Test email service directly"""
    
    print("\n📧 Testing Email Service Directly...")
    
    test_data = {
        "name": "Direct Test User",
        "email": "direct@example.com",
        "subject": "Direct Email Service Test",
        "description": "Testing email service directly"
    }
    
    try:
        response = requests.post(
            "https://it-helpdesk-email.onrender.com/submit_ticket",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Email service working!")
            print(f"   - Message: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Email service failed!")
            print(f"   - Status: {response.status_code}")
            print(f"   - Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Email service connection failed: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 IT Helpdesk Integration Test")
    print("=" * 30)
    
    # Test email service directly first
    email_ok = test_email_service_direct()
    
    # Test main application
    main_ok = test_ticket_submission()
    
    print("\n📊 Test Results:")
    print("=" * 15)
    print(f"Email Service: {'✅ PASS' if email_ok else '❌ FAIL'}")
    print(f"Main App Integration: {'✅ PASS' if main_ok else '❌ FAIL'}")
    
    if email_ok and main_ok:
        print("\n🎉 All tests passed! Integration is working!")
    elif email_ok and not main_ok:
        print("\n⚠️ Email service works, but main app integration needs fixing")
        print("   - The main app needs to be updated to use the correct email service URL")
        print("   - Update app.py line 89 to use: https://it-helpdesk-email.onrender.com/submit_ticket")
    else:
        print("\n❌ Both services need attention")
        print("   - Check Render dashboard for service status")
        print("   - Verify environment variables are set correctly")

if __name__ == "__main__":
    main()
