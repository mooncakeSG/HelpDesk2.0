#!/usr/bin/env python3
"""
Fix email configuration to send to the same Gmail address for testing
"""

import os

def fix_email_config():
    """Update .env file to send emails to the same Gmail address"""
    
    print("🔧 Fixing Email Configuration")
    print("=" * 40)
    
    # Read current .env file
    env_file = '.env'
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return
    
    # Read current content
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update NOTIFY_EMAILS to use the same Gmail address
    updated_lines = []
    for line in lines:
        if line.startswith('NOTIFY_EMAILS='):
            updated_lines.append('NOTIFY_EMAILS=keawinkoesnel804@gmail.com\n')
            print("✅ Updated NOTIFY_EMAILS to use same Gmail address")
        else:
            updated_lines.append(line)
    
    # Write updated content
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ Configuration updated!")
    print("📧 Emails will now be sent to: keawinkoesnel804@gmail.com")
    print()
    print("🔄 Please restart the email server:")
    print("   1. Stop the current server (Ctrl+C)")
    print("   2. Run: python email_notifications.py")
    print("   3. Test with: python test_same_email.py")

if __name__ == "__main__":
    fix_email_config()
