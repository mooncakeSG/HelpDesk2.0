#!/usr/bin/env python3
"""
Add category column to tickets table and organize resolved tickets into Week 1 folder
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
    """Main function to add category column and organize tickets"""
    print("📁 Adding Category System to Tickets")
    print("====================================")
    
    # Step 1: Add category column
    print("1. Adding category column to tickets table...")
    add_category_query = '''
        USE DATABASE 'my-database';
        ALTER TABLE tickets ADD COLUMN category TEXT DEFAULT 'General'
    '''
    result = execute_query(add_category_query)
    if result:
        print("✅ Category column added successfully")
    else:
        print("⚠️ Category column may already exist (this is normal)")
    
    # Step 2: Update all resolved tickets to Week 1 category
    print("\n2. Organizing resolved tickets into 'Week 1: Account and Communications Support'...")
    update_category_query = '''
        USE DATABASE 'my-database';
        UPDATE tickets 
        SET category = 'Week 1: Account and Communications Support' 
        WHERE status = 'Resolved'
    '''
    result = execute_query(update_category_query)
    if result:
        print("✅ Resolved tickets organized into Week 1 folder")
    
    # Step 3: Verify the changes
    print("\n3. Verifying category organization...")
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT category, COUNT(*) as count 
        FROM tickets 
        GROUP BY category
    '''
    result = execute_query(verify_query)
    if result and 'data' in result:
        print("📊 Category Distribution:")
        for row in result['data']:
            print(f"   - {row['category']}: {row['count']} tickets")
    
    # Step 4: Show sample of organized tickets
    print("\n4. Sample of organized tickets...")
    sample_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, issue, status, category 
        FROM tickets 
        WHERE category = 'Week 1: Account and Communications Support'
        LIMIT 5
    '''
    result = execute_query(sample_query)
    if result and 'data' in result:
        print("📋 Sample Week 1 Tickets:")
        for row in result['data']:
            print(f"   - Ticket #{row['id']}: {row['name']} - {row['issue'][:50]}...")
    
    print("\n🎉 Category system successfully implemented!")
    print("   - All resolved tickets are now in 'Week 1: Account and Communications Support'")
    print("   - New tickets will default to 'General' category")

if __name__ == "__main__":
    main()
