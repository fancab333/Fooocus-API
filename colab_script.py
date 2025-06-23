import subprocess
import time
import re
import requests

# 1. Launch Fooocus API in the background
fooocus_proc = subprocess.Popen(
    ["python3", "main.py", "--port", "8888", "--host", "0.0.0.0"]
)

print("Launching LocalTunnel (random subdomain)...")
lt_process = subprocess.Popen(
    ["lt", "--port", "8888"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Wait for public URL
public_url = None
start_time = time.time()

while time.time() - start_time < 15:
    line = lt_process.stdout.readline()
    print(line.strip())
    match = re.search(r"(https://[a-z0-9-]+\.loca\.lt)", line)
    if match:
        public_url = match.group(1)
        break

if public_url:
    print("Public URL:", public_url)

    # API test: call the /v1/ping endpoint
    try:
        response = requests.get(f"{public_url}/ping")
        print("✅ API test succeeded:", response.text)
    except Exception as e:
        print("❌ API test failed:", e)
else:
    print("Failed to retrieve tunnel URL.")