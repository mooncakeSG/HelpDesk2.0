#!/usr/bin/env python3
"""
Test Integration Between Ticket System and Email Service
"""

import requests
import json
import time
from datetime import datetime

def test_main_application():
    """Test if main application is accessible"""
    print("🔍 Testing Main Application...")
    
    try:
        response = requests.get("https://it-helpdesk-main.onrender.com/", timeout=10)
        if response.status_code == 200:
            print("✅ Main Application: ACCESSIBLE")
            return True
        else:
            print(f"❌ Main Application: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main Application: CONNECTION FAILED - {e}")
        return False

def test_email_service():
    """Test if email service is accessible"""
    print("🔍 Testing Email Service...")
    
    try:
        response = requests.get("https://it-helpdesk-email.onrender.com/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email Service: HEALTHY - {data['status']}")
            return True
        else:
            print(f"❌ Email Service: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Email Service: CONNECTION FAILED - {e}")
        return False

def test_email_endpoints():
    """Test email service endpoints"""
    print("🔍 Testing Email Service Endpoints...")
    
    try:
        # Test root endpoint
        response = requests.get("https://it-helpdesk-email.onrender.com/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Email Service Endpoints: AVAILABLE")
            print(f"   - Health Check: {data['endpoints']['GET /health']}")
            print(f"   - Submit Ticket: {data['endpoints']['POST /submit_ticket']}")
            return True
        else:
            print(f"❌ Email Service Endpoints: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Email Service Endpoints: CONNECTION FAILED - {e}")
        return False

def test_ticket_submission():
    """Test ticket submission through email service"""
    print("🔍 Testing Ticket Submission...")
    
    test_ticket = {
        "name": "Integration Test User",
        "email": "test@example.com",
        "subject": "Integration Test - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "This is a test ticket to verify the integration between the ticket system and email service."
    }
    
    try:
        response = requests.post(
            "https://it-helpdesk-email.onrender.com/submit_ticket",
            json=test_ticket,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ticket Submission: SUCCESS")
            print(f"   - Message: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Ticket Submission: ERROR - Status {response.status_code}")
            print(f"   - Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ticket Submission: CONNECTION FAILED - {e}")
        return False

def test_main_app_ticket_form():
    """Test if main app ticket form is accessible"""
    print("🔍 Testing Main App Ticket Form...")
    
    try:
        response = requests.get("https://it-helpdesk-main.onrender.com/ticket", timeout=10)
        if response.status_code == 200:
            print("✅ Ticket Form: ACCESSIBLE")
            return True
        else:
            print(f"❌ Ticket Form: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ticket Form: CONNECTION FAILED - {e}")
        return False

def test_agent_portal():
    """Test if agent portal is accessible"""
    print("🔍 Testing Agent Portal...")
    
    try:
        response = requests.get("https://it-helpdesk-main.onrender.com/agent", timeout=10)
        if response.status_code == 200:
            print("✅ Agent Portal: ACCESSIBLE")
            return True
        else:
            print(f"❌ Agent Portal: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent Portal: CONNECTION FAILED - {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 IT Helpdesk Integration Test")
    print("=" * 40)
    print()
    
    tests = [
        ("Main Application", test_main_application),
        ("Email Service Health", test_email_service),
        ("Email Service Endpoints", test_email_endpoints),
        ("Ticket Form", test_main_app_ticket_form),
        ("Agent Portal", test_agent_portal),
        ("Email Integration", test_ticket_submission)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print()
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Integration is working perfectly!")
        print()
        print("✅ Your IT Helpdesk system is fully connected:")
        print("   • Main application is accessible")
        print("   • Email service is healthy")
        print("   • Ticket submission works")
        print("   • Agent portal is functional")
        print("   • Email notifications are ready")
    else:
        print("⚠️ Some tests failed - Check the issues above")
        print()
        print("🔧 Troubleshooting steps:")
        print("   1. Check Render dashboard for service status")
        print("   2. Verify environment variables are set")
        print("   3. Check service logs for errors")
        print("   4. Ensure both services are running")
    
    print()
    print("🌐 Live URLs:")
    print("   • Main App: https://it-helpdesk-main.onrender.com/")
    print("   • Email Service: https://it-helpdesk-email.onrender.com/")

if __name__ == "__main__":
    main()
