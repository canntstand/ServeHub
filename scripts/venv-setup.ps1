python -m venv .venv

.venv\Scripts\Activate.ps1

Add-Content -Path .venv\Scripts\Activate.ps1 -Value "function global:docdev {docker compose -f docker-compose.dev.yaml @args}"
Add-Content -Path .venv\Scripts\Activate.ps1 -Value "function global:docprod {docker compose -f docker-compose.prod.yaml @args}"

pip install -r services\email-scheduler\requirements.txt
pip install -r services\link-preview\requirements.txt
python.exe -m pip install --upgrade pip

deactivate