#!/usr/bin/env python3
"""
Script to update the database schema with priority and assigned_agent columns
"""

import requests
import os

# Set environment variables
os.environ['SQLITECLOUD_API_KEY'] = 'FpQNNvLCTlRGFvVlOnBuQbqNel3b0wPDs9u6jO2HsWU'
os.environ['SQLITECLOUD_URL'] = 'https://crihbwjchz.g5.sqlite.cloud:443/v2/weblite/sql'

api_key = os.environ['SQLITECLOUD_API_KEY']
api_url = os.environ['SQLITECLOUD_URL']
headers = {'Authorization': f'Bearer {api_key}'}

def execute_sql(sql_command):
    """Execute a single SQL command"""
    payload = {'sql': sql_command}
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Success: {sql_command[:50]}...")
            return True
        else:
            print(f"❌ Error {response.status_code}: {sql_command[:50]}...")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def update_database():
    """Update the database schema"""
    print("🚀 Updating database schema...")
    print("=" * 50)
    
    # List of SQL commands to execute
    commands = [
        "USE DATABASE 'my-database'; ALTER TABLE tickets ADD COLUMN priority TEXT DEFAULT 'Medium'",
        "USE DATABASE 'my-database'; ALTER TABLE tickets ADD COLUMN assigned_agent TEXT DEFAULT ''",
        "USE DATABASE 'my-database'; CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority)",
        "USE DATABASE 'my-database'; CREATE INDEX IF NOT EXISTS idx_tickets_assigned_agent ON tickets(assigned_agent)",
        "USE DATABASE 'my-database'; UPDATE tickets SET priority = 'Medium' WHERE priority IS NULL",
        "USE DATABASE 'my-database'; UPDATE tickets SET assigned_agent = '' WHERE assigned_agent IS NULL"
    ]
    
    success_count = 0
    for command in commands:
        if execute_sql(command):
            success_count += 1
    
    print("=" * 50)
    print(f"🎉 Database update completed!")
    print(f"✅ Successful commands: {success_count}/{len(commands)}")
    
    if success_count > 0:
        print("\n🌐 Database schema updated with priority and agent assignment!")

if __name__ == "__main__":
    update_database()
