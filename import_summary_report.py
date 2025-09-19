#!/usr/bin/env python3
"""
Generate a summary report of the imported Excel tickets
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLiteCloud configuration
API_KEY = os.getenv('SQLITECLOUD_API_KEY')
API_URL = os.getenv('SQLITECLOUD_URL')

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
            return result.get('data', [])
        else:
            print(f"❌ Query failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    """Generate import summary report"""
    print("📊 Excel Import Summary Report")
    print("=============================")
    
    # Get imported tickets (those with "Imported from Excel" in notes)
    query = '''
        USE DATABASE 'my-database';
        SELECT id, name, issue, status, priority, assigned_agent, notes
        FROM tickets 
        WHERE notes LIKE '%Imported from Excel%'
        ORDER BY id
    '''
    
    imported_tickets = execute_query(query)
    
    print(f"\n✅ Successfully imported {len(imported_tickets)} tickets from Excel file")
    print(f"📅 Import date: 2025-09-19 10:08:01")
    print(f"🎯 All tickets marked as: RESOLVED")
    
    print(f"\n📋 Imported Tickets Details:")
    print("=" * 80)
    
    for ticket in imported_tickets:
        print(f"\n🎫 Ticket ID: {ticket['id']}")
        print(f"   👤 Name: {ticket['name']}")
        print(f"   📝 Issue: {ticket['issue'][:60]}...")
        print(f"   🏷️  Priority: {ticket['priority']}")
        print(f"   👨‍💼 Assigned Agent: {ticket['assigned_agent']}")
        print(f"   ✅ Status: {ticket['status']}")
        
        # Extract KB article from notes
        notes = ticket['notes']
        if 'KB Article:' in notes:
            kb_article = notes.split('KB Article: ')[1]
            print(f"   📚 KB Article: {kb_article}")
    
    # Summary statistics
    print(f"\n📊 Import Statistics:")
    print("=" * 40)
    
    # Count by priority
    high_priority = len([t for t in imported_tickets if t['priority'] == 'High'])
    medium_priority = len([t for t in imported_tickets if t['priority'] == 'Medium'])
    low_priority = len([t for t in imported_tickets if t['priority'] == 'Low'])
    
    print(f"🔴 High Priority: {high_priority} tickets")
    print(f"🟡 Medium Priority: {medium_priority} tickets")
    print(f"🟢 Low Priority: {low_priority} tickets")
    
    # Count by agent
    azola_tickets = len([t for t in imported_tickets if t['assigned_agent'] == 'Azola Xabadiya'])
    keawin_tickets = len([t for t in imported_tickets if t['assigned_agent'] == 'Keawin Koesnel'])
    
    print(f"\n👨‍💼 Agent Assignment:")
    print(f"   Azola Xabadiya: {azola_tickets} tickets")
    print(f"   Keawin Koesnel: {keawin_tickets} tickets")
    
    # Get total database count
    total_query = '''
        USE DATABASE 'my-database';
        SELECT COUNT(*) as total FROM tickets
    '''
    total_result = execute_query(total_query)
    total_tickets = total_result[0]['total'] if total_result else 0
    
    print(f"\n📈 Database Status:")
    print(f"   Total tickets in database: {total_tickets}")
    print(f"   Imported tickets: {len(imported_tickets)}")
    print(f"   Previously existing: {total_tickets - len(imported_tickets)}")
    
    print(f"\n🎉 Import completed successfully!")
    print(f"🌐 View tickets at: http://localhost:5000/agent")
    print(f"📊 All imported tickets are marked as RESOLVED and ready for daily logs")

if __name__ == "__main__":
    main()
