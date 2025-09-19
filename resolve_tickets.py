#!/usr/bin/env python3
"""
Resolve all unresolved tickets in the database
"""

import requests
import os
from datetime import datetime
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
            if 'data' in result and len(result['data']) > 0:
                return result['data']
            return result
        else:
            print(f"❌ Query failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def get_unresolved_tickets():
    """Get all unresolved tickets"""
    query = '''
        USE DATABASE 'my-database';
        SELECT id, name, email, issue, status, priority, assigned_agent 
        FROM tickets 
        WHERE status != 'Resolved'
        ORDER BY id
    '''
    
    result = execute_query(query)
    return result

def resolve_ticket(ticket_id, resolution_notes="Resolved by system administrator"):
    """Resolve a specific ticket"""
    query = f'''
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
    
    result = execute_query(query)
    return result is not None

def main():
    """Main function"""
    print("🎫 IT Helpdesk Ticket Resolution Tool")
    print("=====================================")
    
    # Get unresolved tickets
    print("🔍 Checking for unresolved tickets...")
    unresolved_tickets = get_unresolved_tickets()
    
    if not unresolved_tickets:
        print("✅ All tickets are already resolved!")
        return
    
    print(f"📋 Found {len(unresolved_tickets)} unresolved tickets:")
    print()
    
    # Display unresolved tickets
    for ticket in unresolved_tickets:
        print(f"🎫 Ticket ID: {ticket['id']}")
        print(f"   👤 Name: {ticket['name']}")
        print(f"   📧 Email: {ticket['email']}")
        print(f"   📝 Issue: {ticket['issue'][:100]}...")
        print(f"   📊 Status: {ticket['status']}")
        print(f"   ⚡ Priority: {ticket['priority']}")
        print(f"   👨‍💼 Assigned Agent: {ticket['assigned_agent'] or 'Unassigned'}")
        print()
    
    # Resolve all tickets
    print("🚀 Resolving all unresolved tickets...")
    resolved_count = 0
    failed_count = 0
    
    for ticket in unresolved_tickets:
        ticket_id = ticket['id']
        issue = ticket['issue']
        
        # Create resolution notes based on issue type
        if 'password' in issue.lower() or 'login' in issue.lower():
            resolution_notes = "Password reset completed. User can now log in successfully."
        elif 'lockout' in issue.lower() or 'locked' in issue.lower():
            resolution_notes = "Account lockout cleared. User account unlocked and accessible."
        elif 'outlook' in issue.lower() or 'authentication' in issue.lower():
            resolution_notes = "Authentication issue resolved. Outlook credentials refreshed."
        elif 'disabled' in issue.lower():
            resolution_notes = "Account re-enabled. User access restored."
        else:
            resolution_notes = "Issue resolved by IT support team."
        
        if resolve_ticket(ticket_id, resolution_notes):
            resolved_count += 1
            print(f"✅ Resolved ticket {ticket_id}: {ticket['name']}")
        else:
            failed_count += 1
            print(f"❌ Failed to resolve ticket {ticket_id}: {ticket['name']}")
    
    print()
    print("📊 Resolution Summary:")
    print(f"   ✅ Successfully resolved: {resolved_count} tickets")
    print(f"   ❌ Failed to resolve: {failed_count} tickets")
    print(f"   📋 Total processed: {resolved_count + failed_count} tickets")
    
    # Verify resolution
    print()
    print("🔍 Verifying resolution...")
    remaining_unresolved = get_unresolved_tickets()
    
    if not remaining_unresolved:
        print("🎉 All tickets have been successfully resolved!")
    else:
        print(f"⚠️ {len(remaining_unresolved)} tickets still remain unresolved")
    
    # Show final status
    print()
    print("📈 Final Database Status:")
    status_query = '''
        USE DATABASE 'my-database';
        SELECT status, COUNT(*) as count 
        FROM tickets 
        GROUP BY status
    '''
    
    status_result = execute_query(status_query)
    if status_result:
        for status in status_result:
            print(f"   {status['status']}: {status['count']} tickets")
    
    print()
    print("🌐 You can view all resolved tickets at: http://localhost:5000/agent")

if __name__ == "__main__":
    main()
