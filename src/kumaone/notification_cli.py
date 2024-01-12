#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""monitor module for kumaone"""
import sys

# Import builtin python libraries
from pathlib import Path
from typing import Optional

# Import external python libraries
from rich.console import Console
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated
import typer

# Import custom (local) python packages
from .configs import check_config
from .connection import connect_login, disconnect
from .notifications import list_notifications
from src.kumaone.utils import _check_data_path, log_manager, _mutual_exclusivity_check

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="list", help="List all uptime kuma notification processes.")
def notification_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    List all uptime kuma notification

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_notifications(verbose=verbose, logger=logger)


@app.callback()
def notification_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone notification process manager. An uptime kuma notification processes manager wrapper.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
