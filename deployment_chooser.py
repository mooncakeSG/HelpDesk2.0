#!/usr/bin/env python3
"""
IT Helpdesk Deployment Option Chooser
Helps you select the best deployment option based on your requirements
"""

def deployment_chooser():
    """Interactive deployment option chooser"""
    
    print("🚀 IT Helpdesk Deployment Option Chooser")
    print("=" * 50)
    print()
    
    # Get user requirements
    print("📋 Let's find the best deployment option for you!")
    print()
    
    # Team size
    print("1. How many people will use the system?")
    print("   a) 1-5 people (small team)")
    print("   b) 5-20 people (medium team)")
    print("   c) 20-100 people (large team)")
    print("   d) 100+ people (enterprise)")
    
    team_size = input("   Enter your choice (a/b/c/d): ").lower()
    
    # Budget
    print("\n2. What's your monthly budget?")
    print("   a) $0-10 (free/low cost)")
    print("   b) $10-50 (moderate)")
    print("   c) $50-200 (generous)")
    print("   d) $200+ (enterprise)")
    
    budget = input("   Enter your choice (a/b/c/d): ").lower()
    
    # Technical expertise
    print("\n3. What's your technical expertise level?")
    print("   a) Beginner (prefer easy setup)")
    print("   b) Intermediate (comfortable with some configuration)")
    print("   c) Advanced (can handle complex setups)")
    print("   d) Expert (want full control)")
    
    expertise = input("   Enter your choice (a/b/c/d): ").lower()
    
    # Deployment timeline
    print("\n4. When do you need it deployed?")
    print("   a) Today (urgent)")
    print("   b) This week")
    print("   c) This month")
    print("   d) No rush")
    
    timeline = input("   Enter your choice (a/b/c/d): ").lower()
    
    # Calculate recommendation
    recommendation = calculate_recommendation(team_size, budget, expertise, timeline)
    
    print("\n" + "=" * 50)
    print("🎯 RECOMMENDED DEPLOYMENT OPTION")
    print("=" * 50)
    print()
    
    if recommendation == "heroku":
        print_heroku_recommendation()
    elif recommendation == "railway":
        print_railway_recommendation()
    elif recommendation == "render":
        print_render_recommendation()
    elif recommendation == "digitalocean":
        print_digitalocean_recommendation()
    elif recommendation == "docker":
        print_docker_recommendation()
    elif recommendation == "ubuntu":
        print_ubuntu_recommendation()
    elif recommendation == "aws":
        print_aws_recommendation()
    
    print("\n" + "=" * 50)
    print("📚 ALTERNATIVE OPTIONS")
    print("=" * 50)
    print()
    
    print_alternative_options(recommendation)
    
    print("\n" + "=" * 50)
    print("🚀 NEXT STEPS")
    print("=" * 50)
    print()
    
    print_next_steps(recommendation)

