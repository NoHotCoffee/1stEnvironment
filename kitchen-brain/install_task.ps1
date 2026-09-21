$taskName = "KitchenBrain"
$batPath = Join-Path $PSScriptRoot "start_kitchen_brain.bat"

Write-Host "Run this command in PowerShell to create the scheduled task (does not run automatically here):"
Write-Host "schtasks /Create /SC ONLOGON /RL LIMITED /TN `"$taskName`" /TR `"`"$batPath`"`""
