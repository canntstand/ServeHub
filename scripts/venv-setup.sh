#!/bin/bash

# Запускать из корневой директории проекта

if [ -d ".venv" ]; then
    rm -rf .venv
fi

python -m venv .venv

if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin" ]]; then
    source .venv/bin/activate
    echo "alias docdev='docker compose -f docker-compose.dev.yaml'" >> .venv/bin/activate
    echo "alias docprod='docker compose -f docker-compose.prod.yaml'" >> .venv/bin/activate
else
    source .venv/Scripts/activate
    echo "alias docdev='docker compose -f docker-compose.dev.yaml'" >> .venv/Scripts/activate
    echo "alias docprod='docker compose -f docker-compose.prod.yaml'" >> .venv/Scripts/activate
fi

cd services

for service in */; do
    cd "$service"
    if [ -f "requirements.txt" ]; then
        pip install -r "requirements.txt"
    fi
    cd ..
done

cd ..
python -m pip install --upgrade pip
