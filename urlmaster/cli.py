import typer
from urlmaster import runner

app = typer.Typer()

@app.command()
def install_service():
    """Install URL Master as a background service"""
    runner.install_service()

if __name__ == "__main__":
    app()
