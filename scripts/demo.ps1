param(
  [int]$Seed = 7
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $root

Write-Host "[1/4] Generate sample data" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" -m catalyst_ai.cli generate-data --seed $Seed

Write-Host "[2/4] Generate artifacts" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" -m catalyst_ai.cli generate-artifacts

Write-Host "[3/4] Run tests" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" -m pytest -q

Write-Host "[4/4] Start Streamlit" -ForegroundColor Cyan
& "$root\.venv\Scripts\python.exe" -m streamlit run "$root\streamlit_app.py"
