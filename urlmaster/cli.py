import typer
from urlmaster import runner

app = typer.Typer()

@app.command()

def install_service():
    """Install URL Master as a background service"""
    runner.install_service()
@app.command()
def neeraj():
    print("wporking")
@app.command()
def run():
    """Start URL Master"""
    runner.run_fastapi()
    runner.run_frontend()
    runner.open_browser()
if __name__ == "__main__":
    app()
