
# Запускать из корневой директории проекта

if (Test-Path -Path ".venv") {
    Remove-Item -Path ".venv" -Recurse -Force
}

python -m venv .venv

.venv\Scripts\Activate.ps1

Add-Content -Path .venv\Scripts\Activate.ps1 -Value "function global:docdev {docker compose -f docker-compose.dev.yaml @args}"
Add-Content -Path .venv\Scripts\Activate.ps1 -Value "function global:docprod {docker compose -f docker-compose.prod.yaml @args}"

Set-Location services

foreach ($file in Get-ChildItem -Directory) {
    Set-Location $file
    if (Test-Path -Path "requirements.txt") {
        pip install -r requirements.txt
    }
    Set-Location ..
}

Set-Location ..
python.exe -m pip install --upgrade pip
