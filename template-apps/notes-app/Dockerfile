FROM python:3.14-slim-bookworm

WORKDIR /notes-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--port", "8000" ]