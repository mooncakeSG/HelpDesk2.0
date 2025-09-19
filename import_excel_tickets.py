#!/usr/bin/env python3
"""
Import tickets from Excel file to SQLiteCloud database
This script reads the Book.xlsx file and imports all tickets as resolved
"""

import pandas as pd
import requests
import os
from datetime import datetime
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
            if 'results' in result and len(result['results']) > 0:
                return result['results'][0]
            return result
        else:
            print(f"❌ Query failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def read_excel_tickets():
    """Read tickets from Excel file"""
    try:
        # Read the Excel file
        excel_file = "assests/Book.xlsx"
        df = pd.read_excel(excel_file, sheet_name='Ticket Tracker')
        
        print(f"📊 Found {len(df)} tickets in Excel file")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Display first few rows to understand structure
        print("\n📄 Sample data:")
        print(df.head())
        
        return df
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def import_tickets_to_database(df):
    """Import tickets from DataFrame to SQLiteCloud database"""
    imported_count = 0
    error_count = 0
    
    print(f"\n🚀 Starting import of {len(df)} tickets...")
    
    for index, row in df.iterrows():
        try:
            # Extract data from Excel row
            assigned_agent = str(row.get('AssignedAgent', '')).strip()
            incident_category = str(row.get('IncidentCategory', 'Account / Authentication')).strip()
            priority = str(row.get('Priority', 'Medium')).strip()
            brief_summary = str(row.get('BriefSummary', '')).strip()
            full_description = str(row.get('FullDescription', '')).strip()
            kb_article = str(row.get('KBArticleLinked', '')).strip()
            
            # Skip empty rows
            if not brief_summary or brief_summary == 'nan':
                continue
            
            # Create a name from the brief summary (first few words)
            name_parts = brief_summary.split()[:3]
            name = ' '.join(name_parts) if name_parts else 'User'
            
            # Create email (generic format)
            email = f"user{index + 1}@company.com"
            
            # Create timestamp (use current time for all imported tickets)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Escape single quotes to prevent SQL injection
            name_escaped = name.replace("'", "''")
            email_escaped = email.replace("'", "''")
            issue_escaped = full_description.replace("'", "''")
            priority_escaped = priority.replace("'", "''")
            assigned_agent_escaped = assigned_agent.replace("'", "''")
            
            # Create notes with KB article reference
            notes = f"Imported from Excel. Category: {incident_category}"
            if kb_article and kb_article != 'nan':
                notes += f" | KB Article: {kb_article}"
            notes_escaped = notes.replace("'", "''")
            
            # Insert ticket into database
            insert_query = f'''
                USE DATABASE 'my-database';
                INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent)
                VALUES ('{timestamp}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '{notes_escaped}', 'Resolved', '{priority_escaped}', '{assigned_agent_escaped}')
            '''
            
            result = execute_query(insert_query)
            if result is not None:
                imported_count += 1
                print(f"✅ Imported ticket {imported_count}: {brief_summary[:50]}...")
            else:
                error_count += 1
                print(f"❌ Failed to import ticket: {brief_summary[:50]}...")
                
        except Exception as e:
            error_count += 1
            print(f"❌ Error importing ticket {index + 1}: {e}")
    
    print(f"\n📊 Import Summary:")
    print(f"   ✅ Successfully imported: {imported_count} tickets")
    print(f"   ❌ Failed to import: {error_count} tickets")
    print(f"   📋 Total processed: {imported_count + error_count} tickets")
    
    return imported_count, error_count

def verify_import():
    """Verify that tickets were imported correctly"""
    print(f"\n🔍 Verifying import...")
    
    # Count total tickets
    count_query = '''
        USE DATABASE 'my-database';
        SELECT COUNT(*) as total FROM tickets
    '''
    
    result = execute_query(count_query)
    if result:
        total_tickets = result.get('total', 0)
        print(f"📊 Total tickets in database: {total_tickets}")
        
        # Count resolved tickets
        resolved_query = '''
            USE DATABASE 'my-database';
            SELECT COUNT(*) as resolved FROM tickets WHERE status = 'Resolved'
        '''
        
        result = execute_query(resolved_query)
        if result:
            resolved_tickets = result.get('resolved', 0)
            print(f"✅ Resolved tickets: {resolved_tickets}")
        
        # Show recent tickets
        recent_query = '''
            USE DATABASE 'my-database';
            SELECT id, name, issue, status, priority, assigned_agent 
            FROM tickets 
            ORDER BY id DESC 
            LIMIT 5
        '''
        
        result = execute_query(recent_query)
        if result and 'rows' in result:
            print(f"\n📋 Recent tickets:")
            for row in result['rows']:
                print(f"   ID {row.get('id', 'N/A')}: {row.get('name', 'N/A')} - {row.get('status', 'N/A')} ({row.get('priority', 'N/A')})")

def main():
    """Main function"""
    print("🎫 IT Helpdesk Excel Import Tool")
    print("================================")
    
    # Test database connection
    print("🔌 Testing database connection...")
    test_query = "USE DATABASE 'my-database'; SELECT 1 as test"
    result = execute_query(test_query)
    
    if result is None:
        print("❌ Cannot connect to SQLiteCloud database. Please check your credentials.")
        return
    
    print("✅ Database connection successful")
    
    # Read Excel file
    print("\n📖 Reading Excel file...")
    df = read_excel_tickets()
    
    if df is None or df.empty:
        print("❌ No data found in Excel file")
        return
    
    # Import tickets
    imported_count, error_count = import_tickets_to_database(df)
    
    # Verify import
    if imported_count > 0:
        verify_import()
    
    print(f"\n🎉 Import completed!")
    print(f"   You can now view the imported tickets at: http://localhost:5000/agent")

if __name__ == "__main__":
    main()
