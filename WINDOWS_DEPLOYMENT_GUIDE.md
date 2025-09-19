# 🪟 Windows VPS Deployment Guide - IT Helpdesk System

## 📋 **Overview**
This guide covers deploying the IT Helpdesk system on Windows Server or Windows 10/11 VPS, providing full control and enterprise-grade features.

## 🎯 **Why Choose Windows VPS?**

### **Advantages:**
- ✅ **Familiar Environment**: Windows Server management
- ✅ **Active Directory Integration**: Enterprise authentication
- ✅ **PowerShell Management**: Advanced automation
- ✅ **Windows Services**: Native service management
- ✅ **IIS Integration**: Web server options
- ✅ **Enterprise Tools**: Monitoring and management
- ✅ **RDP Access**: Remote desktop management

### **Best For:**
- Windows-centric organizations
- Teams familiar with Windows Server
- Enterprise environments
- Active Directory integration needs
- PowerShell automation requirements

## 🖥️ **System Requirements**

### **Minimum Requirements:**
- **OS**: Windows Server 2016+ or Windows 10/11
- **RAM**: 4GB (8GB recommended)
- **Storage**: 20GB free space
- **CPU**: 2 cores (4 cores recommended)
- **Network**: Stable internet connection

### **Recommended VPS Providers:**
- **DigitalOcean**: $12-24/month
- **Vultr**: $10-20/month
- **Linode**: $12-24/month
- **AWS EC2**: $15-40/month
- **Azure**: $20-50/month

## 🚀 **Quick Deployment**

### **Automated Deployment (Recommended)**
```powershell
# Download and run the deployment script
Invoke-WebRequest -Uri "https://your-repo.com/deploy_windows.ps1" -OutFile "deploy_windows.ps1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy_windows.ps1
```

### **Manual Deployment Steps**
1. **Prepare Windows VPS**
2. **Install Dependencies**
3. **Configure Services**
4. **Set up Nginx**
5. **Configure Firewall**
6. **Test Deployment**

## 📦 **Detailed Installation**

### **Step 1: Prepare Windows VPS**

#### **A. Windows Server Setup**
```powershell
# Enable Windows features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
```

#### **B. Windows Updates**
```powershell
# Install Windows Updates
Install-Module -Name PSWindowsUpdate -Force
Get-WindowsUpdate -Install -AcceptAll -AutoReboot
```

### **Step 2: Install Dependencies**

#### **A. Install Chocolatey**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### **B. Install Required Software**
```powershell
# Install Python and dependencies
choco install python3 -y
choco install git -y
choco install nginx -y
choco install curl -y
choco install nssm -y  # Non-Sucking Service Manager
```

### **Step 3: Application Setup**

#### **A. Create Application Directory**
```powershell
$appDir = "C:\ITHelpdesk"
New-Item -ItemType Directory -Path $appDir -Force
Set-Location $appDir
```

#### **B. Get Application Files**
```powershell
# Option 1: Clone from Git
git clone https://github.com/your-username/helpdesk.git .

# Option 2: Copy files manually
# Copy all application files to C:\ITHelpdesk
```

#### **C. Python Environment**
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r email_requirements.txt
```

### **Step 4: Windows Services Configuration**

#### **A. Create Service Scripts**
```batch
# start_main.bat
@echo off
cd /d C:\ITHelpdesk
call venv\Scripts\activate.bat
python app.py
```

```batch
# start_email.bat
@echo off
cd /d C:\ITHelpdesk
call venv\Scripts\activate.bat
python email_notifications.py
```

#### **B. Install Services with NSSM**
```powershell
# Install main application service
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" install "ITHelpdeskMain" "C:\ITHelpdesk\start_main.bat"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain" DisplayName "IT Helpdesk Main Application"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain" Start SERVICE_AUTO_START

# Install email service
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" install "ITHelpdeskEmail" "C:\ITHelpdesk\start_email.bat"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskEmail" DisplayName "IT Helpdesk Email Service"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskEmail" Start SERVICE_AUTO_START
```

### **Step 5: Nginx Configuration**

#### **A. Nginx Config File**
```nginx
# C:\tools\nginx\conf\nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream helpdesk_main {
        server 127.0.0.1:5000;
    }

    upstream helpdesk_email {
        server 127.0.0.1:5001;
    }

    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass http://helpdesk_main;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /email/ {
            proxy_pass http://helpdesk_email/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

