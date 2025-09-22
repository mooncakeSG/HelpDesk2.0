#!/usr/bin/env python3
"""
Verify that agent assignments match the image requirements
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
    print("❌ Error: SQLITECLOUD_API_KEY and SQLITECLOUD_URL must be set in environment variables")
    exit(1)

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def execute_query(query, params=None):
    """Execute a SQL query on SQLiteCloud"""
    try:
        payload = {"sql": query}
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"❌ Query failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def main():
    """Verify agent assignments match the image"""
    print("👤 Verifying Agent Assignments for Week 2 Tickets")
    print("================================================")
    
    # Expected assignments based on the image
    expected_assignments = {
        32: "Phumza Melinda Sotyantya",  # Sarah Johnson
        33: "Asenathi Bokwana",          # Mike Chen
        34: "Phumza Melinda Sotyantya",  # Emily Rodriguez
        35: "Asenathi Bokwana",          # David Thompson
        36: "Asenathi Bokwana",          # Lisa Wang
        37: "Phumza Melinda Sotyantya",  # James Wilson
        38: "Asenathi Bokwana",          # Maria Garcia
        39: "Phumza Melinda Sotyantya",  # Robert Brown
        40: "Asenathi Bokwana",          # Jennifer Davis
        41: "Phumza Melinda Sotyantya",  # Christopher Lee
        42: "Asenathi Bokwana",          # Amanda Taylor
        43: "Phumza Melinda Sotyantya"   # Michael Anderson
    }
    
    # Fetch current assignments from database
    query = '''
        USE DATABASE 'my-database';
        SELECT id, name, assigned_agent
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        ORDER BY id
    '''
    
    result = execute_query(query)
    if not result or 'data' not in result:
        print("❌ Failed to fetch ticket data")
        return
    
    tickets = result['data']
    
    print("📋 Verification Results:")
    print("-" * 50)
    
    all_correct = True
    
    for ticket in tickets:
        ticket_id = ticket['id']
        name = ticket['name']
        assigned_agent = ticket['assigned_agent']
        expected_agent = expected_assignments.get(ticket_id, 'Unknown')
        
        is_correct = assigned_agent == expected_agent
        status = "✅" if is_correct else "❌"
        
        print(f"{status} Ticket #{ticket_id}: {name}")
        print(f"   Expected: {expected_agent}")
        print(f"   Actual:   {assigned_agent}")
        print()
        
        if not is_correct:
            all_correct = False
    
    # Summary
    print("📊 Summary:")
    print("-" * 20)
    
    if all_correct:
        print("🎉 All agent assignments are correct!")
        print("   - All 12 Week 2 tickets have the correct agent assignments")
        print("   - Assignments match the provided image exactly")
        print("   - Ready for viewing in the Agent Portal")
    else:
        print("❌ Some agent assignments are incorrect")
        print("   - Please check the assignments and update as needed")
    
    # Agent workload summary
    print("\n👤 Agent Workload Summary:")
    print("-" * 30)
    
    agent_counts = {}
    for ticket in tickets:
        agent = ticket['assigned_agent']
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    for agent, count in agent_counts.items():
        print(f"   - {agent}: {count} tickets")
    
    print(f"\n📈 Total Week 2 tickets: {len(tickets)}")
    print("✅ Agent assignment verification completed!")

if __name__ == "__main__":
    main()
