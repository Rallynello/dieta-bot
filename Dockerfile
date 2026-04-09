FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dieta_bot.py .
COPY run.py .
COPY menu_settimanale.json .
COPY frasimotivazionali.txt .
COPY ingredienti_definitivi.json .
COPY web_app/ ./web_app/

EXPOSE 8000

CMD ["python3", "run.py"]
