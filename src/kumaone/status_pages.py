#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Status pages module for kumaone"""

# Import builtin python libraries
import json
import sys

import yaml

# Import external python libraries
from rich.console import Console
from rich import print
from rich.rule import Rule
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


def get_satus_page(url=None, slug=None, logger=None, full_details=True):
    """
    Get a status page by slug.

    :param url: (str) Uptime kuma url.
    :param slug: (str) Status page slug.
    :param logger: (object) Logger object.
    :param full_details: (bool) Full details if True, event response only otherwise.
    :return: (dict) Python dictionary with status page info
    """

    event_response = _sio_call("getStatusPage", slug)

    if full_details:
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
        return status_page_data
    else:
        return event_response


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
        # console.print(Rule(style="purple"))
        for status_page_data_file in status_page_data_files:
            with open(status_page_data_file, "r") as tmp_data_file_read:
                status_pages = yaml.safe_load(tmp_data_file_read)["status_pages"]
                for status_page in status_pages:
                    logger.debug(status_page)
                    status_page_id = add_status_page(
                        status_page_title=status_page["title"].title(),
                        status_page_slug=status_page["slug"],
                        logger=logger,
                    )
    else:
        status_page_info = get_satus_page(slug=status_page_slug, full_details=False, logger=logger)
        if status_page_info["ok"]:
            status_page_id = status_page_info["config"]["id"]
            console.print(
                f":sunflower: Status page '{status_page_id} - {status_page_title} ({status_page_slug})' already exists."
            )
            logger.debug(status_page_info)
            return status_page_info["config"]["id"]
        else:
            with wait_for_event(ioevents.status_page_list):
                response = _sio_call("addStatusPage", (status_page_title.title(), status_page_slug))
                if response["ok"]:
                    console.print(
                        f":hatching_chick: Status page '{status_page_title.title()} ({status_page_slug})' has been created.",
                        style="logging.level.info",
                    )
                    logger.debug(f"Status page creation response: {response}")
                else:
                    console.print(f":red_circle: Error: {response['msg']}")
                    sys.exit(1)
    # console.print(Rule(style="purple"))


def delete_status_page(status_page_data_files=None, status_page_slug=None, logger=None):
    """
    Deletes a status page from uptime kuma.

    :param status_page_data_files: (Path) Status page config file location. File or Directory.
    :param status_page_slug: (str) Slug of the status page.
    :param logger: (object) Logger object for logging purposes.
    :return: None.
    """

    # console.print(Rule(title="Delete Status Page", style="purple"))
    if status_page_data_files:
        pass
    elif status_page_slug:
        status_page_info = _sio_call("getStatusPage", status_page_slug)
        if status_page_info["ok"]:
            response = _sio_call("deleteStatusPage", status_page_slug)
            if response["ok"]:
                console.print(f":wastebasket: Status page '{status_page_slug}' has been deleted.")
        else:
            console.print(f":orange_circle: Status page '{status_page_slug}' does not exist.")
