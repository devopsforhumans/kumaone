#!/usr/bin/env python3


"""monitor module for kumaone"""
import sys

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
from src.kumaone.status_pages import add_status_page, delete_status_page, get_satus_page, list_status_pages
from src.kumaone.utils import _check_data_path, log_manager, _mutual_exclusivity_check

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
        typer.Option(
            ...,
            "--pages",
            "-p",
            help="Status page(s) data. Exclusive to '--title' and '--slug'",
            callback=_mutual_exclusivity_check(size=3),
        ),
    ] = None,
    title: Annotated[
        str,
        typer.Option(
            ...,
            "--title",
            "-t",
            help="Title of the status page. '--slug' is required.",
            callback=_mutual_exclusivity_check(size=3),
        ),
    ] = None,
    slug: Annotated[
        str,
        typer.Option(
            ...,
            "--slug",
            "-s",
            help="Slug of the status page. '--title' is required.",
            callback=_mutual_exclusivity_check(size=3),
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path], typer.Option(..., "--config", "-c", help="Uptime kuma configuration file path.")
    ] = Path.home().joinpath(".config/kumaone/kuma.yaml"),
    log_level: Annotated[str, typer.Option(help="Set log level.")] = "NOTSET",
    save: Annotated[
        bool, typer.Option(help="Add monitors to a status page. Valid when '--pages' / '-p' set to a directory.")
    ] = False,
):
    """
    Add one or more uptime kuma status page(s).

    :return: None
    """

    if log_level:
        state["log_level"] = log_level
        logger = log_manager(log_level=log_level)
    if status_pages is None and title is None and slug is None:
        raise typer.BadParameter(
            "At least '--title' / '-t' and '--slug' / '-s' parameters OR '--pages' / '-p' parameter is required."
        )
    elif status_pages:
        status_page_config = "from_file"
    elif title and slug:
        status_page_config = "inline"
    elif title is None or slug is None:
        raise typer.BadParameter("Both '--title' / '-t' and '--slug' / '-s' parametes are required.")
        exit(1)

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if status_page_config == "inline":
        add_status_page(status_page_title=title, status_page_slug=slug, logger=logger)
    elif status_page_config == "from_file":
        status_page_file_paths = _check_data_path(
            data_path=status_pages, logger=logger, key_to_check_for="status_pages"
        )
        add_status_page(status_page_data_files=status_page_file_paths, logger=logger, url=config_data.url, save=save)
    disconnect()


@app.command(name="delete", help="Delete one or more uptime kuma status page(s).")
def status_page_delete(
    status_pages: Annotated[
        Optional[Path],
        typer.Option(..., "--pages", "-p", help="Status page(s) data. Exclusive to '--slug'"),
    ] = None,
    slug: Annotated[str, typer.Option(..., "--slug", "-s", help="Slug of the status page.")] = None,
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
    if status_pages is None and slug is None:
        raise typer.BadParameter(
            message="At least one of the parameters '--slug' / '-s' OR '--pages' / '-p' is required."
        )
        sys.exit(1)
    elif status_pages:
        status_page_config = "from_file"
    elif status_pages is None and slug is not None:
        status_page_config = "inline"

    config_data = check_config(config_path=config_file, logger=logger)
    connect_login(config_data=config_data)
    if status_page_config == "inline":
        delete_status_page(status_page_slug=slug, logger=logger)
    elif status_page_config == "from_file":
        status_page_file_paths = _check_data_path(
            data_path=status_pages, logger=logger, key_to_check_for="status_pages"
        )
        delete_status_page(status_page_data_files=status_page_file_paths, logger=logger)
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
    get_satus_page(slug=slug, logger=logger, url=config_data.url, show_details=True)
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
