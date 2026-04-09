#!/usr/bin/env python3
"""
Runner per lanciare sia il bot Telegram che il server Flask per la mini app
"""
import threading
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
import logging
import os

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Stato globale
bot_status = {'running': False, 'error': None}

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
    logger.info(f"Richiesta file: {path}")
    return send_from_directory(web_app_dir, path)

@app.route('/health')
def health():
    """Health check per Railway"""
    return jsonify({'status': 'ok', 'bot': bot_status}), 200

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
    global bot_status
    try:
        # Import qui per evitare problemi di circular import
        from dieta_bot import main as bot_main
        
        # Controlla se TOKEN esiste
        TOKEN = os.getenv("TOKEN")
        if not TOKEN:
            logger.warning("TOKEN env variable not set - bot will not run but Flask will still serve web_app")
            bot_status['error'] = 'TOKEN not set'
            bot_status['running'] = False
            return
        
        logger.info("✅ TOKEN found, starting bot polling...")
        bot_status['running'] = True
        bot_main()
    except KeyboardInterrupt:
        logger.info("Bot interrupted")
        bot_status['running'] = False
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
        bot_status['error'] = str(e)
        bot_status['running'] = False

if __name__ == '__main__':
    # Lancia il bot in un thread daemon separato
    logger.info("=" * 60)
    logger.info("STARTING DIETA BOT WITH FLASK MINI APP SERVER")
    logger.info("=" * 60)
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("✅ Bot thread started (daemon)")
    logger.info("Waiting for bot to initialize...")
    
    import time
    time.sleep(2)
    logger.info("=" * 60)
    
    # Lancia Flask nel main thread (questo blocca, come vuole Railway)
    logger.info("Starting Flask server on port 8000...")
    logger.info("Flask will serve files from: " + str(web_app_dir))
    logger.info("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Flask error: {e}")
        import traceback
        traceback.print_exc()


