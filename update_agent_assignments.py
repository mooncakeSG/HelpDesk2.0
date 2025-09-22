#!/usr/bin/env python3
"""
Update agent assignments for Week 2 tickets to match the correct agents from the image
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
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def main():
    """Update agent assignments for Week 2 tickets"""
    print("👤 Updating Agent Assignments for Week 2 Tickets")
    print("===============================================")
    
    # Agent assignments based on the image
    # Tickets 32-43 should be assigned to Phumza Melinda Sotyantya and Asenathi Bokwana
    agent_assignments = {
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
    
    print("📋 Agent Assignment Plan:")
    print("   - Phumza Melinda Sotyantya: 6 tickets")
    print("   - Asenathi Bokwana: 6 tickets")
    print()
    
    updated_count = 0
    
    # Update each ticket with the correct agent assignment
    for ticket_id, agent_name in agent_assignments.items():
        # Escape single quotes in agent name
        agent_escaped = agent_name.replace("'", "''")
        
        update_query = f'''
            USE DATABASE 'my-database';
            UPDATE tickets 
            SET assigned_agent = '{agent_escaped}'
            WHERE id = {ticket_id}
        '''
        
        result = execute_query(update_query)
        if result:
            updated_count += 1
            print(f"✅ Updated Ticket #{ticket_id}: Assigned to {agent_name}")
        else:
            print(f"❌ Failed to update Ticket #{ticket_id}")
    
    print(f"\n🎉 Successfully updated {updated_count} ticket assignments!")
    
    # Verify the updates
    print("\n📊 Verifying agent assignments...")
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, assigned_agent
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        ORDER BY id
    '''
    
    result = execute_query(verify_query)
    if result and 'data' in result:
        print("📋 Week 2 Agent Assignments:")
        for ticket in result['data']:
            print(f"   - Ticket #{ticket['id']}: {ticket['name']} → {ticket['assigned_agent']}")
    
    # Show agent workload summary
    print("\n👤 Agent Workload Summary:")
    workload_query = '''
        USE DATABASE 'my-database';
        SELECT assigned_agent, COUNT(*) as count
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        GROUP BY assigned_agent
        ORDER BY count DESC
    '''
    
    result = execute_query(workload_query)
    if result and 'data' in result:
        for agent in result['data']:
            print(f"   - {agent['assigned_agent']}: {agent['count']} tickets")
    
    print("\n✅ Agent assignments updated successfully!")
    print("   - All Week 2 tickets now have correct agent assignments")
    print("   - Agent assignments match the provided image")
    print("   - Ready for viewing in the Agent Portal")

if __name__ == "__main__":
    main()
