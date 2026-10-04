# College Placement Prediction - PowerShell Launcher
$pyPath = "C:\Users\naidu\AppData\Local\Programs\Python\Python311"
$pyExe = "$pyPath\python.exe"

# Refresh current session path so 'python' works directly
$env:Path = "$pyPath;$pyPath\Scripts;" + $env:Path

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  College Placement Prediction - Web Application" -ForegroundColor White
Write-Host "  BCA Mini Project (Machine Learning)" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $pyExe) {
    Write-Host "Using Python from: $pyExe" -ForegroundColor Green
    Write-Host "Starting Flask Web Server at: http://127.0.0.1:5000" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Gray
    Write-Host ""
    & $pyExe "app/app.py"
} else {
    python "app/app.py"
}
