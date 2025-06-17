# start_tunnel.py
import subprocess
import re
import json
import os
import signal
from fastapi import HTTPException

TUNNELS_FILE = "active_tunnels.json"

def get_cloudflared_public_url(url:str):
    domain = re.sub(r'^https?://', '', url).strip('/')
    print(f"domain is {domain}")
    # Run cloudflared tunnel command
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://127.0.0.1:80", "--http-host-header", domain],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
        if match:
            public_url = match.group(1)
            # print("\n🌐 Public Tunnel URL:", public_url)

            # ✅ Save URL and PID
            tunnel_info = {"public_url": public_url, "pid": process.pid,"herd_link":url}
            save_tunnel(tunnel_info)
            break

def save_tunnel(tunnel_info: dict) -> str:
    """
    Saves or updates a tunnel entry in the JSON file based on herd_link.

    Args:
        tunnel_info (dict): Dictionary with keys: public_url, pid, herd_link.

    Returns:
        str: The saved or updated public_url.
    """
    if os.path.exists(TUNNELS_FILE):
        with open(TUNNELS_FILE, "r") as f:
            try:
                tunnels = json.load(f)
            except json.JSONDecodeError:
                tunnels = []
    else:
        tunnels = []

    updated = False
    for idx, tunnel in enumerate(tunnels):
        if tunnel.get("herd_link") == tunnel_info["herd_link"]:
            kill_tunnel_by_url(tunnel.get('herd_link'))#Kill Old Cloudflared tunnel link before update new
            tunnels[idx] = tunnel_info
            updated = True
            break

    if not updated:
        tunnels.append(tunnel_info)

    with open(TUNNELS_FILE, "w") as f:
        json.dump(tunnels, f, indent=2)

    return tunnel_info['public_url']

# def save_tunnel(tunnel_info):
#     if os.path.exists(TUNNELS_FILE):
#         with open(TUNNELS_FILE, "r") as f:
#             tunnels = json.load(f)
#     else:
#         tunnels = []

#     tunnels.append(tunnel_info)

#     with open(TUNNELS_FILE, "w") as f:
#         json.dump(tunnels, f, indent=2)
    
#     return tunnel_info['public_url']



# def kill_tunnel_by_url(herd_link:str):
#     if not os.path.exists(TUNNELS_FILE):
#         print("No active tunnels found.")
#         return

#     with open(TUNNELS_FILE, "r") as f:
#         tunnels = json.load(f)

#     updated_tunnels = []
#     killed = False

#     for tunnel in tunnels:
#         if tunnel["herd_link"] == herd_link:
#             try:
#                 os.kill(tunnel["pid"], signal.SIGTERM)
#                 print(f"✅ Killed tunnel: {tunnel['herd_link']} (PID {tunnel['pid']})")
#                 killed = True
#             except ProcessLookupError:
#                 print(f"⚠️ Process already dead for: {tunnel['url']}")
#         else:
#             updated_tunnels.append(tunnel)

#     # Update file with remaining tunnels
#     with open(TUNNELS_FILE, "w") as f:
#         json.dump(updated_tunnels, f, indent=2)

#     if not killed:
#         print("❌ No tunnel found with the specified URL.")




def kill_tunnel_by_url(herd_link: str):
    
    if not os.path.exists(TUNNELS_FILE):
        print("No active tunnels found.")
        return

    with open(TUNNELS_FILE, "r") as f:
        try:
            tunnels = json.load(f)
        except json.JSONDecodeError:
            print("Tunnel file is corrupted or empty.")
            return

    updated_tunnels = []
    killed = False

    for tunnel in tunnels:
        if tunnel["herd_link"] == herd_link:
            try:
                os.kill(tunnel["pid"], signal.SIGTERM)
                killed = True
            except ProcessLookupError:
                HTTPException(400,detail=f"⚠️ Process already dead for: {tunnel['herd_link']}")
        else:
            updated_tunnels.append(tunnel)

    # Always write updated list back
    with open(TUNNELS_FILE, "w") as f:
        json.dump(updated_tunnels, f, indent=2)

    if not killed:
        raise HTTPException(400,detail="Not tunnel active right now")
    return True

def get_tunnel(herd_link: str, file_path: str = 'active_tunnels.json') -> str | None:
        if not os.path.exists(TUNNELS_FILE):
            return None
        with open(file_path, 'r') as f:
            tunnels = json.load(f)

        for tunnel in tunnels:
            if tunnel.get('herd_link') == herd_link:
                return tunnel.get('public_url')

        return None

