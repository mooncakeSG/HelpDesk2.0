# Windows Service Management Script for IT Helpdesk
# Provides easy management of IT Helpdesk services

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "health", "backup", "update")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("main", "email", "all")]
    [string]$Service = "all"
)

$appDir = "C:\ITHelpdesk"
$services = @{
    "main" = "ITHelpdeskMain"
    "email" = "ITHelpdeskEmail"
}

function Show-Header {
    Write-Host "🪟 IT Helpdesk Windows Service Manager" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
}

function Start-Services {
    param([string]$serviceType)
    
    if ($serviceType -eq "all") {
        Write-Host "🚀 Starting all IT Helpdesk services..." -ForegroundColor Yellow
        foreach ($service in $services.Values) {
            try {
                Start-Service -Name $service -ErrorAction Stop
                Write-Host "✅ Started $service" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to start $service : $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        $serviceName = $services[$serviceType]
        if ($serviceName) {
            Write-Host "🚀 Starting $serviceName..." -ForegroundColor Yellow
            try {
                Start-Service -Name $serviceName -ErrorAction Stop
                Write-Host "✅ Started $serviceName" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to start $serviceName : $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Unknown service: $serviceType" -ForegroundColor Red
        }
    }
}

function Stop-Services {
    param([string]$serviceType)
    
    if ($serviceType -eq "all") {
        Write-Host "🛑 Stopping all IT Helpdesk services..." -ForegroundColor Yellow
        foreach ($service in $services.Values) {
            try {
                Stop-Service -Name $service -ErrorAction Stop
                Write-Host "✅ Stopped $service" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to stop $service : $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        $serviceName = $services[$serviceType]
        if ($serviceName) {
            Write-Host "🛑 Stopping $serviceName..." -ForegroundColor Yellow
            try {
                Stop-Service -Name $serviceName -ErrorAction Stop
                Write-Host "✅ Stopped $serviceName" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to stop $serviceName : $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Unknown service: $serviceType" -ForegroundColor Red
        }
    }
}

function Restart-Services {
    param([string]$serviceType)
    
    if ($serviceType -eq "all") {
        Write-Host "🔄 Restarting all IT Helpdesk services..." -ForegroundColor Yellow
        foreach ($service in $services.Values) {
            try {
                Restart-Service -Name $service -ErrorAction Stop
                Write-Host "✅ Restarted $service" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to restart $service : $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        $serviceName = $services[$serviceType]
        if ($serviceName) {
            Write-Host "🔄 Restarting $serviceName..." -ForegroundColor Yellow
            try {
                Restart-Service -Name $serviceName -ErrorAction Stop
                Write-Host "✅ Restarted $serviceName" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to restart $serviceName : $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Unknown service: $serviceType" -ForegroundColor Red
        }
    }
}

function Show-Status {
    Write-Host "📊 IT Helpdesk Service Status" -ForegroundColor Yellow
    Write-Host "=============================" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($serviceType in $services.Keys) {
        $serviceName = $services[$serviceType]
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        
        if ($service) {
            $statusColor = switch ($service.Status) {
                "Running" { "Green" }
                "Stopped" { "Red" }
                "Starting" { "Yellow" }
                "Stopping" { "Yellow" }
                default { "Gray" }
            }
            
            Write-Host "$serviceType service ($serviceName): " -NoNewline
            Write-Host $service.Status -ForegroundColor $statusColor
            Write-Host "   Start Type: $($service.StartType)" -ForegroundColor Gray
        } else {
            Write-Host "$serviceType service ($serviceName): " -NoNewline
            Write-Host "Not Found" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "🌐 Endpoint Status:" -ForegroundColor Yellow
    
    # Test main app
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "   Main App (http://localhost:5000): " -NoNewline
            Write-Host "✅ Online" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Main App (http://localhost:5000): " -NoNewline
        Write-Host "❌ Offline" -ForegroundColor Red
    }
    
    # Test email service
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5001/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "   Email Service (http://localhost:5001): " -NoNewline
            Write-Host "✅ Online" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Email Service (http://localhost:5001): " -NoNewline
        Write-Host "❌ Offline" -ForegroundColor Red
    }
    
    # Test nginx proxy
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "   Nginx Proxy (http://localhost): " -NoNewline
            Write-Host "✅ Online" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Nginx Proxy (http://localhost): " -NoNewline
        Write-Host "❌ Offline" -ForegroundColor Red
    }
}

function Show-Logs {
    Write-Host "📋 IT Helpdesk Service Logs" -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Yellow
    Write-Host ""
    
    # Show recent application logs
    Write-Host "Recent Application Logs:" -ForegroundColor Cyan
    try {
        Get-EventLog -LogName Application -Source "*ITHelpdesk*" -Newest 10 | ForEach-Object {
            $time = $_.TimeGenerated.ToString("yyyy-MM-dd HH:mm:ss")
            $level = switch ($_.EntryType) {
                "Error" { "🔴 ERROR" }
                "Warning" { "🟡 WARN" }
                "Information" { "🔵 INFO" }
                default { "⚪ $($_.EntryType)" }
            }
            Write-Host "   [$time] $level - $($_.Message)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   No application logs found" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Recent System Logs:" -ForegroundColor Cyan
    try {
        Get-EventLog -LogName System -Source "*Service*" -Newest 5 | Where-Object { $_.Message -like "*ITHelpdesk*" } | ForEach-Object {
            $time = $_.TimeGenerated.ToString("yyyy-MM-dd HH:mm:ss")
            Write-Host "   [$time] $($_.Message)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   No system logs found" -ForegroundColor Gray
    }
}

function Test-Health {
    Write-Host "🏥 IT Helpdesk Health Check" -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Yellow
    Write-Host ""
    
    $allHealthy = $true
    
    # Check services
    Write-Host "Service Health:" -ForegroundColor Cyan
    foreach ($serviceType in $services.Keys) {
        $serviceName = $services[$serviceType]
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        
        if ($service -and $service.Status -eq "Running") {
            Write-Host "   $serviceType service: ✅ Healthy" -ForegroundColor Green
        } else {
            Write-Host "   $serviceType service: ❌ Unhealthy" -ForegroundColor Red
            $allHealthy = $false
        }
    }
    
    Write-Host ""
    Write-Host "Endpoint Health:" -ForegroundColor Cyan
    
    # Test main app
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "   Main App: ✅ Responding" -ForegroundColor Green
        } else {
            Write-Host "   Main App: ❌ HTTP $($response.StatusCode)" -ForegroundColor Red
            $allHealthy = $false
        }
    } catch {
        Write-Host "   Main App: ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
    
    # Test email service
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5001/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $healthData = $response.Content | ConvertFrom-Json
            Write-Host "   Email Service: ✅ $($healthData.status)" -ForegroundColor Green
        } else {
            Write-Host "   Email Service: ❌ HTTP $($response.StatusCode)" -ForegroundColor Red
            $allHealthy = $false
        }
    } catch {
        Write-Host "   Email Service: ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
    
    Write-Host ""
    if ($allHealthy) {
        Write-Host "🎉 Overall Health: ✅ All systems operational" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Overall Health: ❌ Some issues detected" -ForegroundColor Red
    }
}

function Backup-System {
    Write-Host "💾 IT Helpdesk System Backup" -ForegroundColor Yellow
    Write-Host "============================" -ForegroundColor Yellow
    Write-Host ""
    
    $backupDir = "C:\Backups\ITHelpdesk"
    $date = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "$backupDir\$date"
    
    try {
        New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
        
        Write-Host "📁 Backing up application files..." -ForegroundColor Gray
        Copy-Item "$appDir" -Destination "$backupPath\ITHelpdesk" -Recurse -Exclude "venv", "__pycache__", "*.pyc"
        
        Write-Host "⚙️ Backing up configuration..." -ForegroundColor Gray
        Copy-Item "$appDir\.env" -Destination "$backupPath\" -ErrorAction SilentlyContinue
        
        Write-Host "📋 Backing up service configuration..." -ForegroundColor Gray
        Get-Service ITHelpdesk* | Export-Csv "$backupPath\services.csv" -NoTypeInformation
        
        Write-Host "✅ Backup completed: $backupPath" -ForegroundColor Green
        Write-Host "   Size: $((Get-ChildItem $backupPath -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB) MB" -ForegroundColor Gray
        
    } catch {
        Write-Host "❌ Backup failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Update-System {
    Write-Host "🔄 IT Helpdesk System Update" -ForegroundColor Yellow
    Write-Host "============================" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "⚠️ This will stop services, update code, and restart services" -ForegroundColor Yellow
    $confirm = Read-Host "Continue? (y/N)"
    
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "Update cancelled" -ForegroundColor Gray
        return
    }
    
    try {
        Write-Host "🛑 Stopping services..." -ForegroundColor Gray
        Stop-Services -serviceType "all"
        
        Write-Host "📥 Updating application files..." -ForegroundColor Gray
        if (Test-Path "$appDir\.git") {
            Set-Location $appDir
            git pull
        } else {
            Write-Host "   No git repository found. Please update files manually." -ForegroundColor Yellow
        }
        
        Write-Host "📦 Updating Python dependencies..." -ForegroundColor Gray
        Set-Location $appDir
        & ".\venv\Scripts\Activate.ps1"
        pip install -r requirements.txt --upgrade
        pip install -r email_requirements.txt --upgrade
        
        Write-Host "🚀 Starting services..." -ForegroundColor Gray
        Start-Services -serviceType "all"
        
        Write-Host "✅ Update completed successfully" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Update failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "🔄 Attempting to restart services..." -ForegroundColor Yellow
        Start-Services -serviceType "all"
    }
}

# Main execution
Show-Header

switch ($Action) {
    "start" { Start-Services -serviceType $Service }
    "stop" { Stop-Services -serviceType $Service }
    "restart" { Restart-Services -serviceType $Service }
    "status" { Show-Status }
    "logs" { Show-Logs }
    "health" { Test-Health }
    "backup" { Backup-System }
    "update" { Update-System }
}

Write-Host ""
Write-Host "💡 Usage Examples:" -ForegroundColor Cyan
Write-Host "   .\manage_windows_services.ps1 -Action start -Service main" -ForegroundColor Gray
Write-Host "   .\manage_windows_services.ps1 -Action status" -ForegroundColor Gray
Write-Host "   .\manage_windows_services.ps1 -Action health" -ForegroundColor Gray
Write-Host "   .\manage_windows_services.ps1 -Action backup" -ForegroundColor Gray
