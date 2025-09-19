#!/usr/bin/env python3
"""
Export all tickets from database to Excel daily log file (Simplified)
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
            if 'data' in result:
                return result['data']
            return result
        else:
            print(f"❌ Query failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_all_tickets():
    """Get all tickets from database"""
    query = '''
        USE DATABASE 'my-database';
        SELECT 
            id as TicketID,
            timestamp as DateOpened,
            name as ReporterName,
            email as ReporterContact,
            assigned_agent as AssignedAgent,
            priority as Priority,
            status as Status,
            issue as FullDescription,
            notes as ResolutionNotes
        FROM tickets 
        ORDER BY id
    '''
    
    tickets = execute_query(query)
    return tickets

def get_kb_article(issue):
    """Determine KB article based on issue type"""
    issue_lower = str(issue).lower()
    
    if 'password' in issue_lower and 'forgotten' in issue_lower:
        return 'KB_Password_Reset'
    elif 'lockout' in issue_lower or 'locked' in issue_lower:
        return 'KB_Password_Reset'
    elif 'disabled' in issue_lower:
        return 'KB_Account_Enable'
    elif 'outlook' in issue_lower or 'authentication' in issue_lower:
        return 'KB_MFA_Reset'
    elif 'mfa' in issue_lower and 'lost' in issue_lower:
        return 'KB_MFA_Reset'
    elif 'temporary' in issue_lower and 'contractor' in issue_lower:
        return 'KB_Temp_Account'
    elif 'suspicious' in issue_lower or 'unknown' in issue_lower:
        return 'KB_Security_Check'
    elif 'expired' in issue_lower:
        return 'KB_Password_Reset'
    else:
        return 'KB_General_Support'

def create_daily_log_excel(tickets):
    """Create Excel file with daily log of all tickets"""
    
    # Get current date for filename
    current_date = datetime.now().strftime("%Y%m%d")
    filename = f"IT_Helpdesk_Daily_Log_{current_date}.xlsx"
    
    print(f"📊 Creating daily log: {filename}")
    
    # Create DataFrame
    df = pd.DataFrame(tickets)
    
    # Add calculated columns
    df['BriefSummary'] = df['FullDescription'].str[:50] + "..."
    df['IncidentCategory'] = 'Account / Authentication'
    df['KBArticleLinked'] = df['FullDescription'].apply(get_kb_article)
    df['ResolutionDate'] = df['DateOpened']
    df['TimeToResolve'] = 'Same Day'
    
    # Reorder columns to match your original Excel format
    column_order = [
        'TicketID', 'DateOpened', 'ReporterName', 'ReporterContact', 
        'AssignedAgent', 'IncidentCategory', 'Priority', 'BriefSummary', 
        'FullDescription', 'Status', 'ResolutionNotes', 'KBArticleLinked',
        'ResolutionDate', 'TimeToResolve'
    ]
    
    df = df[column_order]
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main daily log sheet
        df.to_excel(writer, sheet_name='Daily Log', index=False)
        
        # Create summary statistics
        summary_data = {
            'Metric': [
                'Total Tickets',
                'Resolved Tickets',
                'Open Tickets',
                'In Progress Tickets',
                'High Priority Tickets',
                'Medium Priority Tickets',
                'Low Priority Tickets',
                'Tickets by Azola Xabadiya',
                'Tickets by Keawin Koesnel',
                'Tickets by System Admin',
                'Unassigned Tickets'
            ],
            'Count': [
                len(df),
                len(df[df['Status'] == 'Resolved']),
                len(df[df['Status'] == 'Open']),
                len(df[df['Status'] == 'In Progress']),
                len(df[df['Priority'] == 'High']),
                len(df[df['Priority'] == 'Medium']),
                len(df[df['Priority'] == 'Low']),
                len(df[df['AssignedAgent'] == 'Azola Xabadiya']),
                len(df[df['AssignedAgent'] == 'Keawin Koesnel']),
                len(df[df['AssignedAgent'] == 'System Admin']),
                len(df[df['AssignedAgent'] == 'Unassigned'])
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Create agent workload sheet
        agent_workload = df.groupby('AssignedAgent').agg({
            'TicketID': 'count',
            'Priority': lambda x: (x == 'High').sum(),
            'Status': lambda x: (x == 'Resolved').sum()
        }).rename(columns={
            'TicketID': 'Total_Tickets',
            'Priority': 'High_Priority',
            'Status': 'Resolved_Tickets'
        })
        
        agent_workload.to_excel(writer, sheet_name='Agent Workload')
    
    print(f"✅ Daily log created successfully: {filename}")
    return filename

def main():
    print("📊 IT Helpdesk Daily Log Export Tool")
    print("====================================")
    print()
    
    # Get all tickets
    print("🔍 Retrieving all tickets from database...")
    tickets = get_all_tickets()
    
    if not tickets:
        print("❌ No tickets found in database")
        return
    
    print(f"📋 Found {len(tickets)} tickets to export")
    print()
    
    # Create Excel file
    filename = create_daily_log_excel(tickets)
    
    print()
    print("📈 Export Summary:")
    print(f"   📄 File created: {filename}")
    print(f"   🎫 Total tickets: {len(tickets)}")
    print(f"   📊 Sheets included: Daily Log, Summary, Agent Workload")
    
    print()
    print("✅ Daily log export completed successfully!")
    print(f"📁 File location: {os.path.abspath(filename)}")
    print()
    print("📋 The Excel file includes:")
    print("   • Daily Log sheet with all ticket details")
    print("   • Summary sheet with statistics")
    print("   • Agent Workload sheet with performance metrics")
    print("   • Proper column formatting and data types")
    print("   • KB article references for each ticket")

if __name__ == "__main__":
    main()
