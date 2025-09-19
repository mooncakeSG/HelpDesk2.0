# Windows VPS Deployment Script for IT Helpdesk System
# Run this script as Administrator on Windows Server

Write-Host "🪟 Deploying IT Helpdesk on Windows VPS" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Check Windows version
$osVersion = [System.Environment]::OSVersion.Version
if ($osVersion.Major -lt 10) {
    Write-Host "❌ Windows 10/Server 2016 or later required" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Running as Administrator on Windows $($osVersion.Major)" -ForegroundColor Green
Write-Host ""

# Set execution policy
Write-Host "🔧 Setting PowerShell execution policy..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine -Force

# Install Chocolatey if not present
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Chocolatey package manager..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install required software
Write-Host "📦 Installing required software..." -ForegroundColor Yellow
$packages = @(
    "python3",
    "git",
    "nginx",
    "curl"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Gray
    choco install $package -y --no-progress
}

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Create application directory
$appDir = "C:\ITHelpdesk"
Write-Host "📁 Creating application directory: $appDir" -ForegroundColor Yellow
if (!(Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force
}

# Set working directory
Set-Location $appDir

# Get application files
Write-Host "📥 Getting application files..." -ForegroundColor Yellow
Write-Host "Please copy your application files to $appDir" -ForegroundColor Cyan
Write-Host "Or clone your repository:" -ForegroundColor Cyan
Write-Host "git clone https://github.com/your-username/helpdesk.git ." -ForegroundColor Gray
Read-Host "Press Enter when files are ready"

# Create virtual environment
Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
& ".\venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install -r email_requirements.txt

# Create Windows Services
Write-Host "⚙️ Creating Windows Services..." -ForegroundColor Yellow

# Main application service
$mainServiceScript = @"
@echo off
cd /d $appDir
call venv\Scripts\activate.bat
python app.py
"@

$mainServiceScript | Out-File -FilePath "$appDir\start_main.bat" -Encoding ASCII

# Email service script
$emailServiceScript = @"
@echo off
cd /d $appDir
call venv\Scripts\activate.bat
python email_notifications.py
"@

$emailServiceScript | Out-File -FilePath "$appDir\start_email.bat" -Encoding ASCII

# Install services using NSSM (Non-Sucking Service Manager)
Write-Host "📦 Installing NSSM for service management..." -ForegroundColor Yellow
choco install nssm -y --no-progress

# Create main application service
Write-Host "Creating main application service..." -ForegroundColor Gray
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" install "ITHelpdeskMain" "$appDir\start_main.bat"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain" DisplayName "IT Helpdesk Main Application"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain" Description "IT Helpdesk Main Flask Application"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskMain" Start SERVICE_AUTO_START

# Create email service
Write-Host "Creating email service..." -ForegroundColor Gray
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" install "ITHelpdeskEmail" "$appDir\start_email.bat"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskEmail" DisplayName "IT Helpdesk Email Service"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskEmail" Description "IT Helpdesk Email Notification Service"
& "C:\ProgramData\chocolatey\lib\nssm\tools\nssm.exe" set "ITHelpdeskEmail" Start SERVICE_AUTO_START

# Configure Nginx
Write-Host "🌐 Configuring Nginx..." -ForegroundColor Yellow
$nginxConfig = @"
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
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto `$scheme;
        }

        location /email/ {
            proxy_pass http://helpdesk_email/;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto `$scheme;
        }
    }
}
"@

$nginxConfig | Out-File -FilePath "C:\tools\nginx\conf\nginx.conf" -Encoding UTF8

# Create environment file
Write-Host "⚙️ Creating environment configuration..." -ForegroundColor Yellow
$envContent = @"
# Database Configuration
SQLITECLOUD_API_KEY=your_sqlitecloud_api_key_here
SQLITECLOUD_URL=your_sqlitecloud_url_here

# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=IT Helpdesk <your_email@gmail.com>
NOTIFY_EMAILS=team1@company.com,team2@company.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
"@

$envContent | Out-File -FilePath "$appDir\.env" -Encoding UTF8

Write-Host "Please update $appDir\.env with your actual configuration:" -ForegroundColor Cyan
Write-Host "   - SQLiteCloud API Key and URL" -ForegroundColor Gray
Write-Host "   - Gmail credentials" -ForegroundColor Gray
Write-Host "   - Notification email addresses" -ForegroundColor Gray
Read-Host "Press Enter when you've updated the .env file"

# Configure Windows Firewall
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "IT Helpdesk HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "IT Helpdesk HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IT Helpdesk Main App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
New-NetFirewallRule -DisplayName "IT Helpdesk Email Service" -Direction Inbound -Protocol TCP -LocalPort 5001 -Action Allow

# Start services
Write-Host "🚀 Starting services..." -ForegroundColor Yellow
Start-Service "ITHelpdeskMain"
Start-Service "ITHelpdeskEmail"
Start-Service "nginx"

# Wait for services to start
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service status
Write-Host "🔍 Checking service status..." -ForegroundColor Yellow
$services = @("ITHelpdeskMain", "ITHelpdeskEmail", "nginx")
foreach ($service in $services) {
    $status = Get-Service -Name $service -ErrorAction SilentlyContinue
    if ($status) {
        if ($status.Status -eq "Running") {
            Write-Host "✅ $service is running" -ForegroundColor Green
        } else {
            Write-Host "❌ $service is not running (Status: $($status.Status))" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ $service service not found" -ForegroundColor Red
    }
}

# Test endpoints
Write-Host "🧪 Testing endpoints..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Main app is running on http://localhost:5000" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Main app is not responding" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/health" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Email service is running on http://localhost:5001" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Email service is not responding" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Nginx proxy is working on http://localhost" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Nginx proxy is not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Windows VPS deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your services are available at:" -ForegroundColor Cyan
Write-Host "   Main App: http://localhost:5000" -ForegroundColor White
Write-Host "   Email Service: http://localhost:5001" -ForegroundColor White
Write-Host "   Nginx Proxy: http://localhost" -ForegroundColor White
Write-Host ""
Write-Host "📝 Useful commands:" -ForegroundColor Cyan
Write-Host "   View service status: Get-Service ITHelpdesk*" -ForegroundColor White
Write-Host "   Start services: Start-Service ITHelpdeskMain,ITHelpdeskEmail" -ForegroundColor White
Write-Host "   Stop services: Stop-Service ITHelpdeskMain,ITHelpdeskEmail" -ForegroundColor White
Write-Host "   Restart services: Restart-Service ITHelpdeskMain,ITHelpdeskEmail" -ForegroundColor White
Write-Host "   View logs: Get-EventLog -LogName Application -Source ITHelpdesk*" -ForegroundColor White
Write-Host ""
Write-Host "🔧 To update the application:" -ForegroundColor Cyan
Write-Host "   1. Stop services: Stop-Service ITHelpdeskMain,ITHelpdeskEmail" -ForegroundColor White
Write-Host "   2. Update files in $appDir" -ForegroundColor White
Write-Host "   3. Start services: Start-Service ITHelpdeskMain,ITHelpdeskEmail" -ForegroundColor White
Write-Host ""
Write-Host "🔒 Security recommendations:" -ForegroundColor Cyan
Write-Host "   1. Set up SSL certificate with Let's Encrypt" -ForegroundColor White
Write-Host "   2. Configure Windows Defender" -ForegroundColor White
Write-Host "   3. Regular Windows Updates" -ForegroundColor White
Write-Host "   4. Monitor Event Logs" -ForegroundColor White
Write-Host "   5. Configure RDP security" -ForegroundColor White
