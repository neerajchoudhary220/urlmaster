import subprocess
import random
import re
import sys

def normalize_for_subdomain(name):
    name = name.replace('.test', '')
    return name


# === USER INPUT ===
herd_site = input("🧠 Enter Herd site (like sembark-apis.test): ").strip()

if not herd_site.endswith('.test'):
    print("❌ Please enter a valid .test domain")
    sys.exit(1)

herd_clean = normalize_for_subdomain(herd_site)
local_port = 80
remote_port = random.randint(3000, 9999)
ssh_user = "tunneluser"
ssh_host = "neerajchoudhary.fun"
ssh_key = "~/.ssh/id_tunnel"
public_subdomain = f"{herd_clean}-{remote_port}"  # use dash
public_url = f"https://{public_subdomain}.{ssh_host}"


# === TUNNEL COMMAND ===
ssh_command = [
    "ssh",
    "-i", ssh_key,
    "-N",
    "-R", f"{remote_port}:127.0.0.1:{local_port}",
    f"{ssh_user}@{ssh_host}"
]

# === INFO ===
print("\n🚀 Creating tunnel...")
print(f"🔐 Herd site:        {herd_site}")
print(f"📦 Local port:       {local_port}")
print(f"🔁 Public port:      {remote_port}")
print(f"🌍 Public URL:       {public_url}")
print(f"🧠 Laravel will see: Host: {herd_site}")
print("📡 Ctrl+C to stop\n")

# === RUN ===
try:
#    processs=  subprocess.run(ssh_command)
    process = subprocess.Popen(ssh_command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    print(process.pid)
except KeyboardInterrupt:
    print("\n🛑 Tunnel closed.")
