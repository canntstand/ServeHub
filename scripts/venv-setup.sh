#!/bin/bash

if [ -d ".venv" ]; then
    .venv/Scripts/activate
    deactivate
    rm -rf .venv
fi

python -m venv .venv

source .venv/Scripts/activate

echo "alias docdev='docker compose -f docker-compose.dev.yaml'" >> .venv/Scripts/activate
echo "alias docprod='docker compose -f docker-compose.prod.yaml'" >> .venv/Scripts/activate

cd services

for service in */; do
    cd "$service"
    if [ -f "requirements.txt" ]; then
        pip install -r "requirements.txt"
    fi
    cd ..
done

python.exe -m pip install --upgrade pip

deactivate