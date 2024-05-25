#!/usr/bin/env python3


"""Notification module for kumaone"""

# Import builtin python libraries
from pathlib import Path
from typing import Optional

# Import external python libraries
from rich.console import Console
import typer
from typing_extensions import Annotated

# Import custom (local) python packages
from src.kumaone.configs import check_config
from src.kumaone.connection import connect_login, disconnect
from src.kumaone.notifications import add_notification, delete_notification, list_notifications, list_notification_providers, list_notification_provider_args
from src.kumaone.utils import log_manager, _mutual_exclusivity_check

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="add", help="Add a new notification provider.")
def notification_add(
    notifications: Annotated[
        Optional[Path],
        typer.Option(..., "--notifications", "-n", help="Notification(s) data."),
    ] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    interactive: Annotated[bool, typer.Option(help="Add notification interactively.")] = False,
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Add a new notification provider.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    if interactive and notifications:
        raise typer.BadParameter("Only one parameter is allowed.")

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if interactive:
        add_notification(interactive=interactive, verbose=verbose, logger=logger)
    elif notifications:
        add_notification(notifications_file_path=notifications, interactive=interactive, verbose=verbose, logger=logger)
    disconnect()


@app.command(name="list", help="List all uptime kuma notification providers.")
def notification_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    List all uptime kuma notification providers.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_notifications(verbose=verbose, logger=logger)
    disconnect()


@app.command(name="show", help="Show details of an uptime kuma notification provider.")
def notification_show(
    notification_title: Annotated[
        str,
        typer.Option(
            ..., "--title", "-t", help="Uptime kuma notification name.", callback=_mutual_exclusivity_check(size=2)
        ),
    ] = None,
    notification_id: Annotated[
        int,
        typer.Option(
            ..., "--id", "-i", help="Uptime kuma notification id.", callback=_mutual_exclusivity_check(size=2)
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    List all uptime kuma notification provider.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    if notification_title is None and notification_id is None:
        raise typer.BadParameter("At least on of '--name' / '-n' or '--id' / '-i' parameter is required.")
    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_notifications(
        verbose=verbose, notification_title=notification_title, notification_id=notification_id, logger=logger
    )
    disconnect()


@app.command(name="providers", help="Show all supported uptime kuma notification providers.")
def notification_list_providers(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    List all uptime kuma notification provider.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_notification_providers(verbose=verbose, logger=logger)
    disconnect()


@app.command(name="provider-args", help="Show all arguments of an uptime kuma notification provider by notification type.")
def notification_show_args(
    notificaton_type: Annotated[
        str,
        typer.Option(
            ..., "--type", "-t", help="Uptime kuma notification type.", callback=_mutual_exclusivity_check(size=2)
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    List all uptime kuma notification provider.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    if notificaton_type is None:
        raise typer.BadParameter("Notification type '--type' / '-n' parameter is required.")
    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    list_notification_provider_args(
        verbose=verbose, notification_type=notificaton_type, logger=logger
    )
    disconnect()


@app.command(name="delete", help="Delete a notification provider.")
def notification_delete(
    notifications: Annotated[
        Optional[Path],
        typer.Option(..., "--notifications", "-n", help="Notification(s) data."),
    ] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    notification_title: Annotated[
        str, typer.Option(..., "--title", "-t", help="Notification title (case sensitive).")
    ] = None,
    verbose: Annotated[bool, typer.Option(help="Show verbose output.")] = False,
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Delete a notification provider.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    if notification_title and notifications:
        raise typer.BadParameter(message="Only one parameter is allowed.")
    if notification_title is None and notifications is None:
        raise typer.BadParameter(message="At least one of '--notifications' / '--name' parameter is required.")

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if notification_title:
        delete_notification(notification_title=notification_title, verbose=verbose, logger=logger)
    elif notifications:
        delete_notification(
            notifications_file_path=notifications, notification_title=notification_title, verbose=verbose, logger=logger
        )
    disconnect()


@app.callback()
def notification_mission_control(log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET"):
    """
    Kumaone notification process manager. An uptime kuma notification processes manager wrapper.
    """

    if log_level:
        state["log_level"] = log_level


if __name__ == "__main__":
    app()
