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
from .status_pages import add_status_page, get_satus_page, list_status_pages
from src.kumaone.utils import _check_data_path, log_manager, _print_missing_options_panel

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

# Create typer app and turn off debug mode by default
app = typer.Typer()
state = {"log_level": "NOTSET"}
console = Console()


@app.command(name="add", help="Add one or more uptime kuma status page(s).")
def status_page_add(
    status_pages: Annotated[
        Optional[Path],
        typer.Option(..., "--pages", "-p", help="Status page(s) data. Exclusive to '--title' and '--slug'"),
    ] = None,
    title: Annotated[
        str, typer.Option(..., "--title", "-t", help="Title of the status page. '--slug' is required.")
    ] = None,
    slug: Annotated[
        str, typer.Option(..., "--slug", "-s", help="Slug of the status page. '--title' is required. ")
    ] = None,
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
    if status_pages is None and title is None and slug is None:
        _print_missing_options_panel(missing_options="'--title' / '-t' and '--slug' / '-s' OR '--pages' / '-p'")
        sys.exit(1)
    elif status_pages:
        status_page_config = "from_file"
    elif title and slug:
        status_page_config = "inline"
    elif title is None or slug is None:
        _print_missing_options_panel(missing_options="'--title' / '-t' and '--slug' / '-s'")
        exit(1)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if status_page_config == "inline":
        add_status_page(status_page_title=title, status_page_slug=slug, logger=logger)
    elif status_page_config == "from_file":
        status_page_file_paths = _check_data_path(
            data_path=status_pages, logger=logger, key_to_check_for="status_pages"
        )
        add_status_page(status_page_data_files=status_page_file_paths, logger=logger)
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
    # monitor_file_paths = _check_monitor_data_path(status_page_data_files=monitors, logger=logger)
    # delete_monitor(monitor_data_files=monitor_file_paths, logger=logger)
    disconnect()


@app.command(name="list", help="List all uptime kuma status pages.")
def status_page_list(
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
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
    list_status_pages(verbose=verbose, logger=logger)
    disconnect()


@app.command(name="show", help="Show a status page details.")
def status_page_show(
    slug: Annotated[str, typer.Option(..., "--slug", "-s", help="Slug of the status page.")],
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
):
    """
    Show a status page details.

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    get_satus_page(url=config_data.url, slug=slug, logger=logger)
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
