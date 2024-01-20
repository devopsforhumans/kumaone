#!/usr/bin/env python3

"""Main module for kumaone"""

# Import builtin python libraries

# Import external python libraries
from rich.console import Console
import typer
from typing_extensions import Annotated
from typing import Optional

# Import custom (local) python packages
from src.kumaone.cli import config_cli, monitor_cli, notification_cli, status_page_cli
from src.kumaone.utils import app_info, version_callback

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
app.add_typer(monitor_cli.app, name="monitor")
app.add_typer(config_cli.app, name="config")
app.add_typer(status_page_cli.app, name="status-page")
app.add_typer(notification_cli.app, name="notification")
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="info", help="Show information about kumaone application.")
def info(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Show application information

    :return: (None) Information on screen.
    """

    if log_level:
        state["log_level"] = log_level
    app_info(log_level=log_level)


@app.callback()
def mission_control(
    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback, is_eager=True)] = None,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Mission control for kumaone, an uptime kuma helper python package.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
