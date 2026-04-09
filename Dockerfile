FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dieta-bot/dieta_bot.py .
COPY dieta-bot/menu_settimanale.json .
COPY dieta-bot/frasimotivazionali.txt .
COPY ingredienti_definitivi.json .

CMD ["python3", "dieta_bot.py"]
