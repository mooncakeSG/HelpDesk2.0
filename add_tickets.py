#!/usr/bin/env python3
"""
Script to add the requested tickets to the SQLiteCloud database
"""

import requests
import os
from datetime import datetime

# Set environment variables
os.environ['SQLITECLOUD_API_KEY'] = 'FpQNNvLCTlRGFvVlOnBuQbqNel3b0wPDs9u6jO2HsWU'
os.environ['SQLITECLOUD_URL'] = 'https://crihbwjchz.g5.sqlite.cloud:443/v2/weblite/sql'

api_key = os.environ['SQLITECLOUD_API_KEY']
api_url = os.environ['SQLITECLOUD_URL']
headers = {'Authorization': f'Bearer {api_key}'}

# Define the tickets
tickets = [
    {
        'name': 'Lindokuhle Mthembu',
        'email': 'lindokuhle.mthembu@company.com',
        'issue': 'Hi, I am locked out because I have forgotten my password. I have already verified my identity using our company app/phone system and my username is @lindokuhle. Could you initiate a password reset for me?',
        'status': 'Open'
    },
    {
        'name': 'Lindokuhle Mthembu',
        'email': 'lindokuhle.mthembu@company.com',
        'issue': 'Hello, I believe my AD account is locked after a few failed login attempts. I am confident I know the correct password now. My username is @lindokuhle; could you check its status and unlock it?',
        'status': 'Open'
    },
    {
        'name': 'Lindokuhle Mthembu',
        'email': 'lindokuhle.mthembu@company.com',
        'issue': 'Hi, I need help with a recurring account lockout. My account gets locked even when I enter the correct password, and it seems to be happening across different systems. Could you please investigate the source of the lockout using the lockout tool and clear it from all points?',
        'status': 'In Progress'
    },
    {
        'name': 'Lindokuhle Mthembu',
        'email': 'lindokuhle.mthembu@company.com',
        'issue': 'Hello, I am unable to log in and I have confirmed my password is correct. Could you check if my account (@lindokuhle) has been disabled? If it is, could you please outline the re-enablement process so I can get the necessary approval from my manager started?',
        'status': 'Open'
    },
    {
        'name': 'Lindokuhle Mthembu',
        'email': 'lindokuhle.mthembu@company.com',
        'issue': 'Hi, I can successfully log into my laptop itself, but I keep getting authentication prompts when I try to open Outlook. It will not accept my password, which I am certain is correct. This suggests a sync issue or a problem with my cached credentials for this specific service. Please advise.',
        'status': 'Open'
    }
]

def add_tickets():
    """Add all tickets to the database"""
    print("🚀 Adding tickets to SQLiteCloud database...")
    print("=" * 50)
    
    success_count = 0
    
    for i, ticket in enumerate(tickets, 1):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Escape single quotes to prevent SQL injection
        name_escaped = ticket['name'].replace("'", "''")
        email_escaped = ticket['email'].replace("'", "''")
        issue_escaped = ticket['issue'].replace("'", "''")
        
        insert_query = {
            'sql': f"""
            USE DATABASE 'my-database';
            INSERT INTO tickets (timestamp, name, email, issue, notes, status)
            VALUES ('{timestamp}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '', '{ticket["status"]}')
            """
        }
        
        try:
            response = requests.post(api_url, json=insert_query, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ Ticket {i} added successfully")
                print(f"   📧 {ticket['email']}")
                print(f"   📋 {ticket['issue'][:60]}...")
                print(f"   🏷️  Status: {ticket['status']}")
                print()
                success_count += 1
            else:
                print(f"❌ Error adding ticket {i}: {response.status_code}")
                print(f"   Response: {response.text}")
                print()
        except Exception as e:
            print(f"❌ Connection error for ticket {i}: {e}")
            print()
    
    print("=" * 50)
    print(f"🎉 Processed {len(tickets)} tickets")
    print(f"✅ Successfully added: {success_count}")
    print(f"❌ Failed: {len(tickets) - success_count}")
    
    if success_count > 0:
        print("\n🌐 You can now view the tickets at: http://localhost:5000/agent")

if __name__ == "__main__":
    add_tickets()
