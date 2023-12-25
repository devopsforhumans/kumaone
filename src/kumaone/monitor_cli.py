#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""monitor module for kumaone"""

# Import builtin python libraries
from pathlib import Path
from typing import Optional

# Import external python libraries
from rich.console import Console
from typing_extensions import Annotated
import typer

# Import custom (local) python packages
from .configs import check_config
from .connection import connect_login, disconnect
from .monitors import _check_monitor_data_path, list_monitors
from src.kumaone.utils import log_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="add", help="Add one or more monitor(s).")
def monitor_add(
    monitors: Annotated[Optional[Path], typer.Option(..., "--monitors", "-m", help="Monitor(s) data.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Adds uptime kuma monitor(s)

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    # config_data = check_config(config_path=config_file, logger=logger)
    # connect_login(config_data=config_data)
    _check_monitor_data_path(data_path=monitors, logger=logger)
    # disconnect()


@app.command(name="list", help="List all monitor groups and processes.")
def monitor_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    groups: Annotated[bool, typer.Option(help="Show only monitoring groups.")] = False,
    processes: Annotated[bool, typer.Option(help="Show only monitoring processes.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Lists all monitor groups and processes

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_monitors(show_groups=groups, show_processes=processes, logger=logger)
    disconnect()


@app.callback()
def monitor_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone monitor manager.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