#### **B. Start Nginx**
```powershell
Start-Service nginx
```

### **Step 6: Environment Configuration**

#### **A. Create .env File**
```env
# C:\ITHelpdesk\.env
SQLITECLOUD_API_KEY=your_sqlitecloud_api_key_here
SQLITECLOUD_URL=your_sqlitecloud_url_here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=IT Helpdesk <your_email@gmail.com>
NOTIFY_EMAILS=team1@company.com,team2@company.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
```

### **Step 7: Windows Firewall Configuration**

```powershell
# Allow HTTP and HTTPS
New-NetFirewallRule -DisplayName "IT Helpdesk HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "IT Helpdesk HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow

# Allow application ports
New-NetFirewallRule -DisplayName "IT Helpdesk Main App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
New-NetFirewallRule -DisplayName "IT Helpdesk Email Service" -Direction Inbound -Protocol TCP -LocalPort 5001 -Action Allow
```

## 🔧 **Service Management**

### **Windows Services Commands**
```powershell
# Check service status
Get-Service ITHelpdesk*

# Start services
Start-Service ITHelpdeskMain
Start-Service ITHelpdeskEmail

# Stop services
Stop-Service ITHelpdeskMain
Stop-Service ITHelpdeskEmail

# Restart services
Restart-Service ITHelpdeskMain
Restart-Service ITHelpdeskEmail

# Set services to auto-start
Set-Service ITHelpdeskMain -StartupType Automatic
Set-Service ITHelpdeskEmail -StartupType Automatic
```

### **Service Monitoring**
```powershell
# Monitor service status
while ($true) {
    Get-Service ITHelpdesk* | Format-Table Name, Status, StartType
    Start-Sleep -Seconds 30
}

# Check service logs
Get-EventLog -LogName Application -Source ITHelpdesk* -Newest 10
```

## 🔒 **Security Configuration**

### **Windows Defender**
```powershell
# Update Windows Defender
Update-MpSignature

# Configure real-time protection
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -DisableBehaviorMonitoring $false
Set-MpPreference -DisableOnAccessProtection $false
```

### **RDP Security**
```powershell
# Enable Network Level Authentication
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1

# Change RDP port (optional)
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "PortNumber" -Value 3389
```

### **SSL Certificate Setup**
```powershell
# Install Certbot for Windows
choco install certbot -y

# Generate SSL certificate
certbot certonly --standalone -d your-domain.com
```

## 📊 **Monitoring and Logging**

### **Performance Monitoring**
```powershell
# Create performance counter
New-Counter -CounterName "\IT Helpdesk\Active Connections" -Description "Active connections to IT Helpdesk"

# Monitor system resources
Get-Counter "\Processor(_Total)\% Processor Time", "\Memory\Available MBytes" -Continuous
```

### **Log Management**
```powershell
# Configure log rotation
$logPath = "C:\ITHelpdesk\logs"
New-Item -ItemType Directory -Path $logPath -Force

# Create log rotation script
$logRotationScript = @"
Get-ChildItem "$logPath\*.log" | Where-Object {`$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
"@

$logRotationScript | Out-File -FilePath "C:\ITHelpdesk\rotate_logs.ps1" -Encoding UTF8
```

### **Health Checks**
```powershell
# Create health check script
$healthCheckScript = @"
try {
    `$response = Invoke-WebRequest -Uri "http://localhost:5000/" -TimeoutSec 10 -UseBasicParsing
    if (`$response.StatusCode -eq 200) {
        Write-Host "Main app: OK" -ForegroundColor Green
    }
} catch {
    Write-Host "Main app: FAILED" -ForegroundColor Red
}

try {
    `$response = Invoke-WebRequest -Uri "http://localhost:5001/health" -TimeoutSec 10 -UseBasicParsing
    if (`$response.StatusCode -eq 200) {
        Write-Host "Email service: OK" -ForegroundColor Green
    }
} catch {
    Write-Host "Email service: FAILED" -ForegroundColor Red
}
"@

