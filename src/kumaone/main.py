#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for kumaone"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
from rich.console import Console
from rich import print
import typer
from typing_extensions import Annotated

# Import custom (local) python packages
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


@app.callback()
def mission_control(
    debug: Annotated[
        bool, typer.Option(help="Turn on Debug mode.", is_eager=True)
    ] = False
):
    """
    Mission control for kumaone, an uptime kuma helper python package.
    """

    if debug:
        state["debug"] = True


if __name__ == "__main__":
    app()
