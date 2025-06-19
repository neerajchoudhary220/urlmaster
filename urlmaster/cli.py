import typer
import json
from pathlib import Path
import random

from urlmaster import runner
import importlib.resources as resources
from urlmaster.services import cloudflared

import getpass

def getusername():
    return getpass.getuser()

BASE_DIR = Path(resources.files("urlmaster"))
data_file = BASE_DIR/"data.json"


__app_name__ = "urlmaster"
__version__ = "1.0.0"
ASCII_LOGO = r"""  _   _   ___   _            __  __     _     ___   _____   ___   ___ 
 | | | | | _ \ | |     ___  |  \/  |   /_\   / __| |_   _| | __| | _ \
 | |_| | |   / | |__  |___| | |\/| |  / _ \  \__ \   | |   | _|  |   /
  \___/  |_|_\ |____|       |_|  |_| /_/ \_\ |___/   |_|   |___| |_|_\
                                                                      """
app = typer.Typer(
    help="📦 URL Master CLI — Manage FastAPI + frontend services",
    add_completion=False
)


    
def addParentDirectory():
    file_path = data_file
    file = Path(file_path)

    # Check if file doesn't exist or is empty
    if not file.exists() or file.stat().st_size == 0:
        typer.secho(" 🗂️ Enter Parent Directory Path", fg=typer.colors.GREEN)
        parent_dir = input("\n").strip()
        if not parent_dir:
            typer.secho(f" ⚠️ This directory '{parent_dir}' does not exist!", fg=typer.colors.RED)
            return

        if not Path(parent_dir).exists():
            typer.secho(f" ⚠️ This directory '{parent_dir}' does not exist!", fg=typer.colors.RED)
            return 

        data = {'parent_directory': parent_dir}

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            typer.secho(f"✅ Data saved to {file_path}", fg=typer.colors.GREEN)
   
        
        
@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        None, "--version", "-v", help="Show the URL Master version and exit"
    )
):
    if version:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    typer.secho(ASCII_LOGO, fg=typer.colors.CYAN)
    typer.secho(f"Welcome {getusername()}",fg=typer.colors.GREEN,bold=True)
    
    


# @app.command()
# def install_service():
#     """Install URL Master as a background service"""
#     typer.secho("🔓 Hacker Mode Activated", fg=typer.colors.GREEN, bold=True)
#     typer.secho("⚠️ Access Denied", fg=typer.colors.RED, bold=True)
#     typer.secho("💡 Tip: Use --help for options", fg=typer.colors.YELLOW)
#     runner.install_service()

@app.command()
def test():
    """Test command"""
    greetings = {
    "english": ["Hello", "Hi", "Hey", "Greetings", "Good day"],
    "hindi": ["Namaste", "Namaskar", "Pranam"],
    "fun": ["Yo!", "What's up?", "Howdy!", "Sup?", "Heya!"]
}

    # Pick a random language
    lang = random.choice(list(greetings.keys()))

    # Pick a random greeting from that language
    greeting = random.choice(greetings[lang])

    # print(f"{greeting}, Neeraj! ({lang})")
    typer.secho(f"✅ ", fg=typer.colors.GREEN)



@app.command()
def start():
    """Start URL Master"""
    addParentDirectory()
    runner.run_fastapi()
    typer.secho(" Please follow below URL to manage URL-MASTER", fg=typer.colors.GREEN, bold=True)
    runner.run_frontend()
    runner.open_browser()

@app.command()
def stop():
    """Stop All tunnel and service"""
    cloudflared.kill_all_tunnels()
    
if __name__ == "__main__":
    app()
