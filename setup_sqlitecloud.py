#!/usr/bin/env python3
"""
SQLiteCloud Setup Helper Script
This script helps you test your SQLiteCloud connection and get the correct API URL.
"""

import requests
import os
from dotenv import load_dotenv

def test_sqlitecloud_connection():
    """Test the SQLiteCloud API connection"""
    load_dotenv()
    
    api_key = os.getenv("SQLITECLOUD_API_KEY")
    api_url = os.getenv("SQLITECLOUD_URL")
    
    if not api_key:
        print("❌ SQLITECLOUD_API_KEY not found in environment variables")
        return False
    
    if not api_url:
        print("❌ SQLITECLOUD_URL not found in environment variables")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 API URL: {api_url}")
    
    # Test the connection
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Try a simple query to test the connection (include USE DATABASE in the same request)
    test_query = {
        "sql": "USE DATABASE 'my-database'; SELECT 1 as test"
    }
    
    try:
        print("\n🔄 Testing connection...")
        response = requests.post(api_url, json=test_query, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Connection successful!")
            print(f"📊 Response: {response.json()}")
            return True
        else:
            print(f"❌ Connection failed with status code: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def create_sample_table():
    """Create the tickets table in SQLiteCloud"""
    load_dotenv()
    
    api_key = os.getenv("SQLITECLOUD_API_KEY")
    api_url = os.getenv("SQLITECLOUD_URL")
    
    if not api_key or not api_url:
        print("❌ Environment variables not set")
        return False
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Create the tickets table (include USE DATABASE in the same request)
        create_table_query = {
            "sql": """
            USE DATABASE 'my-database';
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                issue TEXT NOT NULL,
                notes TEXT DEFAULT '',
                status TEXT DEFAULT 'Open' CHECK (status IN ('Open', 'In Progress', 'Resolved'))
            )
            """
        }
        
        print("\n🔄 Creating tickets table...")
        response = requests.post(api_url, json=create_table_query, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Table created successfully!")
            return True
        else:
            print(f"❌ Table creation failed with status code: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating table: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SQLiteCloud Setup Helper")
    print("=" * 40)
    
    # Test connection
    if test_sqlitecloud_connection():
        print("\n" + "=" * 40)
        # Create table if connection is successful
        create_sample_table()
    else:
        print("\n❌ Setup failed. Please check your configuration.")
        print("\n📋 Troubleshooting tips:")
        print("1. Make sure your .env file exists and has the correct values")
        print("2. Verify your API key is correct")
        print("3. Check that your API URL follows the format: https://api.sqlitecloud.io/v1/db/[DATABASE_ID]/query")
        print("4. Ensure your SQLiteCloud account is active")
