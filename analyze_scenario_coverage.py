#!/usr/bin/env python3
"""
Analyze ticket coverage for specific IT helpdesk scenarios
"""

def analyze_scenario_coverage():
    """Analyze if tickets cover the requested scenarios"""
    
    print("🔍 Analyzing Ticket Coverage for Specific Scenarios")
    print("=" * 60)
    print()
    
    # Define the scenarios to check
    scenarios = {
        "AD Password Reset (Laptop)": {
            "description": "User needs password reset for laptop/computer login",
            "keywords": ["password reset", "forgot password", "laptop", "computer login"],
            "covered": False,
            "tickets": []
        },
        "Account lock (Once-off)": {
            "description": "Single account lockout due to failed login attempts",
            "keywords": ["account locked", "failed login", "unlock", "once-off"],
            "covered": False,
            "tickets": []
        },
        "Account lock (Persistent) Irrate user": {
            "description": "Recurring account lockouts causing user frustration",
            "keywords": ["recurring lockout", "persistent", "multiple systems", "frustrated"],
            "covered": False,
            "tickets": []
        },
        "Account Re-enable": {
            "description": "Account disabled and needs to be re-enabled",
            "keywords": ["account disabled", "re-enable", "disabled account"],
            "covered": False,
            "tickets": []
        }
    }
    
    # Ticket data from the comprehensive log
    tickets = [
        {
            "id": 9,
            "summary": "Hi, I am locked out because I have forgotten my password. I have already verified my identity using our company app/phone system and my username is @lindokuhle. Could you initiate a password reset for me?",
            "category": "Password Reset"
        },
        {
            "id": 10,
            "summary": "Hello, I believe my AD account is locked after a few failed login attempts. I am confident I know the correct password now. My username is @lindokuhle; could you check its status and unlock it?",
            "category": "Account Unlock"
        },
        {
            "id": 11,
            "summary": "Hi, I need help with a recurring account lockout. My account gets locked even when I enter the correct password, and it seems to be happening across different systems. Could you please investigate the source of the lockout using the lockout tool and clear it from all points?",
            "category": "Recurring Lockout"
        },
        {
            "id": 12,
            "summary": "Hello, I am unable to log in and I have confirmed my password is correct. Could you check if my account (@lindokuhle) has been disabled? If it is, could you please outline the re-enablement process so I can get the necessary approval from my manager started?",
            "category": "Account Re-enable"
        },
        {
            "id": 13,
            "summary": "Hi, I can successfully log into my laptop itself, but I keep getting authentication prompts when I try to open Outlook. It won't accept my password, which I am certain is correct. This suggests a sync issue or a problem with my cached credentials for this specific service. Please advise.",
            "category": "Outlook Authentication"
        },
        {
            "id": 17,
            "summary": "Account locked after repeated login attempts on work PC.",
            "category": "Account Unlock"
        },
        {
            "id": 18,
            "summary": "User cannot recall password after holiday, needs reset.",
            "category": "Password Reset"
        },
        {
            "id": 19,
            "summary": "User lost phone used for MFA, cannot log in to Outlook.",
            "category": "MFA Reset"
        },
        {
            "id": 20,
            "summary": "User reports they cannot log in, AD shows account disabled.",
            "category": "Account Re-enable"
        },
        {
            "id": 21,
            "summary": "User password expired and cannot update remotely.",
            "category": "Password Reset"
        },
        {
            "id": 22,
            "summary": "User phone keeps retrying old password, causing lockout.",
            "category": "Account Unlock"
        },
        {
            "id": 23,
            "summary": "Contractor requires temporary AD account with limited permissions.",
            "category": "Temporary Account"
        },
        {
            "id": 24,
            "summary": "User notified of failed login attempts from unknown location.",
            "category": "Security Incident"
        }
    ]
    
    # Analyze coverage for each scenario
    for scenario_name, scenario_info in scenarios.items():
        print(f"📋 {scenario_name}")
        print(f"   Description: {scenario_info['description']}")
        print(f"   Keywords: {', '.join(scenario_info['keywords'])}")
        
        # Check each ticket for coverage
        for ticket in tickets:
            summary_lower = ticket['summary'].lower()
            category_lower = ticket['category'].lower()
            
            # Check if any keywords match
            for keyword in scenario_info['keywords']:
                if keyword.lower() in summary_lower or keyword.lower() in category_lower:
                    scenario_info['covered'] = True
                    scenario_info['tickets'].append({
                        'id': ticket['id'],
                        'summary': ticket['summary'][:100] + "..." if len(ticket['summary']) > 100 else ticket['summary'],
                        'category': ticket['category']
                    })
                    break
        
        # Display results
        if scenario_info['covered']:
            print(f"   ✅ COVERED - Found {len(scenario_info['tickets'])} ticket(s)")
            for ticket in scenario_info['tickets']:
                print(f"      • Ticket #{ticket['id']}: {ticket['category']}")
                print(f"        {ticket['summary']}")
        else:
            print(f"   ❌ NOT COVERED - No matching tickets found")
        
        print()
    
    # Summary
    print("📊 COVERAGE SUMMARY")
    print("=" * 30)
    
    covered_count = sum(1 for scenario in scenarios.values() if scenario['covered'])
    total_scenarios = len(scenarios)
    
    print(f"Scenarios Covered: {covered_count}/{total_scenarios}")
    print(f"Coverage Rate: {(covered_count/total_scenarios)*100:.1f}%")
    print()
    
    print("✅ COVERED SCENARIOS:")
    for scenario_name, scenario_info in scenarios.items():
        if scenario_info['covered']:
            print(f"   • {scenario_name} ({len(scenario_info['tickets'])} ticket(s))")
    
    print()
    print("❌ MISSING SCENARIOS:")
    for scenario_name, scenario_info in scenarios.items():
        if not scenario_info['covered']:
            print(f"   • {scenario_name}")
    
    print()
    print("🎯 RECOMMENDATIONS:")
    if covered_count == total_scenarios:
        print("   • All requested scenarios are covered!")
        print("   • Knowledge base is comprehensive for these use cases")
        print("   • Consider adding more edge cases for complete coverage")
    else:
        print("   • Add tickets for missing scenarios to improve coverage")
        print("   • Consider creating test scenarios for uncovered cases")
        print("   • Review existing tickets to see if they can be categorized differently")
    
    return scenarios

def main():
    print("🔍 IT Helpdesk Scenario Coverage Analysis")
    print("=" * 50)
    print()
    
    scenarios = analyze_scenario_coverage()
    
    print()
    print("📋 DETAILED TICKET BREAKDOWN:")
    print("=" * 35)
    
    # Group tickets by category
    categories = {}
    for scenario_name, scenario_info in scenarios.items():
        if scenario_info['covered']:
            for ticket in scenario_info['tickets']:
                category = ticket['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(ticket)
    
    for category, tickets in categories.items():
        print(f"\n📁 {category} ({len(tickets)} ticket(s)):")
        for ticket in tickets:
            print(f"   • Ticket #{ticket['id']}: {ticket['summary']}")

if __name__ == "__main__":
    main()
