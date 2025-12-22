FROM python:3.14-slim-bookworm

WORKDIR /notes-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .