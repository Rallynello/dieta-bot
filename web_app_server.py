#!/usr/bin/env python3
"""
Simple HTTP server for Telegram Mini App
Serve the web app files at /web_app
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve from web_app directory
        if path.startswith('/web_app'):
            path = path[8:]  # Remove /web_app prefix
        
        # Default to index.html for root
        if path == '/' or path == '':
            path = '/index.html'
        
        return super().translate_path(path)
    
    def end_headers(self):
        # Add CORS headers for Telegram
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    # Change to web_app directory
    os.chdir(Path(__file__).parent / 'web_app')
    
    server = HTTPServer(('0.0.0.0', 8000), MyHTTPRequestHandler)
    print('Mini App server started at http://0.0.0.0:8000')
    server.serve_forever()
