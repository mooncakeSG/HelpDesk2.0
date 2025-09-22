#!/usr/bin/env python3
"""
Import Week 2 tickets from the text file with comprehensive notes
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

def get_comprehensive_notes(issue_description, priority):
    """Generate comprehensive resolution notes based on issue type"""
    
    if "laptop takes 15 minutes to boot" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed slow boot performance issue
2. Checked startup programs and services:
   - Disabled unnecessary startup applications
   - Removed bloatware and trial software
3. Performed disk cleanup and defragmentation
4. Updated device drivers (especially storage drivers)
5. Checked for malware and viruses
6. Optimized Windows startup settings
7. Replaced failing HDD with SSD (if applicable)
8. Updated BIOS/UEFI firmware
9. Tested boot performance - reduced to 2-3 minutes
10. Provided user training on system maintenance

RESOLUTION: Laptop boot time significantly improved. System now boots in under 3 minutes."""

    elif "bsod" in issue_description.lower() and "external monitor" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed BSOD related to external monitor connection
2. Checked display drivers and updated to latest version
3. Tested different HDMI cables and ports
4. Verified monitor compatibility and resolution settings
5. Updated graphics card drivers
6. Checked Windows display settings and scaling
7. Tested with different external monitors
8. Updated BIOS/UEFI settings for display output
9. Resolved driver conflicts in Device Manager
10. Tested connection stability over extended period

RESOLUTION: External monitor connection issue resolved. No more BSOD when connecting via HDMI."""

    elif "unidentified network" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed network connectivity issue
2. Checked network adapter settings and drivers
3. Verified IP configuration and DNS settings
4. Reset network adapter to factory defaults
5. Updated network card drivers
6. Checked Windows network services
7. Verified router/switch port functionality
8. Tested with different network cables
9. Configured static IP if DHCP issues persist
10. Updated Windows network stack

RESOLUTION: Network connectivity restored. Desktop now properly connects to network and internet."""

    elif "replacement laptop" in issue_description.lower() and "burglary" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Addressed urgent laptop replacement request
2. Verified incident report and police documentation
3. Checked available inventory for immediate replacement
4. Expedited procurement process for new laptop
5. Coordinated with security team for data protection
6. Set up new laptop with user's profile and applications
7. Transferred essential data from backups
8. Implemented additional security measures
9. Provided temporary loaner laptop within 2 hours
10. Scheduled follow-up for permanent replacement

RESOLUTION: Emergency laptop replacement provided within 2 hours. User can continue working immediately."""

    elif "fan is always loud" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed overheating and fan noise issue
2. Opened laptop and cleaned dust from fans and vents
3. Replaced thermal paste on CPU and GPU
4. Checked for blocked air vents
5. Updated BIOS to latest version
6. Optimized power settings to reduce heat generation
7. Installed temperature monitoring software
8. Replaced failing fan if necessary
9. Tested system under load for 1 hour
10. Provided user guidance on proper laptop ventilation

RESOLUTION: Fan noise significantly reduced. System maintains normal temperature under load."""

    elif "usb device" in issue_description.lower() and "crashes" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed USB device compatibility issue
2. Tested USB device on different computers
3. Updated USB drivers and chipset drivers
4. Checked USB port functionality
5. Updated Windows USB stack
6. Verified device compatibility with system
7. Tested with different USB devices
8. Updated BIOS/UEFI USB settings
9. Resolved driver conflicts in Device Manager
10. Provided compatible USB device recommendations

RESOLUTION: USB compatibility issue resolved. Device now works without causing system crashes."""

    elif "wi-fi connects but no internet" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed Wi-Fi connectivity issue
2. Checked network adapter settings and drivers
3. Verified DNS configuration and settings
4. Reset network adapter to factory defaults
5. Updated Wi-Fi drivers to latest version
6. Checked Windows network services
7. Verified router/access point configuration
8. Tested with different Wi-Fi networks
9. Configured static DNS servers (8.8.8.8, 8.8.4.4)
10. Updated Windows network stack

RESOLUTION: Wi-Fi internet connectivity restored. User can now access internet through Wi-Fi."""

    elif "laptop was stolen" in issue_description.lower() and "coffee shop" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Addressed urgent security incident
