FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir flask

COPY web_app/ ./web_app/
COPY app_only.py .

EXPOSE 8000

CMD ["python3", "app_only.py"]

