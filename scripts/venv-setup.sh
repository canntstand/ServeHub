#!/bin/bash

python -m venv .venv

source .venv/Scripts/activate

echo "alias docdev='docker compose -f docker-compose.dev.yaml'" >> .venv/Scripts/activate
echo "alias docprod='docker compose -f docker-compose.prod.yaml'" >> .venv/Scripts/activate

pip install -r requirements.txt
python.exe -m pip install --upgrade pip

deactivate