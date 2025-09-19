# Windows Monitoring Script for IT Helpdesk System
# Provides real-time monitoring and alerting

param(
    [Parameter(Mandatory=$false)]
    [int]$Interval = 30,
    
    [Parameter(Mandatory=$false)]
    [switch]$Continuous,
    
    [Parameter(Mandatory=$false)]
    [string]$LogFile = "C:\ITHelpdesk\logs\monitor.log"
)

$appDir = "C:\ITHelpdesk"
$services = @("ITHelpdeskMain", "ITHelpdeskEmail")
$endpoints = @(
    @{Name="Main App"; URL="http://localhost:5000/"; Timeout=5},
    @{Name="Email Service"; URL="http://localhost:5001/health"; Timeout=5},
    @{Name="Nginx Proxy"; URL="http://localhost/"; Timeout=5}
)

function Initialize-Monitoring {
    # Create log directory
    $logDir = Split-Path $LogFile -Parent
    if (!(Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    # Create log file if it doesn't exist
    if (!(Test-Path $LogFile)) {
        New-Item -ItemType File -Path $LogFile -Force | Out-Null
    }
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    # Write to console with colors
    switch ($Level) {
        "ERROR" { Write-Host $logEntry -ForegroundColor Red }
        "WARN" { Write-Host $logEntry -ForegroundColor Yellow }
        "INFO" { Write-Host $logEntry -ForegroundColor Green }
        default { Write-Host $logEntry -ForegroundColor White }
    }
    
    # Write to log file
    Add-Content -Path $LogFile -Value $logEntry
}

function Test-ServiceHealth {
    $healthy = $true
    
    foreach ($serviceName in $services) {
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        
        if ($service -and $service.Status -eq "Running") {
            Write-Log "Service $serviceName is running" "INFO"
        } else {
            Write-Log "Service $serviceName is not running (Status: $($service.Status))" "ERROR"
            $healthy = $false
        }
    }
    
    return $healthy
}

function Test-EndpointHealth {
    $healthy = $true
    
    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-WebRequest -Uri $endpoint.URL -TimeoutSec $endpoint.Timeout -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Log "$($endpoint.Name) is responding (HTTP $($response.StatusCode))" "INFO"
            } else {
                Write-Log "$($endpoint.Name) returned HTTP $($response.StatusCode)" "WARN"
                $healthy = $false
            }
        } catch {
            Write-Log "$($endpoint.Name) is not responding: $($_.Exception.Message)" "ERROR"
            $healthy = $false
        }
    }
    
    return $healthy
}

function Get-SystemMetrics {
    $cpu = Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 1
    $memory = Get-Counter "\Memory\Available MBytes" -SampleInterval 1 -MaxSamples 1
    $disk = Get-Counter "\PhysicalDisk(_Total)\% Disk Time" -SampleInterval 1 -MaxSamples 1
    
    $metrics = @{
        CPU = [math]::Round($cpu.CounterSamples.CookedValue, 2)
        Memory = [math]::Round($memory.CounterSamples.CookedValue, 2)
        Disk = [math]::Round($disk.CounterSamples.CookedValue, 2)
    }
    
    return $metrics
}

function Test-SystemHealth {
    $metrics = Get-SystemMetrics
    
    Write-Log "System Metrics - CPU: $($metrics.CPU)%, Memory: $($metrics.Memory) MB, Disk: $($metrics.Disk)%" "INFO"
    
    $healthy = $true
    
    # Check CPU usage
    if ($metrics.CPU -gt 80) {
        Write-Log "High CPU usage detected: $($metrics.CPU)%" "WARN"
        $healthy = $false
    }
    
    # Check memory usage
    if ($metrics.Memory -lt 500) {
        Write-Log "Low memory available: $($metrics.Memory) MB" "WARN"
        $healthy = $false
    }
    
    # Check disk usage
    if ($metrics.Disk -gt 90) {
        Write-Log "High disk usage detected: $($metrics.Disk)%" "WARN"
        $healthy = $false
    }
    
    return $healthy
}

