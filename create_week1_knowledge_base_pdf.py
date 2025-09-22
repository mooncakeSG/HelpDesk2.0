#!/usr/bin/env python3
"""
Create Week 1 Knowledge Base PDF from IT Helpdesk Comprehensive Log
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os

def create_week1_knowledge_base_pdf():
    """Create Week 1 Knowledge Base PDF file"""
    
    # Get current date for filename
    current_date = datetime.now().strftime("%Y%m%d")
    filename = f"Week1_Knowledge_Base_{current_date}.pdf"
    
    print(f"📚 Creating Week 1 Knowledge Base PDF: {filename}")
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2E8B57')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#2E8B57')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#4682B4')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20
    )
    
    # Build the story (content)
    story = []
    
    # Title page
    story.append(Paragraph("IT Helpdesk Knowledge Base", title_style))
    story.append(Paragraph("Week 1 Analysis & Procedures", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Paragraph("Based on Comprehensive Ticket Analysis", body_style))
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", heading_style))
    toc_items = [
        "1. Executive Summary",
        "2. Incident Patterns Analysis", 
        "3. Solution Playbook",
        "4. Agent Performance Analysis",
        "5. Common Issues & Solutions",
        "6. Escalation Procedures",
        "7. Week 1 Performance Summary",
        "8. Recommendations & Next Steps"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(Paragraph(
        "Week 1 of the IT Helpdesk operation demonstrated exceptional performance with a 100% resolution rate. "
        "All 13 tickets were resolved within the same business day, with no escalations required. "
        "The team successfully handled various incident types, with password-related issues being the most common. "
        "This knowledge base captures the patterns, procedures, and best practices established during the first week.",
        body_style
    ))
    
    story.append(Paragraph("Key Achievements:", subheading_style))
    achievements = [
        "100% ticket resolution rate achieved",
        "All tickets resolved same day",
        "Zero escalations required",
        "6 knowledge base articles created",
        "5 prevention strategies identified",
        "Perfect agent performance across all team members"
    ]
    
    for achievement in achievements:
        story.append(Paragraph(f"✓ {achievement}", bullet_style))
    
    story.append(PageBreak())
    
    # Incident Patterns Analysis
    story.append(Paragraph("2. Incident Patterns Analysis", heading_style))
    
    # Create incident patterns table
    incident_data = [
        ['Incident Type', 'Frequency', 'Priority', 'Resolution Time'],
        ['Password Reset Requests', '4 tickets', 'Medium', 'Same Day'],
        ['Account Lockouts', '3 tickets', 'Medium', 'Same Day'],
        ['Recurring Lockouts', '1 ticket', 'Medium', 'Same Day'],
        ['Account Disabled', '2 tickets', 'Medium', 'Same Day'],
        ['Outlook Authentication', '1 ticket', 'Low', 'Same Day'],
        ['MFA Device Issues', '1 ticket', 'High', 'Same Day'],
        ['Password Expiration', '1 ticket', 'Medium', 'Same Day'],
        ['Temporary Access', '1 ticket', 'Low', 'Same Day'],
        ['Security Incidents', '1 ticket', 'High', 'Same Day']
    ]
    
    incident_table = Table(incident_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
    incident_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E8B57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(incident_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Key Insights:", subheading_style))
    insights = [
        "Password-related issues account for 54% of all tickets (7 out of 13)",
        "Medium priority tickets are most common (77% of total)",
        "All incidents resolved within same business day",
        "No recurring issues or unresolved tickets",
        "Security incidents require immediate attention (High priority)"
    ]
    
    for insight in insights:
        story.append(Paragraph(f"• {insight}", bullet_style))
    
    story.append(PageBreak())
    
    # Solution Playbook
    story.append(Paragraph("3. Solution Playbook", heading_style))
    story.append(Paragraph(
        "Standardized procedures for resolving common IT helpdesk issues. "
        "Each procedure follows a 5-step process to ensure consistent and effective resolution.",
        body_style
    ))
    
    # Password Reset Procedure
    story.append(Paragraph("3.1 Password Reset Procedure", subheading_style))
    password_steps = [
        "Verify user identity through company app/phone system",
        "Access Active Directory Users and Computers (ADUC)",
        "Locate user account: @username",
        "Reset password using 'Reset Password' function",
        "Set temporary password with complexity requirements"
    ]
    
    for i, step in enumerate(password_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))
    
    story.append(Paragraph("KB Article: KB_Password_Reset", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Account Unlock Procedure
    story.append(Paragraph("3.2 Account Unlock Procedure", subheading_style))
    unlock_steps = [
        "Check Active Directory for account lockout status",
        "Verify lockout was due to failed login attempts",
        "Use ADUC to unlock user account",
        "Reset failed login counter to zero",
        "Verify account is now accessible"
    ]
    
    for i, step in enumerate(unlock_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))
    
    story.append(Paragraph("KB Article: KB_Password_Reset", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Recurring Lockout Procedure
    story.append(Paragraph("3.3 Recurring Lockout Resolution", subheading_style))
    recurring_steps = [
        "Analyze lockout source using LockoutStatus.exe tool",
        "Identify multiple lockout sources across domain controllers",
        "Check for cached credentials on user devices",
        "Clear all cached credentials from devices",
        "Reset user password to clear cached bad passwords"
    ]
    
    for i, step in enumerate(recurring_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))
    
    story.append(Paragraph("KB Article: KB_Password_Reset", body_style))
    story.append(PageBreak())
    
    # Agent Performance Analysis
    story.append(Paragraph("4. Agent Performance Analysis", heading_style))
    
    # Agent performance table
    agent_data = [
        ['Agent Name', 'Total Tickets', 'High Priority', 'Medium Priority', 'Low Priority', 'Resolution Rate'],
        ['Azola Xabadiya', '4 tickets', '1', '3', '0', '100%'],
        ['Keawin Koesnel', '6 tickets', '1', '4', '1', '100%'],
        ['System Admin', '3 tickets', '0', '3', '0', '100%']
    ]
    
    agent_table = Table(agent_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    agent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E8B57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(agent_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Performance Highlights:", subheading_style))
    highlights = [
        "All agents achieved 100% resolution rate",
        "Keawin Koesnel handled the most tickets (6)",
        "Azola Xabadiya and Keawin Koesnel handled high-priority security incidents",
        "System Admin focused on standard password and account issues",
        "No performance issues or training needs identified"
    ]
    
    for highlight in highlights:
        story.append(Paragraph(f"• {highlight}", bullet_style))
    
    story.append(PageBreak())
    
    # Common Issues & Solutions
    story.append(Paragraph("5. Common Issues & Solutions", heading_style))
    
    issues = [
        {
            "issue": "User forgot password",
            "symptoms": "Cannot log in, password not working",
            "solution": "Reset password via ADUC, provide temporary password",
            "prevention": "Send password expiration reminders"
        },
        {
            "issue": "Account locked after failed attempts",
            "symptoms": "Account locked message, cannot access systems",
            "solution": "Unlock account in ADUC, reset failed login counter",
            "prevention": "Educate users on correct password entry"
        },
        {
            "issue": "Recurring account lockouts",
            "symptoms": "Account locks repeatedly even with correct password",
            "solution": "Clear cached credentials from all devices",
            "prevention": "Regular credential cache maintenance"
        },
        {
            "issue": "Account disabled unexpectedly",
            "symptoms": "Login denied, account may be disabled",
            "solution": "Re-enable account if authorized, document reason",
            "prevention": "Review account disablement policies"
        },
        {
            "issue": "Outlook authentication prompts",
            "symptoms": "Outlook keeps asking for password",
            "solution": "Clear credential cache, reset Office 365 password",
            "prevention": "Regular Office 365 credential refresh"
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        story.append(Paragraph(f"5.{i} {issue['issue']}", subheading_style))
        story.append(Paragraph(f"<b>Symptoms:</b> {issue['symptoms']}", body_style))
        story.append(Paragraph(f"<b>Solution:</b> {issue['solution']}", body_style))
        story.append(Paragraph(f"<b>Prevention:</b> {issue['prevention']}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # Escalation Procedures
    story.append(Paragraph("6. Escalation Procedures", heading_style))
    story.append(Paragraph(
        "Guidelines for when and how to escalate issues beyond the helpdesk team. "
        "Proper escalation ensures timely resolution of complex or high-impact incidents.",
        body_style
    ))
    
    escalation_data = [
        ['Issue Type', 'When to Escalate', 'Level 1', 'Level 2'],
        ['High Priority Security', 'Immediate', 'IT Security Team', 'CISO'],
        ['Recurring Lockouts', 'After 2 failed attempts', 'Senior IT Support', 'IT Director'],
        ['Multiple User Issues', 'More than 5 users affected', 'IT Manager', 'IT Director'],
        ['System-wide Problems', 'Authentication system down', 'System Administrator', 'IT Director'],
        ['Access Violations', 'Unauthorized access attempts', 'IT Security Team', 'CISO']
    ]
    
    escalation_table = Table(escalation_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch])
    escalation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E8B57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(escalation_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Documentation Required for Escalation:", subheading_style))
    doc_requirements = [
        "Security incident report and log files",
        "Resolution attempts and user impact assessment",
        "User list and affected systems",
        "System status and error logs",
        "Access logs and authorization documents"
    ]
    
    for req in doc_requirements:
        story.append(Paragraph(f"• {req}", bullet_style))
    
    story.append(PageBreak())
    
    # Week 1 Performance Summary
    story.append(Paragraph("7. Week 1 Performance Summary", heading_style))
    
    summary_data = [
        ['Metric', 'Value', 'Notes'],
        ['Total Tickets Handled', '13 tickets', 'All tickets from Week 1 successfully processed'],
        ['Tickets Resolved', '13 tickets', 'No outstanding or unresolved tickets'],
        ['Resolution Rate', '100%', 'Perfect resolution rate achieved'],
        ['Average Resolution Time', 'Same Day', 'All tickets resolved within same business day'],
        ['Most Common Issue Type', 'Password Reset (4 tickets)', 'Password-related issues most frequent'],
        ['Highest Priority Issues', '2 High Priority tickets', 'MFA device lost and security incidents'],
        ['Agent Performance Rating', 'Excellent (100% resolution rate)', 'All agents performed exceptionally well'],
        ['User Satisfaction', 'High', 'Users received prompt and effective support'],
        ['Knowledge Base Articles', '6 KB articles', 'Comprehensive knowledge base established'],
        ['Process Improvements', '5 prevention strategies', 'Proactive measures identified for common issues']
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E8B57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Key Success Factors:", subheading_style))
    success_factors = [
        "Standardized procedures for common issues",
        "Quick response time and same-day resolution",
        "Comprehensive documentation and knowledge sharing",
        "Effective agent training and performance",
        "Proactive identification of prevention strategies"
    ]
    
    for factor in success_factors:
        story.append(Paragraph(f"• {factor}", bullet_style))
    
    story.append(PageBreak())
    
    # Recommendations & Next Steps
    story.append(Paragraph("8. Recommendations & Next Steps", heading_style))
    
    story.append(Paragraph("8.1 Immediate Actions (Week 2)", subheading_style))
    immediate_actions = [
        "Implement password expiration reminder system",
        "Create user education materials for password management",
        "Set up automated credential cache cleanup schedule",
        "Review and update account disablement policies",
        "Establish regular Office 365 credential refresh procedures"
    ]
    
    for action in immediate_actions:
        story.append(Paragraph(f"• {action}", bullet_style))
    
    story.append(Paragraph("8.2 Medium-term Improvements (Month 1)", subheading_style))
    medium_term = [
        "Develop self-service password reset portal",
        "Implement automated account lockout monitoring",
        "Create user training program for common issues",
        "Establish regular knowledge base review process",
        "Set up performance metrics dashboard"
    ]
    
    for improvement in medium_term:
        story.append(Paragraph(f"• {improvement}", bullet_style))
    
    story.append(Paragraph("8.3 Long-term Strategic Goals (Quarter 1)", subheading_style))
    long_term = [
        "Reduce ticket volume through prevention strategies",
        "Implement advanced security monitoring and alerting",
        "Develop predictive analytics for common issues",
        "Create comprehensive user self-service portal",
        "Establish IT service management best practices"
    ]
    
    for goal in long_term:
        story.append(Paragraph(f"• {goal}", bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("--- End of Week 1 Knowledge Base ---", body_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ Week 1 Knowledge Base PDF created successfully: {filename}")
    return filename

def main():
    print("📚 Week 1 Knowledge Base PDF Creator")
    print("====================================")
    print()
    
    # Create PDF file
    filename = create_week1_knowledge_base_pdf()
    
    print()
    print("📈 PDF Knowledge Base Summary:")
    print(f"   📄 File created: {filename}")
    print(f"   📊 Pages: 8 comprehensive sections")
    print(f"   🎨 Formatting: Professional styling with color-coded sections")
    
    print()
    print("✅ Week 1 Knowledge Base PDF created successfully!")
    print(f"📁 File location: {os.path.abspath(filename)}")
    print()
    print("📋 The PDF Knowledge Base includes:")
    print("   • Executive Summary with key achievements")
    print("   • Incident Patterns Analysis with frequency data")
    print("   • Solution Playbook with step-by-step procedures")
    print("   • Agent Performance Analysis with metrics")
    print("   • Common Issues & Solutions with prevention tips")
    print("   • Escalation Procedures with contact information")
    print("   • Week 1 Performance Summary with detailed metrics")
    print("   • Recommendations & Next Steps for continuous improvement")
    print()
    print("🎯 Key Features:")
    print("   • Professional formatting with color-coded headers")
    print("   • Comprehensive tables with data visualization")
    print("   • Step-by-step procedures for common issues")
    print("   • Performance metrics and analysis")
    print("   • Strategic recommendations for improvement")

if __name__ == "__main__":
    main()