2. Immediately initiated remote wipe procedures
3. Changed all user passwords and credentials
4. Notified security team and management
5. Filed police report and insurance claim
6. Provided replacement laptop within 4 hours
7. Restored data from backups
8. Implemented additional security measures
9. Provided security training to user
10. Updated company security policies

RESOLUTION: Security incident handled. All data remotely wiped, replacement provided, user can continue working securely."""

    elif "unresponsive" in issue_description.lower() and "browser tabs" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed browser performance issue
2. Checked system memory usage and availability
3. Updated browser to latest version
4. Cleared browser cache and temporary files
5. Disabled unnecessary browser extensions
6. Increased virtual memory allocation
7. Updated graphics drivers
8. Optimized browser settings for performance
9. Provided user training on tab management
10. Recommended browser alternatives if needed

RESOLUTION: Browser performance improved. System now handles multiple tabs without becoming unresponsive."""

    elif "bsod" in issue_description.lower() and "windows updates" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed BSOD after Windows updates
2. Booted into Safe Mode
3. Uninstalled problematic Windows updates
4. Updated device drivers to latest versions
5. Ran System File Checker (SFC) scan
6. Performed DISM repair operations
7. Updated BIOS/UEFI firmware
8. Tested system stability
9. Reinstalled updates in controlled manner
10. Set up automatic driver updates

RESOLUTION: BSOD issue resolved. System now boots normally after Windows updates."""

    elif "network works on phone" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Diagnosed laptop-specific network issue
2. Checked network adapter settings and drivers
3. Verified IP configuration and DNS settings
4. Reset network adapter to factory defaults
5. Updated network card drivers
6. Checked Windows network services
7. Verified router/switch port functionality
8. Tested with different network cables
9. Configured static IP if DHCP issues persist
10. Updated Windows network stack

RESOLUTION: Laptop network connectivity restored. Now matches phone network performance."""

    elif "laptop was stolen" in issue_description.lower() and "business trip" in issue_description.lower():
        return """RESOLUTION STEPS TAKEN:
1. Addressed critical security incident for executive
2. Immediately initiated remote wipe procedures
3. Changed all executive passwords and credentials
4. Notified security team and senior management
5. Filed police report and insurance claim
6. Provided premium replacement laptop within 2 hours
7. Restored critical data from backups
8. Implemented enhanced security measures
9. Provided executive security briefing
10. Updated company security protocols

RESOLUTION: Critical security incident handled. All data remotely wiped, premium replacement provided, executive can continue working securely."""

    else:
        return """RESOLUTION STEPS TAKEN:
1. Analyzed reported issue and gathered details
2. Performed diagnostic checks on affected systems
3. Identified root cause of the problem
4. Implemented appropriate solution
5. Tested resolution to ensure functionality
6. Verified user access and system performance
7. Documented resolution steps for future reference
8. Updated relevant knowledge base articles
9. Notified user of successful resolution

RESOLUTION: Issue successfully resolved. All systems functioning normally."""

def get_priority(issue_description):
    """Determine priority based on issue description"""
    if any(keyword in issue_description.lower() for keyword in ["stolen", "burglary", "furious", "executive", "immediately"]):
        return "High"
    elif any(keyword in issue_description.lower() for keyword in ["bsod", "crashes", "unresponsive", "no internet"]):
        return "Medium"
    else:
        return "Low"

def get_assigned_agent(issue_description, priority):
    """Assign appropriate agent based on issue type and priority"""
    if priority == "High" or "stolen" in issue_description.lower():
        return "Azola Xabadiya"  # Senior agent for high priority/security issues
    elif "hardware" in issue_description.lower() or "laptop" in issue_description.lower():
        return "Keawin Koesnel"  # Hardware specialist
    else:
        return "Azola Xabadiya"  # Default assignment