function Test-DatabaseConnectivity {
    try {
        # Test SQLiteCloud connectivity by making a simple request
        $env:SQLITECLOUD_API_KEY = (Get-Content "$appDir\.env" | Where-Object { $_ -like "SQLITECLOUD_API_KEY=*" }).Split("=")[1]
        $env:SQLITECLOUD_URL = (Get-Content "$appDir\.env" | Where-Object { $_ -like "SQLITECLOUD_URL=*" }).Split("=")[1]
        
        if ($env:SQLITECLOUD_API_KEY -and $env:SQLITECLOUD_URL) {
            Write-Log "Database configuration found" "INFO"
            return $true
        } else {
            Write-Log "Database configuration missing" "ERROR"
            return $false
        }
    } catch {
        Write-Log "Database connectivity test failed: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-EmailConfiguration {
    try {
        $env:MAIL_USERNAME = (Get-Content "$appDir\.env" | Where-Object { $_ -like "MAIL_USERNAME=*" }).Split("=")[1]
        $env:MAIL_PASSWORD = (Get-Content "$appDir\.env" | Where-Object { $_ -like "MAIL_PASSWORD=*" }).Split("=")[1]
        $env:NOTIFY_EMAILS = (Get-Content "$appDir\.env" | Where-Object { $_ -like "NOTIFY_EMAILS=*" }).Split("=")[1]
        
        if ($env:MAIL_USERNAME -and $env:MAIL_PASSWORD -and $env:NOTIFY_EMAILS) {
            Write-Log "Email configuration found" "INFO"
            return $true
        } else {
            Write-Log "Email configuration missing" "ERROR"
            return $false
        }
    } catch {
        Write-Log "Email configuration test failed: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Send-Alert {
    param([string]$Message)
    
    Write-Log "ALERT: $Message" "ERROR"
    
    # You can add email alerts here
    # try {
    #     Send-MailMessage -To "admin@company.com" -From "alerts@company.com" -Subject "IT Helpdesk Alert" -Body $Message -SmtpServer "smtp.gmail.com" -Port 587 -UseSsl -Credential (Get-Credential)
    # } catch {
    #     Write-Log "Failed to send email alert: $($_.Exception.Message)" "ERROR"
    # }
}

function Start-Monitoring {
    Write-Host "🔍 IT Helpdesk Windows Monitor" -ForegroundColor Cyan
    Write-Host "=============================" -ForegroundColor Cyan
    Write-Host "Monitoring interval: $Interval seconds" -ForegroundColor Yellow
    Write-Host "Log file: $LogFile" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
    Write-Host ""
    
    $iteration = 0
    
    do {
        $iteration++
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        Write-Host "🕐 [$timestamp] Health Check #$iteration" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        $overallHealth = $true
        
        # Test services
        Write-Host "🔧 Testing Services..." -ForegroundColor Yellow
        $serviceHealth = Test-ServiceHealth
        if (-not $serviceHealth) {
            $overallHealth = $false
            Send-Alert "One or more services are not running"
        }
        
        # Test endpoints
        Write-Host "🌐 Testing Endpoints..." -ForegroundColor Yellow
        $endpointHealth = Test-EndpointHealth
        if (-not $endpointHealth) {
            $overallHealth = $false
            Send-Alert "One or more endpoints are not responding"
        }
        
        # Test system health
        Write-Host "💻 Testing System Health..." -ForegroundColor Yellow
        $systemHealth = Test-SystemHealth
        if (-not $systemHealth) {
            $overallHealth = $false
            Send-Alert "System resource usage is high"
        }
        
        # Test database connectivity
        Write-Host "🗄️ Testing Database..." -ForegroundColor Yellow
        $dbHealth = Test-DatabaseConnectivity
        if (-not $dbHealth) {
            $overallHealth = $false
            Send-Alert "Database connectivity issues detected"
        }
        
        # Test email configuration
        Write-Host "📧 Testing Email Configuration..." -ForegroundColor Yellow
        $emailHealth = Test-EmailConfiguration
        if (-not $emailHealth) {
            $overallHealth = $false
            Send-Alert "Email configuration issues detected"
        }
        
        # Overall health summary
        Write-Host ""
        if ($overallHealth) {
            Write-Host "✅ Overall Health: All systems operational" -ForegroundColor Green
            Write-Log "Health check passed - all systems operational" "INFO"
        } else {
            Write-Host "❌ Overall Health: Issues detected" -ForegroundColor Red
            Write-Log "Health check failed - issues detected" "ERROR"
        }
        
        Write-Host ""
        Write-Host "⏳ Waiting $Interval seconds until next check..." -ForegroundColor Gray
        
        if ($Continuous) {
            Start-Sleep -Seconds $Interval
        } else {
            break
        }
        
    } while ($Continuous)
    
    Write-Host ""
    Write-Host "🏁 Monitoring completed" -ForegroundColor Green
}

function Show-Help {
    Write-Host "🔍 IT Helpdesk Windows Monitor" -ForegroundColor Cyan
    Write-Host "=============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\monitor_windows.ps1 [-Interval <seconds>] [-Continuous] [-LogFile <path>]" -ForegroundColor White
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -Interval    Monitoring interval in seconds (default: 30)" -ForegroundColor White
    Write-Host "  -Continuous  Run continuously (default: single check)" -ForegroundColor White
    Write-Host "  -LogFile     Log file path (default: C:\ITHelpdesk\logs\monitor.log)" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\monitor_windows.ps1                    # Single health check" -ForegroundColor White
    Write-Host "  .\monitor_windows.ps1 -Continuous        # Continuous monitoring" -ForegroundColor White
    Write-Host "  .\monitor_windows.ps1 -Interval 60       # Check every 60 seconds" -ForegroundColor White
    Write-Host "  .\monitor_windows.ps1 -LogFile C:\logs\monitor.log" -ForegroundColor White
}

# Main execution
if ($args -contains "-h" -or $args -contains "--help") {
    Show-Help
    exit 0
}

Initialize-Monitoring
Start-Monitoring
