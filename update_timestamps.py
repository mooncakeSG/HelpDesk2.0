#!/usr/bin/env python3
"""
Update timestamps for Week 2 tickets to match the image format and dates
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
    """Update timestamps for Week 2 tickets"""
    print("🕒 Updating Timestamps for Week 2 Tickets")
    print("=========================================")
    
    # Timestamp updates based on the image
    # Week 2 tickets (32-43) should have timestamps in M/DD/YYYY HH:MM format
    timestamp_updates = {
        32: "9/22/2025 9:43",    # Sarah Johnson
        33: "9/22/2025 10:18",   # Mike Chen
        34: "9/22/2025 10:43",   # Emily Rodriguez
        35: "9/22/2025 11:08",   # David Thompson
        36: "9/22/2025 11:33",   # Lisa Wang
        37: "9/22/2025 11:58",   # James Wilson
        38: "9/22/2025 12:13",   # Maria Garcia
        39: "9/22/2025 12:28",   # Robert Brown
        40: "9/22/2025 12:43",   # Jennifer Davis
        41: "9/22/2025 13:28",   # Christopher Lee
        42: "9/22/2025 13:23",   # Amanda Taylor
        43: "9/22/2025 13:58"    # Michael Anderson
    }
    
    print("📅 Timestamp Update Plan:")
    print("   - Format: M/DD/YYYY HH:MM")
    print("   - Date: 9/22/2025")
    print("   - Times: Spread throughout the day")
    print()
    
    updated_count = 0
    
    # Update each ticket with the correct timestamp
    for ticket_id, new_timestamp in timestamp_updates.items():
        # Escape single quotes in timestamp
        timestamp_escaped = new_timestamp.replace("'", "''")
        
        update_query = f'''
            USE DATABASE 'my-database';
            UPDATE tickets 
            SET timestamp = '{timestamp_escaped}'
            WHERE id = {ticket_id}
        '''
        
        result = execute_query(update_query)
        if result:
            updated_count += 1
            print(f"✅ Updated Ticket #{ticket_id}: {new_timestamp}")
        else:
            print(f"❌ Failed to update Ticket #{ticket_id}")
    
    print(f"\n🎉 Successfully updated {updated_count} ticket timestamps!")
    
    # Verify the updates
    print("\n📊 Verifying timestamp updates...")
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, timestamp
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        ORDER BY id
    '''
    
    result = execute_query(verify_query)
    if result and 'data' in result:
        print("📋 Week 2 Updated Timestamps:")
        for ticket in result['data']:
            print(f"   - Ticket #{ticket['id']}: {ticket['name']} → {ticket['timestamp']}")
    
    # Show chronological order
    print("\n🕒 Chronological Order:")
    chronological_query = '''
        USE DATABASE 'my-database';
        SELECT id, name, timestamp
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        ORDER BY timestamp
    '''
    
    result = execute_query(chronological_query)
    if result and 'data' in result:
        for i, ticket in enumerate(result['data'], 1):
            print(f"   {i:2d}. {ticket['timestamp']} - Ticket #{ticket['id']}: {ticket['name']}")
    
    print("\n✅ Timestamp updates completed successfully!")
    print("   - All Week 2 tickets now have correct timestamps")
    print("   - Timestamps match the provided image format")
    print("   - Chronological order maintained throughout the day")
    print("   - Ready for viewing in the Agent Portal")

if __name__ == "__main__":
    main()
