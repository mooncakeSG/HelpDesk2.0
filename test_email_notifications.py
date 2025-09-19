#!/usr/bin/env python3
"""
Test script for IT Helpdesk Email Notification System
Demonstrates how to submit tickets via API
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:5001"

def test_ticket_submission():
    """Test submitting a ticket via the API"""
    
    # Sample ticket data
    ticket_data = {
        "name": "John Smith",
        "email": "john.smith@company.com",
        "subject": "Laptop won't start - urgent",
        "description": """Hi IT Team,

My laptop suddenly stopped working this morning. When I press the power button, nothing happens - no lights, no fan noise, completely dead.

Details:
- Model: Dell Latitude 5520
- Last working: Yesterday evening
- Tried: Different power adapter, holding power button for 30 seconds
- Error: No response at all

This is urgent as I have an important presentation at 2 PM today.

Please help ASAP!

Thanks,
John"""
    }
    
    print("🚀 Testing IT Helpdesk Email Notification System")
    print("=" * 50)
    print(f"📧 Submitting ticket for: {ticket_data['name']}")
    print(f"📋 Subject: {ticket_data['subject']}")
    print()
    
    try:
        # Submit ticket
        response = requests.post(
            f"{API_BASE_URL}/submit_ticket",
            json=ticket_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ticket submitted successfully!")
            print(f"📬 Email sent to {result['recipients']} recipients")
            print(f"🎫 Ticket ID: {result['ticket_id']}")
            print(f"💬 Message: {result['message']}")
        else:
            print(f"❌ Error submitting ticket: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the email notification server is running on port 5001")
        print("   Run: python email_notifications.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Service is healthy!")
            print(f"🕐 Timestamp: {result['timestamp']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_api_info():
    """Test the API information endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("📋 API Information:")
            print(f"   Service: {result['service']}")
            print(f"   Version: {result['version']}")
            print("   Available endpoints:")
            for endpoint, description in result['endpoints'].items():
                print(f"     {endpoint}: {description}")
        else:
            print(f"❌ API info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API info error: {e}")

if __name__ == "__main__":
    print("🧪 IT Helpdesk Email Notification System - Test Suite")
    print("=" * 60)
    print()
    
    # Test health check
    print("1. Testing health check...")
    test_health_check()
    print()
    
    # Test API info
    print("2. Testing API information...")
    test_api_info()
    print()
    
    # Test ticket submission
    print("3. Testing ticket submission...")
    test_ticket_submission()
    print()
    
    print("🎉 Test suite completed!")
    print()
    print("📝 Next steps:")
    print("   1. Check your email inbox for the notification")
    print("   2. Verify the CSV attachment contains the ticket details")
    print("   3. Test with different ticket data if needed")
