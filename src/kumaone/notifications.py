#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Status pages module for kumaone"""

# Import builtin python libraries
import json
from pathlib import Path
import yaml

# Import external python libraries
from rich.console import Console
from rich.table import Table

# Import custom (local) python packages
from .event_handlers import get_event_data, wait_for_event
from . import ioevents
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


def add_notification(notifications_file_path=None, interactive=None, logger=None, verbose=None):
    """
    Add notification provider(s)

    :param notifications_file_path: (Path) Path to the notification provider definition file.
    :param interactive: (bool) Whether the notification provider should be added interactively or not.
    :param logger: (object) Logger object instance.
    :param verbose: (bool) Print verbose output if True.
    :return: None
    """

    if notifications_file_path is not None and Path(notifications_file_path).is_file():
        with open(notifications_file_path, "r") as notification_config_file:
            notification_configs = yaml.safe_load(notification_config_file)["notifications"]
        logger.debug(notification_configs)
    for notification_config in notification_configs:
        for payload in notification_config.values():
            logger.debug(f"Payload for '{payload['type']}': {payload}")
            # TODO: check if already exists or not.
            with wait_for_event(ioevents.notification_list):
                response = _sio_call("addNotification", (payload, None))
                if verbose:
                    print(f"{payload['type']}: {response}")
                else:
                    if response["ok"]:
                        console.print(
                            f":floppy_disk: Notification provider for {payload['type']} added successfully.",
                            style="logging.level.info",
                        )
                    else:
                        console.print(
                            f":orange_circle: '{payload['type']}' notification provider addition failed. Response: {response['msg']}",
                            style="logging.level.warning",
                        )


def list_notifications(verbose=None, name=None, notification_id=None, logger=None):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param name: (str) Uptime kuma notification process name.
    :param notification_id: (int) Uptime kuma notification process id.
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
    if name is not None or notification_id is not None:
        pretty_response = _get_notification_by_name_or_id(
            response=pretty_response, notification_name=name, notification_id=notification_id, logger=logger
        )
    if pretty_response:
        console.print(f":megaphone: Available notification providers", style="logging.level.info")
        if verbose:
            console.print(f"{json.dumps(pretty_response, indent=4, sort_keys=True)}", style="logging.level.info")
        else:
            table = Table("id", "type", "name", "active", "isDefault")
            for item in pretty_response:
                table.add_row(str(item["id"]), item["type"], item["name"], str(item["active"]), str(item["isDefault"]))
            console.print(table, style="green")
