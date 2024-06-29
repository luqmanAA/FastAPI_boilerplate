from subprocess import run as sub_runner

from typer import Typer, prompt
from uvicorn import run


from src.management.commands.createsuperuser import createsuperuser as _createsuper_user

app = Typer()


@app.command()
def createsuperuser():
    """Create a superuser."""
    _createsuper_user()


@app.command()
def startserver():
    """Start the FastAPI server."""
    uvicorn_options = {
        "app": "src.main:app",
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
    }
    run(**uvicorn_options)


@app.command()
def automigration():
    migration_message = prompt(
        "Enter migration message", default="Auto-generated migration"
    )

    sub_runner(["alembic", "revision", "--autogenerate",
               "-m", migration_message])


@app.command()
def createmigration():
    migration_message = prompt("Enter migration message", default="")

    sub_runner(["alembic", "revision", "-m", migration_message])


@app.command()
def runmigration():
    sub_runner(["alembic", "upgrade", "head"])


@app.command()
def runtest():
    """Run tests."""


if __name__ == "__main__":
    app()
