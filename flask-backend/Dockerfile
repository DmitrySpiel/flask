# Dockerfile
FROM --platform=linux/amd64 python:3.9-slim as build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]