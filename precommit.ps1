$ErrorActionPreference = "Stop"

function Invoke-Check([string]$command, [string]$taskName)
{
    cmd.exe /c $command

    if ($LASTEXITCODE -ne 0)
    {
        Write-Error "Error @ ${taskName}"
        Read-Host
        Exit 1
    }
}

Write-Host "Checking with pydocstyle..." -Fore Cyan
Invoke-Check "pydocstyle dlasset --count" "pydocstyle"

Write-Host "Checking with pylint..." -Fore Cyan
Invoke-Check "pylint dlasset" "pylint"

Write-Host "Checking with mypy..." -Fore Cyan
Invoke-Check "mypy dlasset" "mypy"

Write-Host "Checking with bandit..." -Fore Cyan
Invoke-Check "bandit -r dlasset" "bandit"

Write-Host "Checking with flake8..." -Fore Cyan
Invoke-Check "flake8 dlasset --count" "flake8"

Write-Host "Running code tests..." -Fore Cyan
Invoke-Check "pytest" "code test"

Write-Host "--- All checks passed. ---" -Fore Green
Write-Host "Press any key to continue."
Read-Host
