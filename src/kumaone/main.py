#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for kumaone"""

# Import builtin python libraries
import logging
from pathlib import Path
import sys

# Import external python libraries
from rich.console import Console
from rich import print
import typer
from typing import Optional
from typing_extensions import Annotated

# Import custom (local) python packages
from .config import check_config, ConfigActions
from .utils import debug_manager, app_info

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"debug": False}
console = Console()


@app.command(name="info", help="Show information about this application.")
def info(debug: Annotated[bool, typer.Option(help="Turn on Debug mode.", is_eager=True)] = False):
    """
    Show application information

    :return: Information on screen.
    """

    if debug or state["debug"]:
        debug_manager()
    app_info()


@app.command(name="bulk_add_monitor", help="Add one or more monitor(s).")
def bulk_add_monitor(
    monitor_data: Annotated[Optional[Path], typer.Option(..., "--file", "-f", help="Monitor data file path.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = "kuma.conf",
    debug: Annotated[bool, typer.Option(help="Turn on Debug mode.", is_eager=True)] = False,
):
    """
    Adds uptime kuma monitor(s)

    :return: (object) json object
    """

    if debug or state["debug"]:
        debug_manager()

    config_data = check_config(config_path=config_file)
    print(config_data)


@app.command(name="config", help="Kumaone config handler.")
def config(
    action: Annotated[ConfigActions, typer.Option(..., "--action", "-a", help="Perform uptime kuma config actions.")] = "none",
    show: Annotated[bool, typer.Option(help="Show current uptime kuma config.")] = False,
    debug: Annotated[bool, typer.Option(help="Turn on Debug mode.", is_eager=True)] = False,
):
    """
    Uptime kuma server config management

    :return: (None) On screen output.
    """

    if debug or state["debug"]:
        log_level = "debug"
    else:
        log_level = None

    if show:
        if action != "none":
            console.print(f":x: Both 'show' and 'action' can't be used together.")
        else:
            check_config(log_level=log_level)


@app.callback()
def mission_control(debug: Annotated[bool, typer.Option(help="Turn on Debug mode.", is_eager=True)] = False):
    """
    Mission control for kumaone, an uptime kuma helper python package.
    """

    if debug:
        state["debug"] = True


if __name__ == "__main__":
    app()
