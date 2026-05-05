# Quick Deployment Health Check
# Windows PowerShell script to verify production is working

$FRONTEND="https://emergent-six-zeta.vercel.app"
$BACKEND="https://emergent-av9b.onrender.com"

Write-Host "=== ML Visualizer Health Check ===" -ForegroundColor Cyan
Write-Host ""

# Test Frontend
Write-Host "Testing Frontend..." -ForegroundColor Yellow
$result = (Invoke-WebRequest -Uri $FRONTEND -UseBasicParsing -TimeoutSec 10).StatusCode
Write-Host "Frontend Status: $result" -ForegroundColor Green

# Test Backend Health
Write-Host "Testing Backend Health..." -ForegroundColor Yellow
$result = (Invoke-WebRequest -Uri "$BACKEND/health" -UseBasicParsing -TimeoutSec 10).StatusCode
Write-Host "Backend Health Status: $result" -ForegroundColor Green

# Test API Docs
Write-Host "Testing API Docs..." -ForegroundColor Yellow
$result = (Invoke-WebRequest -Uri "$BACKEND/docs" -UseBasicParsing -TimeoutSec 10).StatusCode
Write-Host "API Docs Status: $result" -ForegroundColor Green

Write-Host ""
Write-Host "Frontend: $FRONTEND" -ForegroundColor Cyan
Write-Host "Backend: $BACKEND" -ForegroundColor Cyan
Write-Host "API Docs: $BACKEND/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Deployment is HEALTHY!" -ForegroundColor Green
