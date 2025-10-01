#!/usr/bin/env python3
"""
Verify Week 3 ticket import and clean up duplicates if needed
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
    print("Error: SQLITECLOUD_API_KEY and SQLITECLOUD_URL must be set in environment variables")
    exit(1)

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
            return result
        else:
            print(f"Query failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def main():
    """Verify Week 3 ticket import"""
    print("Verifying Week 3 ticket import...")
    print("=================================")
    
    # Check all Week 3 tickets
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT id, timestamp, name, issue, status, priority, assigned_agent, category
        FROM tickets 
        WHERE category = 'Week 3: Performance & Optimization Support'
        ORDER BY id
    '''
    
    result = execute_query(verify_query)
    
    if result and 'data' in result:
        print(f"Found {len(result['data'])} Week 3 tickets:")
        print()
        
        for row in result['data']:
            if isinstance(row, dict):
                print(f"ID: {row.get('id', 'N/A')}")
                print(f"Time: {row.get('timestamp', 'N/A')}")
                print(f"Name: {row.get('name', 'N/A')}")
                print(f"Issue: {str(row.get('issue', 'N/A'))[:100]}...")
                print(f"Status: {row.get('status', 'N/A')}")
                print(f"Priority: {row.get('priority', 'N/A')}")
                print(f"Agent: {row.get('assigned_agent', 'N/A')}")
                print(f"Category: {row.get('category', 'N/A')}")
                print("-" * 50)
            else:
                print(f"Row data: {row}")
                print("-" * 50)
        
        # Check for duplicates
        if len(result['data']) > 2:
            print(f"\nWARNING: Found {len(result['data'])} tickets, expected 2. There may be duplicates.")
            
            # Get unique tickets by content
            unique_tickets = {}
            for row in result['data']:
                if isinstance(row, dict):
                    key = f"{row.get('name', '')}_{row.get('issue', '')[:50]}"
                    if key not in unique_tickets:
                        unique_tickets[key] = row
                    else:
                        print(f"Duplicate found: ID {row.get('id', 'N/A')} - {row.get('name', 'N/A')}")
            
            print(f"Unique tickets: {len(unique_tickets)}")
            
            # Ask if user wants to clean up duplicates
            if len(unique_tickets) < len(result['data']):
                print("\nTo clean up duplicates, you can run a cleanup script.")
        else:
            print(f"\nSUCCESS: Found exactly {len(result['data'])} Week 3 tickets as expected.")
    
    else:
        print("No Week 3 tickets found in database")
    
    # Show category distribution
    print("\nCategory Distribution:")
    print("=====================")
    category_query = '''
        USE DATABASE 'my-database';
        SELECT category, COUNT(*) as count 
        FROM tickets 
        GROUP BY category
        ORDER BY count DESC
    '''
    
    result = execute_query(category_query)
    if result and 'data' in result:
        for row in result['data']:
            if isinstance(row, dict):
                print(f"   - {row.get('category', 'N/A')}: {row.get('count', 'N/A')} tickets")
            else:
                print(f"   - Row: {row}")

if __name__ == "__main__":
    main()
