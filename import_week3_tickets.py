#!/usr/bin/env python3
"""
Import Week 3 tickets into the IT Helpdesk database
Based on the extracted ticket data from Spiceworks
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

def import_week3_tickets():
    """Import Week 3 tickets into the database"""
    print("Starting Week 3 ticket import...")
    
    # Week 3 tickets data
    week3_tickets = [
        {
            "id": 44,
            "timestamp": "9/30/2025 10:18",
            "name": "nitohi4715@etenx.com",
            "email": "nitohi4715@etenx.com",
            "issue": "Laptop very slow - laptop has been really slow lately. It takes a long time to start up, and even simple tasks like opening Word or Excel freeze for a while.",
            "notes": """RESOLUTION STEPS:
1. Initial Assessment: User reported laptop performance issues affecting startup and application usage
2. Remote Diagnosis: Performed system analysis to identify performance bottlenecks
3. Performance Optimization:
   - Disabled unnecessary startup programs
   - Ran disk cleanup to remove temporary and cached files
   - Updated system and security patches
   - Checked for background processes using high resources
4. User Confirmation: User confirmed significant performance improvement
5. Ticket Closure: Issue resolved successfully

AGENT RESPONSES:
- Follow-Up: Requested additional information about duration and symptoms
- Optimization: Performed remote system optimization
- Closure: Confirmed resolution and closed ticket

RESOLUTION TIME: 30 minutes
STATUS: Resolved - Performance optimization successful""",
            "status": "Resolved",
            "priority": "Medium",
            "assigned_agent": "Asenathi Bokwana",
            "category": "Week 3: Performance & Optimization Support"
        },
        {
            "id": 45,
            "timestamp": "9/30/2025 11:42",
            "name": "Phumza Sotyantya",
            "email": "nitohi4715@etenx.com",
            "issue": "Computer is slow - Hi, my computer has been running really slow lately. It takes a long time to boot up, and even after logging in, apps like Outlook and Chrome take forever to open. Sometimes the system freezes for a few seconds when switching between programs. I've noticed this happening more over the past week, especially in the mornings. I haven't installed anything new recently, and I've already tried restarting a few times. Can someone please check what's going on?",
            "notes": """RESOLUTION STEPS:
1. Initial Assessment: User reported computer performance issues affecting boot time and application responsiveness
2. Remote Diagnosis: Analyzed system performance and identified optimization opportunities
3. Performance Optimization:
   - Disabled unnecessary startup programs
   - Ran disk cleanup to remove temporary and cached files
   - Updated system and security patches
   - Checked for background processes using high resources
4. User Confirmation: User confirmed laptop is much faster now, starts up quickly, and apps open without freezing
5. Ticket Closure: Issue resolved successfully

AGENT RESPONSES:
- Follow-Up: Requested information about duration and symptoms
- Optimization: Performed remote system optimization
- Closure: Confirmed resolution and closed ticket

RESOLUTION TIME: 30 minutes
STATUS: Resolved - Performance optimization successful""",
            "status": "Resolved",
            "priority": "Medium",
            "assigned_agent": "Asenathi Bokwana",
            "category": "Week 3: Performance & Optimization Support"
        }
    ]
    
    # Import each ticket
    for ticket in week3_tickets:
        print(f"Importing ticket {ticket['id']}: {ticket['issue'][:50]}...")
        
        # Escape single quotes in the data
        name_escaped = ticket['name'].replace("'", "''")
        email_escaped = ticket['email'].replace("'", "''")
        issue_escaped = ticket['issue'].replace("'", "''")
        notes_escaped = ticket['notes'].replace("'", "''")
        priority_escaped = ticket['priority'].replace("'", "''")
        assigned_agent_escaped = ticket['assigned_agent'].replace("'", "''")
        category_escaped = ticket['category'].replace("'", "''")
        
        # Insert ticket into database
        insert_query = f'''
            USE DATABASE 'my-database';
            INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent, category)
            VALUES ('{ticket['timestamp']}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '{notes_escaped}', '{ticket['status']}', '{priority_escaped}', '{assigned_agent_escaped}', '{category_escaped}')
        '''
        
        result = execute_query(insert_query)
        
        if result:
            print(f"Ticket {ticket['id']} imported successfully")
        else:
            print(f"Failed to import ticket {ticket['id']}")
    
    print("\nWeek 3 ticket import completed!")
    print(f"Imported {len(week3_tickets)} tickets")
    
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
        print("Week 3 tickets found in database:")
        for row in result['data']:
            if isinstance(row, dict):
                print(f"   ID: {row.get('id', 'N/A')}, Time: {row.get('timestamp', 'N/A')}, Name: {row.get('name', 'N/A')}, Issue: {str(row.get('issue', 'N/A'))[:50]}..., Status: {row.get('status', 'N/A')}, Priority: {row.get('priority', 'N/A')}, Agent: {row.get('assigned_agent', 'N/A')}, Category: {row.get('category', 'N/A')}")
            else:
                print(f"   Row data: {row}")
    else:
        print("No Week 3 tickets found in database")

if __name__ == "__main__":
    import_week3_tickets()
