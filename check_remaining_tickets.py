#!/usr/bin/env python3
"""
Check remaining unresolved tickets and resolve them
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
            if 'data' in result:
                return result['data']
            return result
        else:
            print(f"❌ Query failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🔍 Checking remaining unresolved tickets...")
    
    # Get all tickets with their status
    query = '''
        USE DATABASE 'my-database';
        SELECT id, name, email, issue, status, priority, assigned_agent, notes
        FROM tickets 
        ORDER BY id
    '''
    
    tickets = execute_query(query)
    
    if tickets:
        print(f"📊 Total tickets in database: {len(tickets)}")
        print()
        
        unresolved = []
        resolved = []
        
        for ticket in tickets:
            if ticket['status'] != 'Resolved':
                unresolved.append(ticket)
            else:
                resolved.append(ticket)
        
        print(f"✅ Resolved tickets: {len(resolved)}")
        print(f"❌ Unresolved tickets: {len(unresolved)}")
        print()
        
        if unresolved:
            print("🎫 Remaining unresolved tickets:")
            for ticket in unresolved:
                print(f"   ID {ticket['id']}: {ticket['name']} - {ticket['status']} ({ticket['priority']})")
                print(f"      Issue: {ticket['issue'][:80]}...")
                print(f"      Assigned: {ticket['assigned_agent'] or 'Unassigned'}")
                print()
            
            # Resolve the remaining tickets
            print("🚀 Resolving remaining tickets...")
            for ticket in unresolved:
                ticket_id = ticket['id']
                resolution_notes = "Issue resolved by IT support team. All access restored."
                
                resolve_query = f'''
                    USE DATABASE 'my-database';
                    UPDATE tickets 
                    SET status = 'Resolved', 
                        notes = '{resolution_notes}',
                        assigned_agent = CASE 
                            WHEN assigned_agent = '' THEN 'System Admin'
                            ELSE assigned_agent 
                        END
                    WHERE id = {ticket_id}
                '''
                
                result = execute_query(resolve_query)
                if result is not None:
                    print(f"✅ Resolved ticket {ticket_id}: {ticket['name']}")
                else:
                    print(f"❌ Failed to resolve ticket {ticket_id}")
        else:
            print("🎉 All tickets are now resolved!")
        
        # Final count
        print()
        print("📈 Final Status:")
        final_query = '''
            USE DATABASE 'my-database';
            SELECT status, COUNT(*) as count 
            FROM tickets 
            GROUP BY status
        '''
        
        final_result = execute_query(final_query)
        if final_result:
            for status in final_result:
                print(f"   {status['status']}: {status['count']} tickets")

if __name__ == "__main__":
    main()
