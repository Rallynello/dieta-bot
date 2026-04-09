#!/usr/bin/env python3
"""
Runner per lanciare sia il bot Telegram che il server Flask per la mini app
"""
import asyncio
import threading
from pathlib import Path
from flask import Flask, send_from_directory
import logging

# Import del bot
from dieta_bot import main as bot_main

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea l'app Flask
app = Flask(__name__)
web_app_dir = Path(__file__).parent / 'web_app'

@app.route('/web_app')
def web_app_root():
    """Serve index.html per la mini app"""
    return send_from_directory(web_app_dir, 'index.html')

@app.route('/web_app/<path:path>')
def web_app_static(path):
    """Serve file statici della mini app"""
    return send_from_directory(web_app_dir, path)

@app.route('/health')
def health():
    """Health check per Railway"""
    return {'status': 'ok'}, 200

def run_flask():
    """Lancia il server Flask"""
    logger.info("Starting Flask server on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=False)

def run_bot():
    """Lancia il bot Telegram"""
    logger.info("Starting Telegram bot...")
    asyncio.run(bot_main())

if __name__ == '__main__':
    # Lancia Flask in un thread separato
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask thread started")
    
    # Lancia il bot nel thread principale
    run_bot()
