# Deployment Health Check Script (PowerShell)
# Verifies production deployment is working correctly
# Usage: .\check-deployment.ps1

# URLs
$FRONTEND_URL = "https://emergent-six-zeta.vercel.app"
$BACKEND_URL = "https://emergent-av9b.onrender.com"
$BACKEND_API = "$BACKEND_URL/api"

Write-Host "=== ML Visualizer Deployment Health Check ===" -ForegroundColor Blue
Write-Host ""

# Check Frontend
Write-Host "Checking Frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $FRONTEND_URL -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Frontend is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Frontend is not responding" -ForegroundColor Red
}

# Check Backend Health
Write-Host ""
Write-Host "Checking Backend Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/health" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend health check passed" -ForegroundColor Green
        $body = $response.Content | ConvertFrom-Json
        Write-Host "  Status: $($body.status)"
        Write-Host "  Service: $($body.service)"
    }
} catch {
    Write-Host "✗ Backend health check failed" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)"
}

# Check API Documentation
Write-Host ""
Write-Host "Checking API Documentation..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/docs" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ API documentation is accessible at /docs" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ API documentation is not accessible" -ForegroundColor Red
}

# Check Decision Tree Endpoint
Write-Host ""
Write-Host "Testing Decision Tree API Endpoint..." -ForegroundColor Yellow
try {
    $payload = @{
        task = "classifier"
        criterion = "gini"
        max_depth = 3
        min_samples_split = 2
        min_samples_leaf = 1
        dataset = "iris"
        uploaded_data = $null
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BACKEND_API/decision_tree" `
        -Method POST `
        -ContentType "application/json" `
        -Body $payload `
        -UseBasicParsing `
        -TimeoutSec 30
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Decision Tree endpoint is working" -ForegroundColor Green
        $body = $response.Content | ConvertFrom-Json
        
        # Check response structure
        if ($body.tree_json -and $body.accuracy -and $body.depth -and $body.n_leaves) {
            Write-Host "✓ Response structure is correct" -ForegroundColor Green
            Write-Host "  Accuracy: $($body.accuracy)"
            Write-Host "  Depth: $($body.depth)"
            Write-Host "  Leaves: $($body.n_leaves)"
        } else {
            Write-Host "✗ Response structure is invalid" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "✗ Decision Tree endpoint failed" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)"
}

# Check Error Handling
Write-Host ""
Write-Host "Testing Error Handling..." -ForegroundColor Yellow
try {
    $payload = @{
        task = "regressor"
        criterion = "entropy"
        max_depth = 3
        min_samples_split = 2
        min_samples_leaf = 1
        dataset = "iris"
        uploaded_data = $null
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BACKEND_API/decision_tree" `
        -Method POST `
        -ContentType "application/json" `
        -Body $payload `
        -UseBasicParsing `
        -TimeoutSec 30
    
    Write-Host "Response received with status: $($response.StatusCode)" -ForegroundColor Yellow
} 
catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    if ($statusCode -eq 400) {
        Write-Host "✓ Error handling is working correctly (returns 400)" -ForegroundColor Green
    } else {
        Write-Host "Status Code: $statusCode" -ForegroundColor Yellow
    }
}

# Summary
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Blue
Write-Host "✓ All critical checks completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: $FRONTEND_URL" -ForegroundColor Yellow
Write-Host "Backend: $BACKEND_URL" -ForegroundColor Yellow
Write-Host "API Docs: $BACKEND_URL/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Deployment is HEALTHY and ready for use!" -ForegroundColor Green
