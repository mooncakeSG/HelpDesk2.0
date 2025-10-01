#!/usr/bin/env python3
"""
Import Week 3 ticket #30 - Duplicate IP address conflict
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLiteCloud configuration
API_KEY = os.getenv('SQLITECLOUD_API_KEY')
API_URL = os.getenv('SQLITECLOUD_URL')

if not API_KEY or not API_URL:
    print("Error: SQLITECLOUD_API_KEY and SQLITECLOUD_URL must be set in environment variables")
    exit(1)

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def execute_query(query):
    """Execute a SQL query on SQLiteCloud"""
    try:
        payload = {"sql": query}
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Query failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def import_week3_ticket_30():
    """Import Week 3 ticket #30 - Duplicate IP address conflict"""
    print("Starting Week 3 ticket #30 import...")
    
    # Ticket #30 data
    ticket_30 = {
        "timestamp": "10/1/2025 9:38",
        "name": "Phumza Sotyantya",
        "email": "phumza.sotyantya@capaciti.org.za",
        "issue": "Duplicate IP address conflict - Laptop keeps showing 'IP Address Conflict Detected' and my network disconnects every few minutes. I can't stay online long enough to finish my work.",
        "notes": """RESOLUTION STEPS:
1. Initial Assessment: User reported IP address conflict causing frequent network disconnections
2. Remote Diagnosis: Identified duplicate IP address issue affecting network connectivity
3. Troubleshooting Steps:
   - Asked user to disconnect from Wi-Fi
   - Instructed user to run ipconfig /release in Command Prompt
   - Instructed user to run ipconfig /renew in Command Prompt
   - User reconnected to Wi-Fi after commands
4. User Confirmation: User confirmed no error after following instructions
5. Follow-up: Documented issue for Network Team to resolve root cause
6. Ticket Closure: Issue temporarily resolved, root cause to be addressed by Network Team

AGENT RESPONSES:
- Initial Response: Explained IP conflict and requested additional information about location and connection type
- User Response: Confirmed issue occurs in office on both Wi-Fi and network cable
- Solution Provided: Gave step-by-step instructions for ipconfig commands
- User Confirmation: User followed instructions and reported no immediate errors
- Closure: Documented for Network Team follow-up

RESOLUTION TIME: 6 minutes
STATUS: Resolved - Temporary fix applied, root cause to be addressed by Network Team""",
        "status": "Resolved",
        "priority": "High",
        "assigned_agent": "Asenathi Bokwana",
        "category": "Week 3: Performance & Optimization Support"
    }
    
    print(f"Importing ticket #30: {ticket_30['issue'][:50]}...")
    
    # Escape single quotes in the data
    name_escaped = ticket_30['name'].replace("'", "''")
    email_escaped = ticket_30['email'].replace("'", "''")
    issue_escaped = ticket_30['issue'].replace("'", "''")
    notes_escaped = ticket_30['notes'].replace("'", "''")
    priority_escaped = ticket_30['priority'].replace("'", "''")
    assigned_agent_escaped = ticket_30['assigned_agent'].replace("'", "''")
    category_escaped = ticket_30['category'].replace("'", "''")
    
    # Insert ticket into database
    insert_query = f'''
        USE DATABASE 'my-database';
        INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent, category)
        VALUES ('{ticket_30['timestamp']}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '{notes_escaped}', '{ticket_30['status']}', '{priority_escaped}', '{assigned_agent_escaped}', '{category_escaped}')
    '''
    
    result = execute_query(insert_query)
    
    if result:
        print("Ticket #30 imported successfully")
    else:
        print("Failed to import ticket #30")
    
    print("\nWeek 3 ticket #30 import completed!")
    
    # Verify the import
    print("\nVerifying import...")
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT id, timestamp, name, issue, status, priority, assigned_agent, category
        FROM tickets 
        WHERE category = 'Week 3: Performance & Optimization Support'
        ORDER BY id
    '''
    
    result = execute_query(verify_query)
    
    if result and 'data' in result:
        print(f"Week 3 tickets found in database: {len(result['data'])} tickets")
        for row in result['data']:
            if isinstance(row, dict):
                print(f"   ID: {row.get('id', 'N/A')}, Time: {row.get('timestamp', 'N/A')}, Name: {row.get('name', 'N/A')}, Issue: {str(row.get('issue', 'N/A'))[:50]}..., Status: {row.get('status', 'N/A')}, Priority: {row.get('priority', 'N/A')}, Agent: {row.get('assigned_agent', 'N/A')}")
            else:
                print(f"   Row data: {row}")
    else:
        print("No Week 3 tickets found in database")

if __name__ == "__main__":
    import_week3_ticket_30()