def main():
    """Import Week 2 tickets with comprehensive notes"""
    print("📁 Importing Week 2: Software & Hardware Support Tickets")
    print("=======================================================")
    
    # Week 2 tickets from the file
    week2_tickets = [
        "User reports their laptop takes 15 minutes to boot and frequently freezes when multiple applications are open.",
        "User experiences a BSOD while connecting an external monitor through HDMI.",
        "Ethernet-connected desktop shows \"Unidentified Network\" and no internet access.",
        "Manager insists IT must provide a replacement laptop within hours after a burglary incident.",
        "Employee reports fan is always loud and system becomes slow after 30 minutes.",
        "User plugs in a USB device and laptop crashes instantly with BSOD.",
        "Employee reports Wi-Fi connects but no internet access is available.",
        "Remote worker calls upset because their laptop was stolen from a coffee shop, worried about personal and company files.",
        "User complains the laptop becomes unresponsive whenever multiple browser tabs are open.",
        "BSOD happens after Windows updates install and the system reboots.",
        "User reports network works fine on their phone but their laptop shows \"No Internet\" despite being connected.",
        "Executive calls furious because their laptop was stolen during a business trip and insists all data must be wiped remotely immediately."
    ]
    
    # Generate timestamps for the last 2 days
    base_time = datetime.now() - timedelta(days=2)
    
    imported_count = 0
    
    for i, issue in enumerate(week2_tickets):
        # Generate timestamp (spread over last 2 days)
        ticket_time = base_time + timedelta(hours=i*2, minutes=i*15)
        timestamp = ticket_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate user details
        user_names = ["Sarah Johnson", "Mike Chen", "Emily Rodriguez", "David Thompson", "Lisa Wang", 
                     "James Wilson", "Maria Garcia", "Robert Brown", "Jennifer Davis", "Christopher Lee",
                     "Amanda Taylor", "Michael Anderson"]
        
        user_emails = ["sarah.johnson@company.com", "mike.chen@company.com", "emily.rodriguez@company.com",
                      "david.thompson@company.com", "lisa.wang@company.com", "james.wilson@company.com",
                      "maria.garcia@company.com", "robert.brown@company.com", "jennifer.davis@company.com",
                      "christopher.lee@company.com", "amanda.taylor@company.com", "michael.anderson@company.com"]
        
        name = user_names[i]
        email = user_emails[i]
        
        # Determine priority and agent
        priority = get_priority(issue)
        assigned_agent = get_assigned_agent(issue, priority)
        
        # Generate comprehensive notes
        notes = get_comprehensive_notes(issue, priority)
        
        # Escape single quotes
        name_escaped = name.replace("'", "''")
        email_escaped = email.replace("'", "''")
        issue_escaped = issue.replace("'", "''")
        notes_escaped = notes.replace("'", "''")
        priority_escaped = priority.replace("'", "''")
        agent_escaped = assigned_agent.replace("'", "''")
        
        # Insert ticket
        insert_query = f'''
            USE DATABASE 'my-database';
            INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent, category)
            VALUES ('{timestamp}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '{notes_escaped}', 'Resolved', '{priority_escaped}', '{agent_escaped}', 'Week 2: Software & Hardware Support')
        '''
        
        result = execute_query(insert_query)
        if result:
            imported_count += 1
            print(f"✅ Imported Ticket #{i+1}: {name} - {issue[:50]}...")
        else:
            print(f"❌ Failed to import Ticket #{i+1}")
    
    print(f"\n🎉 Successfully imported {imported_count} Week 2 tickets!")
    
    # Verify import
    print("\n📊 Verifying import...")
    verify_query = '''
        USE DATABASE 'my-database';
        SELECT category, COUNT(*) as count 
        FROM tickets 
        GROUP BY category
        ORDER BY count DESC
    '''
    result = execute_query(verify_query)
    if result and 'data' in result:
        print("📁 Category Distribution:")
        for row in result['data']:
            print(f"   - {row['category']}: {row['count']} tickets")
    
    print("\n🎯 Week 2 tickets imported with:")
    print("   - Comprehensive resolution notes")
    print("   - Appropriate priority levels")
    print("   - Assigned agents")
    print("   - All marked as 'Resolved'")
    print("   - Proper timestamps over last 2 days")

if __name__ == "__main__":
    main()
