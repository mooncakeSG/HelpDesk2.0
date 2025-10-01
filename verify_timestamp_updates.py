#!/usr/bin/env python3
"""
Verify that timestamp updates match the image requirements
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
    """Verify timestamp updates match the image"""
    print("🕒 Verifying Timestamp Updates for Week 2 Tickets")
    print("================================================")
    
    # Expected timestamps based on the image
    expected_timestamps = {
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
    
    # Fetch current timestamps from database
    query = '''
        USE DATABASE 'my-database';
        SELECT id, name, timestamp
        FROM tickets 
        WHERE category = 'Week 2: Software & Hardware Support'
        AND id BETWEEN 32 AND 43
        ORDER BY id
    '''
    
    result = execute_query(query)
    if not result or 'data' not in result:
        print("❌ Failed to fetch ticket data")
        return
    
    tickets = result['data']
    
    print("📋 Verification Results:")
    print("-" * 60)
    
    all_correct = True
    
    for ticket in tickets:
        ticket_id = ticket['id']
        name = ticket['name']
        current_timestamp = ticket['timestamp']
        expected_timestamp = expected_timestamps.get(ticket_id, 'Unknown')
        
        is_correct = current_timestamp == expected_timestamp
        status = "✅" if is_correct else "❌"
        
        print(f"{status} Ticket #{ticket_id}: {name}")
        print(f"   Expected: {expected_timestamp}")
        print(f"   Actual:   {current_timestamp}")
        print()
        
        if not is_correct:
            all_correct = False
    
    # Summary
    print("📊 Summary:")
    print("-" * 20)
    
    if all_correct:
        print("🎉 All timestamps are correct!")
        print("   - All 12 Week 2 tickets have the correct timestamps")
        print("   - Timestamps match the provided image exactly")
        print("   - Format: M/DD/YYYY HH:MM")
        print("   - Date: 9/22/2025")
        print("   - Ready for viewing in the Agent Portal")
    else:
        print("❌ Some timestamps are incorrect")
        print("   - Please check the timestamps and update as needed")
    
    # Show chronological order
    print("\n🕒 Chronological Order (by timestamp):")
    print("-" * 45)
    
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
    
    # Show time distribution
    print("\n📅 Time Distribution:")
    print("-" * 25)
    
    morning_count = 0
    afternoon_count = 0
    
    for ticket in tickets:
        timestamp = ticket['timestamp']
        if '9:' in timestamp or '10:' in timestamp or '11:' in timestamp:
            morning_count += 1
        elif '12:' in timestamp or '13:' in timestamp:
            afternoon_count += 1
    
    print(f"   🌅 Morning (9:00-11:59): {morning_count} tickets")
    print(f"   🌞 Afternoon (12:00-13:59): {afternoon_count} tickets")
    print(f"   📊 Total: {len(tickets)} tickets")
    
    print(f"\n✅ Timestamp verification completed!")

if __name__ == "__main__":
    main()

