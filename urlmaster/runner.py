import os
import subprocess
import platform
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTALL_DIR = BASE_DIR / "install"

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
