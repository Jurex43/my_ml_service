# Helper script to run Django management commands
# Usage: .\run_django.ps1 migrate
# Usage: .\run_django.ps1 runserver
# Usage: .\run_django.ps1 makemigrations

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

python manage.py @Arguments
