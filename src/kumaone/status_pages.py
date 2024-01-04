#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Status pages module for kumaone"""

# Import builtin python libraries
import json
import sys


# Import external python libraries
from rich.console import Console
from rich import print
from rich.table import Table
import requests


# Import custom (local) python packages
from .event_handlers import get_event_data, wait_for_event
from . import ioevents
from .payload_handler import _get_monitor_payload
from .settings import get_missing_arguments, timeout
from .utils import _sio_call

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def list_status_pages(verbose=None, logger=None):
    """
    Show list of status pages.

    :param verbose: (bool) verbose output.
    :param logger: (object) Logger object.
    :return: None
    """

    response = list(get_event_data(ioevents.status_page_list).values())
    logger.info(json.dumps(response, indent=4))
    console.print(f":hamburger: Available status pages.", style="green")
    table = Table("id", "slug", "Title")
    if not verbose:
        if response:
            for item in response:
                table.add_row(str(item["id"]), item["slug"], item["title"])
            if table.rows:
                console.print(table, style="green")
            else:
                console.print(f":four_leaf_clover: No data available.")
    else:
        console.print(json.dumps(response, indent=4, sort_keys=True), style="green")


def get_satus_page(url=None, slug=None, logger=None):
    """
    Get a status page by slug.

    :param url: (str) Uptime kuma url.
    :param slug: (str) Status page slug.
    :param logger: (object) Logger object.
    :return: (dict) Python dictionary with status page info
    """

    event_response = _sio_call("getStatusPage", slug)

    try:
        http_response = requests.get(f"{url}/api/status-page/{slug}", timeout=timeout).json()
    except requests.exceptions.JSONDecodeError:
        console.print(f":cyclone: Response is not valid JSON.", style="logging.level.error")
        sys.exit(1)
    except requests.exceptions.Timeout:
        console.print(f":poodle: Response timed out.", style="logging.level.error")
        sys.exit(1)

    config = event_response["config"]
    config.update(http_response["config"])
    status_page_data = {
        **config,
        "incident": http_response["incident"],
        "publicGroupList": http_response["publicGroupList"],
        "maintenanceList": http_response["maintenanceList"],
    }
    # TODO: Check if we need to convert 'sendUrl' to boolean
    console.print(f":page_facing_up: '{slug}' status page details", style="logging.level.info")
    console.print(f"{json.dumps(status_page_data, indent=4, sort_keys=True)}", style="logging.level.info")


def add_status_page(status_page_data_files=None, status_page_title=None, status_page_slug=None, logger=None):
    """
    Creates/Adds a status page in uptime kuma.

    :param status_page_data_files: (Path) Status page config file location. File or Directory.
    :param status_page_title: (str) Title of the status page.
    :param status_page_slug: (str) Slug of the status page.
    :param logger: (object) Logger object for logging purposes.
    :return: None.
    """

    if status_page_data_files:
        print(status_page_data_files)
    else:
        print(status_page_title)
        print(status_page_slug)
    # with wait_for_event(ioevents.status_page_list):
    #     response = _sio_call("addStatusPage", (status_page_title, status_page_slug))
    # if response["ok"]:
    #     console.print(
    #         f":hatching_chick: Status page '{status_page_title} ({status_page_slug})' has been created.",
    #         style="logging.level.info",
    #     )
    # else:
    #     console.print(f":red_circle: Error: {response['msg']}")
    #     sys.exit(1)
