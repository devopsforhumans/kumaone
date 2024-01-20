#!/usr/bin/env python3


"""monitor module for kumaone"""

# Import external python libraries
from rich.console import Console
import typer
from typing_extensions import Annotated

# Import custom (local) python packages
from src.kumaone.configs import check_config, create_config, delete_config

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="show", help="Show kumaone config.")
def config_show(
    config_path: Annotated[
        str, typer.Option(..., "--config", "-c", help="Custom full (with extension) location for config file.")
    ] = "",
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Show kumaone config for uptime kuma server.

    :return: (None) On screen output.
    """

    if log_level != "NOTSET":
        state["log_level"] = log_level

    check_config(config_path=config_path, log_level=log_level)


@app.command(name="create", help="Create kumaone config.")
def config_create(
    config_path: Annotated[
        str, typer.Option(..., "--config", "-c", help="Custom full (with extension) location for config file.")
    ] = "",
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Create kumaone config for uptime kuma server.

    :return: (None) On screen output.
    """

    if log_level != "NOTSET":
        state["log_level"] = log_level

    create_config(config_path=config_path, log_level=log_level)


@app.command(name="delete", help="Delete kumaone config.")
def config_delete(
    config_path: Annotated[
        str, typer.Option(..., "--config", "-c", help="Custom full (with extension) location for config file.")
    ] = "",
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Delete kumaone config for uptime kuma server.

    :return: (None) On screen output.
    """

    if log_level != "NOTSET":
        state["log_level"] = log_level

    delete_config(config_path=config_path, log_level=log_level)


# @app.command(name="edit", help="Edit kumaone config.")
# def config_edit(
#     config_path: Annotated[
#         str, typer.Option(..., "--config", "-c", help="Custom full (with extension) location for config file.")
#     ] = "",
#     log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
# ):
#     """
#     Edit kumaone config for uptime kuma server.
#
#     :return: (None) On screen output.
#     """
#
#     if log_level != "NOTSET":
#         state["log_level"] = log_level
#
#     edit_config(config_path=config_path, log_level=log_level)


@app.callback()
def config_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone configuration manager.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
