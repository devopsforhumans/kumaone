#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for kumaone"""

# Import builtin python libraries
from pathlib import Path

# Import external python libraries
from rich.console import Console
from rich import print
import typer
from typing import Optional
from typing_extensions import Annotated

# Import custom (local) python packages
from .config import ConfigActions, check_config, create_config, delete_config, edit_config
from .utils import app_info

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="info", help="Show information about this application.")
def info(log_level: Annotated[str, typer.Option(help="Set log level.")] = "WARNING"):
    """
    Show application information

    :return: Information on screen.
    """

    if log_level:
        state["log_level"] = log_level
    app_info(log_level=log_level)


@app.command(name="bulk_add_monitor", help="Add one or more monitor(s).")
def bulk_add_monitor(
    monitor_data: Annotated[Optional[Path], typer.Option(..., "--file", "-f", help="Monitor data file path.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = "kuma.conf",
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "WARNING",
):
    """
    Adds uptime kuma monitor(s)

    :return: (object) json object
    """

    if log_level:
        state["log_level"] = log_level

    config_data = check_config(config_path=config_file)
    print(config_data)


@app.command(name="config", help="Kumaone config handler.")
def config(
    config_path: Annotated[
        str, typer.Option(..., "--config", "-c", help="Custom full (with extension) location for config file.")
    ] = "",
    action: Annotated[
        ConfigActions, typer.Option(..., "--action", "-a", help="Perform uptime kuma config actions.")
    ] = "show",
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "WARNING",
):
    """
    Uptime kuma server config management

    :return: (None) On screen output.
    """

    if log_level:
        state["log_level"] = log_level

    if action == "show":
        check_config(config_path=config_path, log_level=log_level)
    elif action == "create":
        create_config(config_path=config_path, log_level=log_level)
    elif action == "delete":
        delete_config(config_path=config_path, log_level=log_level)
    elif action == "edit":
        edit_config(config_path=config_path, log_level=log_level)
    else:
        console.print(f":x: Not a valid action.")
        exit(1)


@app.callback()
def mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "WARNING"):
    """
    Mission control for kumaone, an uptime kuma helper python package.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
