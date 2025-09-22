#!/usr/bin/env python3
"""
Render Deployment Helper Script
This script helps prepare your IT Helpdesk application for Render deployment
"""

import os
import json
from datetime import datetime

def create_render_config():
    """Create render.yaml configuration file"""
    
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "it-helpdesk-main",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python app.py",
                "envVars": [
                    {
                        "key": "FLASK_ENV",
                        "value": "production"
                    },
                    {
                        "key": "FLASK_DEBUG",
                        "value": "False"
                    }
                ]
            },
            {
                "type": "web",
                "name": "it-helpdesk-email",
                "env": "python",
                "buildCommand": "pip install -r email_requirements.txt",
                "startCommand": "python email_notifications.py",
                "envVars": [
                    {
                        "key": "FLASK_ENV",
                        "value": "production"
                    },
                    {
                        "key": "FLASK_DEBUG",
                        "value": "False"
                    }
                ]
            }
        ]
    }
    
    with open('render.yaml', 'w') as f:
        import yaml
        yaml.dump(render_config, f, default_flow_style=False)
    
    print("✅ Created render.yaml configuration file")

def check_required_files():
    """Check if all required files exist"""
    
    required_files = [
        'app.py',
        'email_notifications.py',
        'requirements.txt',
        'email_requirements.txt',
        'templates/index.html',
        'templates/ticket_form.html',
        'templates/agent_page.html',
        'static/style.css'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_requirements():
    """Check requirements.txt files"""
    
    # Check main requirements
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        required_packages = [
            'Flask==2.3.3',
            'requests==2.31.0',
            'python-dotenv==1.0.0',
            'reportlab==4.0.4',
            'pandas==2.1.1',
            'openpyxl==3.1.2'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print("❌ Missing packages in requirements.txt:")
            for package in missing_packages:
                print(f"   - {package}")
        else:
            print("✅ requirements.txt is complete")
    
    # Check email requirements
    if os.path.exists('email_requirements.txt'):
        with open('email_requirements.txt', 'r') as f:
            email_requirements = f.read()
        
        required_email_packages = [
            'Flask==2.3.3',
            'Flask-Mail==0.9.1',
            'python-dotenv==1.0.0'
        ]
        
        missing_email_packages = []
        for package in required_email_packages:
            if package not in email_requirements:
                missing_email_packages.append(package)
        
        if missing_email_packages:
            print("❌ Missing packages in email_requirements.txt:")
            for package in missing_email_packages:
                print(f"   - {package}")
        else:
            print("✅ email_requirements.txt is complete")

def create_env_template():
    """Create environment variables template"""
    
    env_template = """# Render Environment Variables Template
# Copy these to your Render dashboard environment variables

# Main Application Environment Variables
SQLITECLOUD_API_KEY=your_sqlitecloud_api_key_here
SQLITECLOUD_URL=https://your-database.g5.sqlite.cloud:443/v2/weblite/sql
FLASK_ENV=production
FLASK_DEBUG=False

# Email Service Environment Variables
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your_16_character_app_password
MAIL_DEFAULT_SENDER=IT Helpdesk <your.email@gmail.com>
NOTIFY_EMAILS=teammate1@gmail.com,teammate2@gmail.com,teammate3@gmail.com
"""
    
    with open('render_env_template.txt', 'w') as f:
        f.write(env_template)
    
    print("✅ Created render_env_template.txt")

def create_deployment_checklist():
    """Create deployment checklist"""
    
    checklist = """# Render Deployment Checklist

## Pre-Deployment
- [ ] All code committed to GitHub
- [ ] Environment variables prepared
- [ ] Database connection tested
- [ ] Email service tested locally
- [ ] Requirements.txt files updated

## Render Setup
- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Main web service created
- [ ] Email web service created
- [ ] Environment variables configured

## Testing
- [ ] Main application accessible
- [ ] Database connection working
- [ ] Email notifications sending
- [ ] Agent page functional
- [ ] Ticket submission working

## Post-Deployment
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Backup procedures established
- [ ] Team access configured
"""
    
    with open('DEPLOYMENT_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("✅ Created DEPLOYMENT_CHECKLIST.md")

def main():
    """Main deployment preparation function"""
    
    print("🚀 Render Deployment Preparation")
    print("=" * 40)
    print()
    
    # Check required files
    print("📁 Checking required files...")
    files_ok = check_required_files()
    print()
    
    # Check requirements
    print("📦 Checking requirements files...")
    check_requirements()
    print()
    
    # Create configuration files
    print("⚙️ Creating configuration files...")
    try:
        create_render_config()
    except ImportError:
        print("⚠️ PyYAML not installed. Install with: pip install PyYAML")
        print("   Or create render.yaml manually using the deployment guide")
    
    create_env_template()
    create_deployment_checklist()
    print()
    
    # Summary
    print("📋 Deployment Preparation Summary:")
    print("=" * 35)
    
    if files_ok:
        print("✅ Ready for deployment!")
        print()
        print("Next steps:")
        print("1. Review RENDER_DEPLOYMENT_GUIDE.md")
        print("2. Set up environment variables in Render dashboard")
        print("3. Deploy main application")
        print("4. Deploy email service")
        print("5. Test deployment")
    else:
        print("❌ Please fix missing files before deployment")
    
    print()
    print("📚 For detailed instructions, see RENDER_DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
