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


def _get_notification_by_name_or_id(response=None, notification_name=None, notification_id=None, logger=None):
    """
    Get notification process details by name or id

    :param response: (list) List of dictionaries with notification data.
    :param notification_name: (str) The name of the notification process.
    :param notification_id: (int) id of the notification process.
    :param logger: (object) Logger object instance.
    :return: (dict) notification details.
    """

    for _notification in response:
        logger.debug(f"Notification id: {notification_id}")
        logger.debug(f"Notification name: {notification_name}")
        if _notification["name"] == notification_name or _notification["id"] == notification_id:
            response = [_notification]
            return response
    console.print(f":orange_circle: Notification id or name doesn't exist.", style="logging.level.warning")


def list_notifications(verbose=None, name=None, id=None, logger=None):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param name: (str) Uptime kuma notification process name.
    :param id: (int) Uptime kuma notification process id.
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
    if name is not None or id is not None:
        pretty_response = _get_notification_by_name_or_id(response=pretty_response, notification_name=name, notification_id=id, logger=logger)
    if pretty_response:
        console.print(f":megaphone: Available notification processes", style="logging.level.info")
        if verbose:
            console.print(f"{json.dumps(pretty_response, indent=4, sort_keys=True)}", style="logging.level.info")
        else:
            table = Table("id", "type", "name", "active", "isDefault")
            for item in pretty_response:
                table.add_row(str(item["id"]), item["type"], item["name"], str(item["active"]), str(item["isDefault"]))
            console.print(table, style="green")
