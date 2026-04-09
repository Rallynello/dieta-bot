#!/usr/bin/env python3
"""
Runner per lanciare sia il bot Telegram che il server Flask per la mini app
"""
import threading
from pathlib import Path
from flask import Flask, send_from_directory
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea l'app Flask
app = Flask(__name__)
web_app_dir = Path(__file__).parent / 'web_app'

@app.route('/')
def root():
    """Serve index.html da radice"""
    logger.info(f"Richiesta root - serve da {web_app_dir}")
    return send_from_directory(web_app_dir, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve file statici"""
    logger.info(f"Richiesta file: {path} da {web_app_dir}")
    return send_from_directory(web_app_dir, path)

@app.route('/health')
def health():
    """Health check per Railway"""
    return {'status': 'ok'}, 200

def run_flask():
    """Lancia il server Flask"""
    logger.info("Starting Flask server on port 8000...")
    try:
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Flask error: {e}")

def run_bot():
    """Lancia il bot Telegram"""
    logger.info("Starting Telegram bot...")
    try:
        # Import qui per evitare problemi di circular import
        from dieta_bot import main as bot_main
        bot_main()
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == '__main__':
    # Lancia il bot in un thread daemon separato
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started (daemon)")
    
    # Lancia Flask nel main thread (questo blocca, come vuole Railway)
    logger.info("Starting Flask server on port 8000...")
    try:
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Flask error: {e}")
        import traceback
        traceback.print_exc()


