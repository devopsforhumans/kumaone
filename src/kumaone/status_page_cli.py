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
from .monitors import _check_monitor_data_path, add_monitor, delete_monitor, list_monitors
from src.kumaone.utils import log_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="add", help="Add one or more uptime kuma status page(s).")
def status_page_add(
    monitors: Annotated[Optional[Path], typer.Option(..., "--monitors", "-m", help="Monitor(s) data.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Add one or more uptime kuma status page(s).

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    # monitor_file_paths = _check_monitor_data_path(data_path=monitors, logger=logger)
    # add_monitor(monitor_data_files=monitor_file_paths, logger=logger)
    disconnect()


@app.command(name="delete", help="Delete one or more uptime kuma status page(s).")
def status_page_delete(
    monitors: Annotated[Optional[Path], typer.Option(..., "--monitors", "-m", help="Monitor(s) data.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Delete one or more uptime kuma status page(s).

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    # monitor_file_paths = _check_monitor_data_path(data_path=monitors, logger=logger)
    # delete_monitor(monitor_data_files=monitor_file_paths, logger=logger)
    disconnect()


@app.command(name="list", help="List all uptime kuma status pages.")
def status_page_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    groups: Annotated[bool, typer.Option(help="Show only monitoring groups.")] = False,
    processes: Annotated[bool, typer.Option(help="Show only monitoring processes.")] = False,
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Lists all uptime kuma status pages.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    # list_monitors(show_groups=groups, show_processes=processes, verbose=verbose, logger=logger)
    disconnect()


@app.callback()
def status_page_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone status page manager. An uptime kuma status page manager wrapper.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