$healthCheckScript | Out-File -FilePath "C:\ITHelpdesk\health_check.ps1" -Encoding UTF8
```

## 🔄 **Backup and Recovery**

### **Automated Backup**
```powershell
# Create backup script
$backupScript = @"
`$backupDir = "C:\Backups\ITHelpdesk"
`$date = Get-Date -Format "yyyyMMdd_HHmmss"

New-Item -ItemType Directory -Path "`$backupDir\`$date" -Force

# Backup application files
Copy-Item "C:\ITHelpdesk" -Destination "`$backupDir\`$date\ITHelpdesk" -Recurse

# Backup configuration
Copy-Item "C:\ITHelpdesk\.env" -Destination "`$backupDir\`$date\"

Write-Host "Backup completed: `$backupDir\`$date" -ForegroundColor Green
"@

$backupScript | Out-File -FilePath "C:\ITHelpdesk\backup.ps1" -Encoding UTF8
```

### **Scheduled Tasks**
```powershell
# Create scheduled task for health checks
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\ITHelpdesk\health_check.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "IT Helpdesk Health Check" -Description "Monitor IT Helpdesk services"

# Create scheduled task for backups
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\ITHelpdesk\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 2AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "IT Helpdesk Backup" -Description "Daily backup of IT Helpdesk"
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Service Won't Start**
```powershell
# Check service status
Get-Service ITHelpdeskMain
Get-WinEvent -LogName Application -MaxEvents 10 | Where-Object {$_.ProviderName -like "*ITHelpdesk*"}

# Check application logs
Get-Content "C:\ITHelpdesk\logs\app.log" -Tail 20
```

#### **Port Conflicts**
```powershell
# Check port usage
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Kill process using port
taskkill /PID <PID> /F
```

#### **Python Environment Issues**
```powershell
# Recreate virtual environment
Remove-Item "C:\ITHelpdesk\venv" -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r email_requirements.txt
```

### **Performance Optimization**

#### **Windows Performance**
```powershell
# Disable unnecessary services
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -eq "Stopped"} | Set-Service -StartupType Disabled

# Optimize virtual memory
$pageFile = Get-WmiObject -Class Win32_PageFileSetting
$pageFile.InitialSize = 2048
$pageFile.MaximumSize = 4096
$pageFile.Put()
```

## 📈 **Scaling and Load Balancing**

### **Multiple Instances**
```powershell
# Create additional service instances
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" install "ITHelpdeskMain2" "C:\ITHelpdesk\start_main.bat"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain2" AppParameters "--port 5002"
```

### **Load Balancer Configuration**
```nginx
upstream helpdesk_main {
    server 127.0.0.1:5000;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

## 💰 **Cost Optimization**

### **Resource Monitoring**
```powershell
# Monitor resource usage
Get-Counter "\Processor(_Total)\% Processor Time", "\Memory\Available MBytes", "\PhysicalDisk(_Total)\% Disk Time" -SampleInterval 1 -MaxSamples 60
```

### **Auto-scaling Script**
```powershell
# Create auto-scaling script based on CPU usage
$cpuUsage = (Get-Counter "\Processor(_Total)\% Processor Time").CounterSamples.CookedValue
if ($cpuUsage -gt 80) {
    # Scale up
    Start-Service ITHelpdeskMain2
} elseif ($cpuUsage -lt 20) {
    # Scale down
    Stop-Service ITHelpdeskMain2
}
```

## 🎯 **Best Practices**

### **Security**
- ✅ Regular Windows Updates
- ✅ Windows Defender enabled
- ✅ Firewall configured
- ✅ RDP secured
- ✅ SSL certificates
- ✅ Regular backups

### **Performance**
- ✅ Monitor resource usage
- ✅ Optimize virtual memory
- ✅ Regular maintenance
- ✅ Log rotation
- ✅ Health monitoring

### **Reliability**
- ✅ Service auto-restart
- ✅ Health checks
- ✅ Automated backups
- ✅ Disaster recovery plan
- ✅ Monitoring alerts

## 🚀 **Quick Start Commands**

```powershell
# Deploy everything
.\deploy_windows.ps1

# Check status
Get-Service ITHelpdesk*

# View logs
Get-EventLog -LogName Application -Source ITHelpdesk* -Newest 10

# Health check
.\health_check.ps1

# Backup
.\backup.ps1
```

Your Windows VPS deployment is now ready for production use! 🎉
