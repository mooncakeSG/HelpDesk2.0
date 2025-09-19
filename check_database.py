#!/usr/bin/env python3
"""
Check database status and troubleshoot import issues
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
        
        print(f"🔍 Query: {query}")
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
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
    """Main function"""
    print("🔍 Database Status Check")
    print("========================")
    
    # Test basic connection
    print("1. Testing basic connection...")
    test_query = "SELECT 1 as test"
    result = execute_query(test_query)
    
    # Check if database exists
    print("\n2. Checking database...")
    db_query = "USE DATABASE 'my-database'"
    result = execute_query(db_query)
    
    # Check if table exists
    print("\n3. Checking if tickets table exists...")
    table_query = '''
        USE DATABASE 'my-database';
        SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'
    '''
    result = execute_query(table_query)
    
    # Check table structure
    print("\n4. Checking table structure...")
    structure_query = '''
        USE DATABASE 'my-database';
        PRAGMA table_info(tickets)
    '''
    result = execute_query(structure_query)
    
    # Count tickets
    print("\n5. Counting tickets...")
    count_query = '''
        USE DATABASE 'my-database';
        SELECT COUNT(*) as total FROM tickets
    '''
    result = execute_query(count_query)
    
    # Show all tickets
    print("\n6. Showing all tickets...")
    all_tickets_query = '''
        USE DATABASE 'my-database';
        SELECT * FROM tickets
    '''
    result = execute_query(all_tickets_query)

if __name__ == "__main__":
    main()
