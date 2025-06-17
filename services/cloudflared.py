# start_tunnel.py
import subprocess
import re
import json
import os
import signal

TUNNELS_FILE = "active_tunnels.json"

def run_cloudflared(url:str):
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(line.strip())  # Optional
        match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
        if match:
            public_url = match.group(1)
            print("\n🌐 Public Tunnel URL:", public_url)

            # ✅ Save URL and PID
            tunnel_info = {"url": public_url, "pid": process.pid,"herd_link":url}
            save_tunnel(tunnel_info)
            break

def save_tunnel(tunnel_info):
    if os.path.exists(TUNNELS_FILE):
        with open(TUNNELS_FILE, "r") as f:
            tunnels = json.load(f)
    else:
        tunnels = []

    tunnels.append(tunnel_info)

    with open(TUNNELS_FILE, "w") as f:
        json.dump(tunnels, f, indent=2)

# run_cloudflared()


def kill_tunnel_by_url(target_url):
    if not os.path.exists(TUNNELS_FILE):
        print("No active tunnels found.")
        return

    with open(TUNNELS_FILE, "r") as f:
        tunnels = json.load(f)

    updated_tunnels = []
    killed = False

    for tunnel in tunnels:
        if tunnel["url"] == target_url:
            try:
                os.kill(tunnel["pid"], signal.SIGTERM)
                print(f"✅ Killed tunnel: {tunnel['url']} (PID {tunnel['pid']})")
                killed = True
            except ProcessLookupError:
                print(f"⚠️ Process already dead for: {tunnel['url']}")
        else:
            updated_tunnels.append(tunnel)

    # Update file with remaining tunnels
    with open(TUNNELS_FILE, "w") as f:
        json.dump(updated_tunnels, f, indent=2)

    if not killed:
        print("❌ No tunnel found with the specified URL.")

# Example usage
# kill_tunnel_by_url("https://proposals-recorded-guest-sequence.trycloudflare.com")
