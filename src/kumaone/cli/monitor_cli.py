#!/usr/bin/env python3


"""monitor module for kumaone"""

# Import builtin python libraries
from pathlib import Path
from typing import Optional

# Import external python libraries
from rich.console import Console
from typing_extensions import Annotated
import typer

# Import custom (local) python packages
from src.kumaone.configs import check_config
from src.kumaone.connection import connect_login, disconnect
from src.kumaone.monitors import add_monitor, delete_monitor, list_monitors
from src.kumaone.utils import _check_data_path, log_manager, _mutual_exclusivity_check

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

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    monitor_file_paths = _check_data_path(data_path=monitors, logger=logger, key_to_check_for="monitors")
    add_monitor(monitor_data_files=monitor_file_paths, logger=logger)
    disconnect()


@app.command(name="delete", help="Delete one or more monitor(s).")
def monitor_delete(
    monitors: Annotated[
        Optional[Path],
        typer.Option(..., "--monitors", "-m", help="Monitor(s) data.", callback=_mutual_exclusivity_check(size=2)),
    ] = None,
    monitor_name: Annotated[
        str,
        typer.Option(
            ..., "--name", "-n", help="Name of the monitor to delete.", callback=_mutual_exclusivity_check(size=2)
        ),
    ] = None,
    monitor_id: Annotated[int, typer.Option(..., "--id", "-i", help="Uptime kuma monitor ID.")] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Deletes uptime kuma monitor(s).

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if monitors is None and monitor_name is None and monitor_id is None:
        raise typer.BadParameter(
            "At least one of the parameter '--monitor'/'-m' OR '--name'/'-n' OR '--id'/'-i' is required."
        )
    if monitor_name is not None and monitor_id is not None:
        raise typer.BadParameter(message="Only one of '--name' and '--id' parameter is allowed.")
    if monitors:
        monitor_file_paths = _check_data_path(data_path=monitors, logger=logger, key_to_check_for="monitors")
        delete_monitor(monitor_data_files=monitor_file_paths, logger=logger)
    elif monitor_id:
        delete_monitor(monitor_id=monitor_id, logger=logger)
    elif monitor_name:
        delete_monitor(monitor_name=monitor_name, logger=logger)
    disconnect()


@app.command(name="list", help="List all monitor groups and processes.")
def monitor_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    groups: Annotated[bool, typer.Option(help="Show only monitoring groups.")] = False,
    processes: Annotated[bool, typer.Option(help="Show only monitoring processes.")] = False,
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Lists all monitor groups and processes

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    if groups and processes:
        raise typer.BadParameter(message="'--groups' and '--processes' can not be used together.")
    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_monitors(show_groups=groups, show_processes=processes, verbose=verbose, logger=logger)
    disconnect()


@app.command(name="show", help="Show details of a single process monitor by ID.")
def monitor_show(
    monitor_id: Annotated[int, typer.Option(..., "--id", "-i", help="Uptime kuma monitor ID.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
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
    list_monitors(monitor_id=monitor_id, logger=logger)
    disconnect()


@app.callback()
def monitor_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone monitor manager. An uptime kuma monitor group and process monitor manager wrapper.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