def calculate_recommendation(team_size, budget, expertise, timeline):
    """Calculate the best deployment option based on user inputs"""
    
    # Scoring system
    scores = {
        "heroku": 0,
        "railway": 0,
        "render": 0,
        "digitalocean": 0,
        "docker": 0,
        "ubuntu": 0,
        "aws": 0
    }
    
    # Team size scoring
    if team_size == "a":  # Small team
        scores["heroku"] += 3
        scores["railway"] += 3
        scores["render"] += 2
        scores["digitalocean"] += 1
    elif team_size == "b":  # Medium team
        scores["heroku"] += 2
        scores["railway"] += 2
        scores["render"] += 2
        scores["digitalocean"] += 3
        scores["docker"] += 2
    elif team_size == "c":  # Large team
        scores["digitalocean"] += 3
        scores["docker"] += 3
        scores["ubuntu"] += 2
        scores["aws"] += 2
    else:  # Enterprise
        scores["aws"] += 3
        scores["ubuntu"] += 3
        scores["docker"] += 2
    
    # Budget scoring
    if budget == "a":  # Free/low cost
        scores["render"] += 3
        scores["railway"] += 2
        scores["heroku"] += 1
    elif budget == "b":  # Moderate
        scores["heroku"] += 3
        scores["railway"] += 3
        scores["digitalocean"] += 2
    elif budget == "c":  # Generous
        scores["digitalocean"] += 3
        scores["docker"] += 2
        scores["aws"] += 2
    else:  # Enterprise
        scores["aws"] += 3
        scores["ubuntu"] += 2
    
    # Expertise scoring
    if expertise == "a":  # Beginner
        scores["heroku"] += 3
        scores["railway"] += 3
        scores["render"] += 3
    elif expertise == "b":  # Intermediate
        scores["heroku"] += 2
        scores["railway"] += 2
        scores["digitalocean"] += 3
        scores["docker"] += 2
    elif expertise == "c":  # Advanced
        scores["digitalocean"] += 2
        scores["docker"] += 3
        scores["ubuntu"] += 2
    else:  # Expert
        scores["ubuntu"] += 3
        scores["aws"] += 3
        scores["docker"] += 2
    
    # Timeline scoring
    if timeline == "a":  # Urgent
        scores["heroku"] += 3
        scores["railway"] += 3
        scores["render"] += 2
    elif timeline == "b":  # This week
        scores["heroku"] += 2
        scores["railway"] += 2
        scores["digitalocean"] += 2
        scores["docker"] += 2
    elif timeline == "c":  # This month
        scores["digitalocean"] += 2
        scores["docker"] += 2
        scores["ubuntu"] += 2
    else:  # No rush
        scores["ubuntu"] += 3
        scores["aws"] += 2
    
    # Return the option with the highest score
    return max(scores, key=scores.get)

def print_heroku_recommendation():
    """Print Heroku recommendation details"""
    print("🏆 HEROKU")
    print("   Best for: Small to medium teams, quick deployment")
    print("   Cost: $7-25/month")
    print("   Setup time: 10 minutes")
    print("   Difficulty: Easy")
    print()
    print("✅ Pros:")
    print("   • Very easy to deploy")
    print("   • Automatic scaling")
    print("   • Built-in monitoring")
    print("   • Great documentation")
    print()
    print("❌ Cons:")
    print("   • Can be expensive for high traffic")
    print("   • Limited customization")
    print("   • Sleeps on free tier")
    print()
    print("🚀 Quick start:")
    print("   ./deploy_heroku.sh")

def print_railway_recommendation():
    """Print Railway recommendation details"""
    print("🏆 RAILWAY")
    print("   Best for: Modern teams, good developer experience")
    print("   Cost: $5-20/month")
    print("   Setup time: 5 minutes")
    print("   Difficulty: Easy")
    print()
    print("✅ Pros:")
    print("   • Modern platform")
    print("   • Great developer experience")
    print("   • Automatic deployments")
    print("   • Good pricing")
    print()
    print("❌ Cons:")
    print("   • Newer platform")
    print("   • Less mature than Heroku")
    print()
    print("🚀 Quick start:")
    print("   railway login && railway deploy")

def print_render_recommendation():
    """Print Render recommendation details"""
    print("🏆 RENDER")
    print("   Best for: Budget-conscious teams, free tier available")
    print("   Cost: $7-25/month (free tier available)")
    print("   Setup time: 10 minutes")
    print("   Difficulty: Easy")
    print()
    print("✅ Pros:")
    print("   • Free tier available")
    print("   • Good performance")
    print("   • Easy setup")
    print("   • Automatic SSL")
    print()
    print("❌ Cons:")
    print("   • Less features than Heroku")
    print("   • Smaller community")
    print()
    print("🚀 Quick start:")
    print("   Connect GitHub repository to Render")

def print_digitalocean_recommendation():
    """Print DigitalOcean recommendation details"""
    print("🏆 DIGITALOCEAN APP PLATFORM")
    print("   Best for: Growing teams, good balance of features and cost")
    print("   Cost: $12-40/month")
    print("   Setup time: 30 minutes")
    print("   Difficulty: Intermediate")
    print()
    print("✅ Pros:")
    print("   • Good performance")
    print("   • Reasonable pricing")
    print("   • Full control")
    print("   • Good documentation")
    print()
    print("❌ Cons:")
    print("   • More complex than Heroku")
    print("   • Requires more configuration")
    print()
    print("🚀 Quick start:")
    print("   Create app in DigitalOcean dashboard")

