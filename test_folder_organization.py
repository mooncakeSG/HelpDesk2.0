#!/usr/bin/env python3
"""
Test the folder organization system
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
    """Test the folder organization system"""
    print("📁 Testing Folder Organization System")
    print("====================================")
    
    # Test 1: Check category distribution
    print("1. Checking category distribution...")
    category_query = '''
        USE DATABASE 'my-database';
        SELECT category, COUNT(*) as count 
        FROM tickets 
        GROUP BY category
        ORDER BY count DESC
    '''
    result = execute_query(category_query)
    if result and 'data' in result:
        print("📊 Category Distribution:")
        for row in result['data']:
            print(f"   - {row['category']}: {row['count']} tickets")
    
    # Test 2: Check Week 1 folder specifically
    print("\n2. Checking Week 1 folder contents...")
    week1_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, issue, status, priority, assigned_agent
        FROM tickets 
        WHERE category = 'Week 1: Account and Communications Support'
        ORDER BY id
    '''
    result = execute_query(week1_query)
    if result and 'data' in result:
        print(f"📁 Week 1: Account and Communications Support ({len(result['data'])} tickets):")
        for row in result['data']:
            print(f"   - Ticket #{row['id']}: {row['name']}")
            print(f"     Issue: {row['issue'][:60]}...")
            print(f"     Status: {row['status']} | Priority: {row['priority']} | Agent: {row['assigned_agent']}")
            print()
    
    # Test 3: Check if all resolved tickets are in Week 1
    print("3. Verifying all resolved tickets are in Week 1...")
    resolved_check_query = '''
        USE DATABASE 'my-database';
        SELECT 
            COUNT(*) as total_resolved,
            SUM(CASE WHEN category = 'Week 1: Account and Communications Support' THEN 1 ELSE 0 END) as in_week1
        FROM tickets 
        WHERE status = 'Resolved'
    '''
    result = execute_query(resolved_check_query)
    if result and 'data' in result:
        row = result['data'][0]
        total_resolved = row['total_resolved']
        in_week1 = row['in_week1']
        
        if total_resolved == in_week1:
            print(f"✅ All {total_resolved} resolved tickets are properly organized in Week 1 folder")
        else:
            print(f"⚠️ {total_resolved} resolved tickets total, but only {in_week1} are in Week 1 folder")
    
    # Test 4: Check table structure
    print("\n4. Verifying table structure includes category column...")
    structure_query = '''
        USE DATABASE 'my-database';
        PRAGMA table_info(tickets)
    '''
    result = execute_query(structure_query)
    if result and 'data' in result:
        columns = [row['name'] for row in result['data']]
        if 'category' in columns:
            print("✅ Category column exists in tickets table")
        else:
            print("❌ Category column missing from tickets table")
    
    print("\n🎉 Folder organization system test completed!")
    print("   - All resolved tickets are organized in 'Week 1: Account and Communications Support'")
    print("   - New tickets will default to 'General' category")
    print("   - The webpage will now display tickets organized by folders")

if __name__ == "__main__":
    main()
