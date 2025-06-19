import socket
try:
    print("Resolving test domain...")
    ip = socket.gethostbyname("trycloudflare.com")
    print(f"✅ DNS works: {ip}")
except Exception as e:
    print(f"❌ DNS failed: {e}")
