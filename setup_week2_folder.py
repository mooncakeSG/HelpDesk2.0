#!/usr/bin/env python3
"""
Set up Week 2: Software & Hardware Support folder and update default category
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
    """Set up Week 2 folder and update default category"""
    print("📁 Setting up Week 2: Software & Hardware Support")
    print("=================================================")
    
    # Step 1: Update default category for new tickets
    print("1. Updating default category for new tickets to Week 2...")
    update_default_query = '''
        USE DATABASE 'my-database';
        UPDATE tickets 
        SET category = 'Week 2: Software & Hardware Support' 
        WHERE category = 'General' OR category IS NULL
    '''
    result = execute_query(update_default_query)
    if result:
        print("✅ Default category updated to Week 2")
    
    # Step 2: Verify current category distribution
    print("\n2. Checking current category distribution...")
    category_query = '''
        USE DATABASE 'my-database';
        SELECT category, COUNT(*) as count 
        FROM tickets 
        GROUP BY category
        ORDER BY count DESC
    '''
    result = execute_query(category_query)
    if result and 'data' in result:
        print("📊 Current Category Distribution:")
        for row in result['data']:
            print(f"   - {row['category']}: {row['count']} tickets")
    
    # Step 3: Show sample tickets from each category
    print("\n3. Sample tickets from each category...")
    sample_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, issue, status, category 
        FROM tickets 
        ORDER BY category, id
        LIMIT 10
    '''
    result = execute_query(sample_query)
    if result and 'data' in result:
        current_category = None
        for row in result['data']:
            if row['category'] != current_category:
                current_category = row['category']
                print(f"\n📁 {current_category}:")
            print(f"   - Ticket #{row['id']}: {row['name']} - {row['issue'][:50]}...")
    
    # Step 4: Create a sample Week 2 ticket for demonstration
    print("\n4. Creating a sample Week 2 ticket for demonstration...")
    sample_ticket_query = '''
        USE DATABASE 'my-database';
        INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent, category)
        VALUES (
            '2025-09-19 16:00:00',
            'Demo User',
            'demo@company.com',
            'Sample Week 2 ticket - Software installation issue',
            '',
            'Open',
            'Medium',
            '',
            'Week 2: Software & Hardware Support'
        )
    '''
    result = execute_query(sample_ticket_query)
    if result:
        print("✅ Sample Week 2 ticket created")
    
    print("\n🎉 Week 2 folder setup completed!")
    print("   - Week 2: Software & Hardware Support is now the default category")
    print("   - All new tickets will be assigned to Week 2")
    print("   - Week 1 tickets remain organized in their folder")
    print("   - The webpage will now display both Week 1 and Week 2 folders")

if __name__ == "__main__":
    main()
