FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dieta_bot.py .
COPY menu_settimanale.json .
COPY frasimotivazionali.txt .

CMD ["python3", "dieta_bot.py"]