def print_docker_recommendation():
    """Print Docker recommendation details"""
    print("🏆 DOCKER")
    print("   Best for: Teams wanting containerization, consistent environments")
    print("   Cost: $10-50/month (depending on hosting)")
    print("   Setup time: 45 minutes")
    print("   Difficulty: Intermediate")
    print()
    print("✅ Pros:")
    print("   • Consistent environments")
    print("   • Easy to scale")
    print("   • Portable")
    print("   • Good for CI/CD")
    print()
    print("❌ Cons:")
    print("   • Requires Docker knowledge")
    print("   • More complex setup")
    print()
    print("🚀 Quick start:")
    print("   ./deploy_docker.sh")

def print_ubuntu_recommendation():
    """Print Ubuntu VPS recommendation details"""
    print("🏆 UBUNTU VPS")
    print("   Best for: Full control, cost-effective, technical teams")
    print("   Cost: $5-20/month")
    print("   Setup time: 2 hours")
    print("   Difficulty: Advanced")
    print()
    print("✅ Pros:")
    print("   • Full control")
    print("   • Very cost-effective")
    print("   • Customizable")
    print("   • Learn server management")
    print()
    print("❌ Cons:")
    print("   • Requires server management")
    print("   • More maintenance")
    print("   • Security responsibility")
    print()
    print("🚀 Quick start:")
    print("   ./deploy_ubuntu.sh")

def print_aws_recommendation():
    """Print AWS recommendation details"""
    print("🏆 AWS")
    print("   Best for: Enterprise, high availability, complex requirements")
    print("   Cost: $50-500/month")
    print("   Setup time: 4 hours")
    print("   Difficulty: Expert")
    print()
    print("✅ Pros:")
    print("   • Enterprise features")
    print("   • High availability")
    print("   • Scalable")
    print("   • Many services")
    print()
    print("❌ Cons:")
    print("   • Complex")
    print("   • Expensive")
    print("   • Steep learning curve")
    print()
    print("🚀 Quick start:")
    print("   Use AWS Elastic Beanstalk or ECS")

def print_alternative_options(recommendation):
    """Print alternative options based on the recommendation"""
    
    alternatives = {
        "heroku": ["Railway", "Render", "DigitalOcean"],
        "railway": ["Heroku", "Render", "DigitalOcean"],
        "render": ["Heroku", "Railway", "DigitalOcean"],
        "digitalocean": ["Heroku", "Railway", "Docker"],
        "docker": ["DigitalOcean", "Ubuntu VPS", "AWS"],
        "ubuntu": ["Docker", "AWS", "DigitalOcean"],
        "aws": ["Ubuntu VPS", "Docker", "DigitalOcean"]
    }
    
    print("If the recommended option doesn't work for you, consider:")
    for alt in alternatives.get(recommendation, []):
        print(f"   • {alt}")

def print_next_steps(recommendation):
    """Print next steps based on the recommendation"""
    
    print("1. 📖 Read the deployment guide:")
    print("   cat DEPLOYMENT_GUIDE.md")
    print()
    
    if recommendation in ["heroku", "docker", "ubuntu"]:
        print("2. 🚀 Run the deployment script:")
        if recommendation == "heroku":
            print("   chmod +x deploy_heroku.sh && ./deploy_heroku.sh")
        elif recommendation == "docker":
            print("   chmod +x deploy_docker.sh && ./deploy_docker.sh")
        elif recommendation == "ubuntu":
            print("   chmod +x deploy_ubuntu.sh && sudo ./deploy_ubuntu.sh")
    else:
        print("2. 🚀 Follow the platform-specific instructions in DEPLOYMENT_GUIDE.md")
    
    print()
    print("3. ⚙️  Configure your environment variables:")
    print("   • SQLiteCloud API credentials")
    print("   • Gmail App Password")
    print("   • Team notification emails")
    print()
    print("4. 🧪 Test your deployment:")
    print("   • Submit a test ticket")
    print("   • Verify email notifications")
    print("   • Check agent portal functionality")
    print()
    print("5. 📚 Set up monitoring and backups")
    print("6. 🔒 Configure SSL/HTTPS")
    print("7. 📢 Notify your team of the new system!")

if __name__ == "__main__":
    deployment_chooser()
