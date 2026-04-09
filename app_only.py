#!/usr/bin/env python3
"""
Minimal Flask server - just for testing
"""
from flask import Flask, send_from_directory, jsonify
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
web_app_dir = Path(__file__).parent / 'web_app'

@app.route('/')
def root():
    logger.info("Serving /")
    return send_from_directory(web_app_dir, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    logger.info(f"Serving {path}")
    return send_from_directory(web_app_dir, path)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Flask is running'}), 200

if __name__ == '__main__':
    logger.info(f"Starting Flask on 0.0.0.0:8000, serving from {web_app_dir}")
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
