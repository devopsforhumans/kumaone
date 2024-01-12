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
from .monitors import _check_monitor
from .payload_handler import _get_status_page_data_payload
from .settings import get_missing_arguments, timeout
from .utils import _sio_call

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def list_notifications(verbose=None, logger=None):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param logger: (object) Logging object.
    :return: None
    """

    response = get_event_data(ioevents.notification_list)
    logger.debug(json.dumps(response, indent=4, sort_keys=True))
    # pretty print information
    pretty_response = []
    for notification in response:
        flat_notification = notification.copy()
        config = json.loads(flat_notification["config"])
        del flat_notification["config"]
        flat_notification.update(config)
        pretty_response.append(flat_notification)
    console.print(f":megaphone: Available notification processes", style="logging.level.info")
    if verbose:
        console.print(f"{json.dumps(pretty_response, indent=4, sort_keys=True)}", style="logging.level.info")
    else:
        table = Table("id", "type", "name", "active", "isDefault")
        for item in pretty_response:
            table.add_row(str(item["id"]), item["type"], item["name"], str(item["active"]), str(item["isDefault"]))
        console.print(table, style="green")
