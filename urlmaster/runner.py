import os
import subprocess
import platform
from pathlib import Path
import webbrowser
import socket
BASE_DIR = Path(__file__).resolve().parent.parent
INSTALL_DIR = BASE_DIR / "install"
STATIC_DIR = BASE_DIR / "public"
MAIN_APP_PATH = BASE_DIR / "main.py"
def install_service():
    system = platform.system()
    cwd = str(BASE_DIR)
    user = os.getenv("USER") or os.getenv("USERNAME")

    print(f"Installing service for {system}...")

    if system == "Linux":
        template_path = INSTALL_DIR / "urlmaster_ubuntu.service.template"
        output_path = INSTALL_DIR / "urlmaster_ubuntu.service"

        with open(template_path, "r") as f:
            content = f.read()

        content = content.replace("{{WORKING_DIR}}", cwd).replace("{{USER}}", user)

        with open(output_path, "w") as f:
            f.write(content)

        # Install systemd service
        subprocess.run(["sudo", "cp", str(output_path), "/etc/systemd/system/urlmaster.service"])
        subprocess.run(["sudo", "systemctl", "daemon-reexec"])
        subprocess.run(["sudo", "systemctl", "enable", "urlmaster"])
        subprocess.run(["sudo", "systemctl", "start", "urlmaster"])
        print("✅ Linux service installed and started.")

    elif system == "Darwin":  # macOS
        template_path = INSTALL_DIR / "urlmaster_mac.plist.template"
        output_path = Path.home() / "Library/LaunchAgents/com.neeraj.urlmaster.plist"

        with open(template_path, "r") as f:
            content = f.read()

        content = content.replace("{{WORKING_DIR}}", cwd)

        with open(output_path, "w") as f:
            f.write(content)

        subprocess.run(["launchctl", "load", str(output_path)])
        print("✅ macOS LaunchAgent installed and loaded.")

    elif system == "Windows":
        bat_path = INSTALL_DIR / "urlmaster_windows.bat"
        subprocess.run([str(bat_path)], shell=True)
        print("✅ Windows service launched via .bat file.")

    else:
        print("❌ Unsupported operating system.")


def is_port_in_use(port: int) -> bool:
    """Check if a given port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def run_fastapi():
    port = 8090
    if is_port_in_use(port):
        print(f"⚠️ FastAPI already running on http://127.0.0.1:{port}")
        return

    print(f"🚀 Starting FastAPI on http://127.0.0.1:{port} ...")
    subprocess.Popen([
        "uvicorn", 
        "main:app",  
        "--host", "127.0.0.1",
        "--port", str(port),
        "--reload"
    ], cwd=BASE_DIR)
    print("✅ FastAPI started in background.")
    
def run_frontend():
    subprocess.Popen(["python3", "-m", "http.server", "8080"], cwd=STATIC_DIR)

def open_browser():
    webbrowser.open("http://localhost:8080")