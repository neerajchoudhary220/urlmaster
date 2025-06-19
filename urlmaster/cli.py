import typer
import json
from pathlib import Path
import os

from urlmaster import runner
import importlib.resources as resources
from urlmaster.services import cloudflared

BASE_DIR = Path(resources.files("urlmaster"))
data_file = BASE_DIR/"data.json"


__app_name__ = "urlmaster"
__version__ = "1.0.0"
ASCII_LOGO = r"""██╗   ██╗██████╗ ██╗           ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
██║   ██║██╔══██╗██║           ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║   ██║██████╔╝██║     █████╗██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
██║   ██║██╔══██╗██║     ╚════╝██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║███████╗      ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║ 
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
        parent_dir = input("Enter Parent Directory Path:\n").strip()

        if not parent_dir:
            print("\033[91m❌ Directory can't be empty\033[0m")
            return

        if not Path(parent_dir).exists():
            print(f"❌ This directory '{parent_dir}' does not exist!")
            return

        data = {'parent_directory': parent_dir}

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            print(f"✅ Data saved to {file_path}")
   
        
        
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
    
    


@app.command()
# def install_service():
#     """Install URL Master as a background service"""
#     typer.secho("🔓 Hacker Mode Activated", fg=typer.colors.GREEN, bold=True)
#     typer.secho("⚠️ Access Denied", fg=typer.colors.RED, bold=True)
#     typer.secho("💡 Tip: Use --help for options", fg=typer.colors.YELLOW)
#     runner.install_service()

@app.command()
def neeraj():
    """Test command"""
    typer.echo("✅ Working!")



@app.command()
def start():
    """Start URL Master"""
    typer.secho(" Please follow below URL to manage URL-MASTER", fg=typer.colors.GREEN, bold=True)
    addParentDirectory()
    runner.run_fastapi()
    runner.run_frontend()
    runner.open_browser()

@app.command()
def stop():
    """Stop All tunnel and service"""
    cloudflared.kill_all_tunnels()
    
if __name__ == "__main__":
    app()
