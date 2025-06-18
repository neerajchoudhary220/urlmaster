import typer
from urlmaster import runner
import json
from pathlib import Path
import os
__app_name__ = "urlmaster"
__version__ = "1.0.0"

app = typer.Typer(
    help="📦 URL Master CLI — Manage FastAPI + frontend services",
    add_completion=False
)

def addParentDirectory():
    file_path = 'data.json'
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
    """\033[92m

    👋 Welcome to URL Master CLI!

    Use this tool to run or install FastAPI + frontend services as a system service.
    \033[0m"""
    if version:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

    typer.echo("\033[92m🙏 Welcome to URL Master CLI!\033[0m")
    typer.echo("\033[92m📦 A tool to manage your Laravel Project With Git Branch to share different URL\033[0m")
    typer.echo("ℹ️  Use '--help' to see the full command list.")

@app.command()
def install_service():
    """Install URL Master as a background service"""
    runner.install_service()

@app.command()
def neeraj():
    """Test command"""
    print("✅ Working!")

@app.command()
def start():
    """Start URl Master"""
    addParentDirectory()
    runner.run_fastapi()
    runner.run_frontend()
    runner.open_browser()

if __name__ == "__main__":
    app()
