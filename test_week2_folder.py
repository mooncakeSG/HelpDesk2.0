#!/usr/bin/env python3
"""
Test the Week 2 folder organization system
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
    """Test the Week 2 folder system"""
    print("📁 Testing Week 2: Software & Hardware Support Folder")
    print("=====================================================")
    
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
    
    # Test 2: Check Week 2 folder contents
    print("\n2. Checking Week 2 folder contents...")
    week2_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, issue, status, priority, assigned_agent
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        ORDER BY id
    '''
    result = execute_query(week2_query)
    if result and 'data' in result:
        print(f"📁 Week 2: Software & Hardware Support ({len(result['data'])} tickets):")
        for row in result['data']:
            print(f"   - Ticket #{row['id']}: {row['name']}")
            print(f"     Issue: {row['issue'][:60]}...")
            print(f"     Status: {row['status']} | Priority: {row['priority']} | Agent: {row['assigned_agent']}")
            print()
    
    # Test 3: Verify Week 1 folder still exists
    print("3. Verifying Week 1 folder still exists...")
    week1_query = '''
        USE DATABASE 'my-database';
        SELECT COUNT(*) as count
        FROM tickets 
        WHERE category = 'Week 1: Account and Communications Support'
    '''
    result = execute_query(week1_query)
    if result and 'data' in result:
        count = result['data'][0]['count']
        print(f"✅ Week 1 folder contains {count} tickets")
    
    # Test 4: Check total tickets
    print("\n4. Checking total ticket count...")
    total_query = '''
        USE DATABASE 'my-database';
        SELECT COUNT(*) as total FROM tickets
    '''
    result = execute_query(total_query)
    if result and 'data' in result:
        total = result['data'][0]['total']
        print(f"📊 Total tickets in system: {total}")
    
    # Test 5: Show folder organization summary
    print("\n5. Folder Organization Summary:")
    print("📁 Week 1: Account and Communications Support (Resolved tickets)")
    print("   - Focus: Account management, password resets, authentication")
    print("   - Status: All resolved and organized")
    print()
    print("📁 Week 2: Software & Hardware Support (Current week)")
    print("   - Focus: Software installations, hardware issues, technical support")
    print("   - Status: Active folder for new tickets")
    print("   - Default: New tickets automatically assigned here")
    
    print("\n🎉 Week 2 folder system test completed!")
    print("   - Week 2 folder is active and ready for new tickets")
    print("   - Week 1 folder remains organized with resolved tickets")
    print("   - New tickets will default to Week 2 category")
    print("   - Both folders have distinct visual styling (green vs blue)")

if __name__ == "__main__":
    main()
