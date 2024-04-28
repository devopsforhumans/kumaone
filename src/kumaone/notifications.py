#!/usr/bin/env python3

"""Notification pages module for kumaone"""

# Import builtin python libraries
import json
from pathlib import Path
import yaml

# Import external python libraries
from rich.console import Console
from rich.table import Table

# Import custom (local) python packages
from .event_handlers import get_event_data, wait_for_event
from .notification_settings import notification_types, notification_providers
from . import ioevents
from .utils import _sio_call

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _get_notification_by_name_or_id(response=None, notification_title=None, notification_id=None, logger=None):
    """
    Get notification process details by name or id

    :param response: (list) List of dictionaries with notification data.
    :param notification_title: (str) The name of the notification process.
    :param notification_id: (int) id of the notification process.
    :param logger: (object) Logger object instance.
    :return: (dict) notification details.
    """

    for _notification in response:
        logger.debug(f"Notification id: {notification_id}")
        logger.debug(f"Notification name: {notification_title}")
        if _notification["name"] == notification_title or _notification["id"] == notification_id:
            response = [_notification]
            return response


def _get_notification_id_by_name(notification_title=None, logger=None):
    """
    Get notification id by name.

    :param notification_title: (str) Name of the notification.
    :param logger: (object) Logger object instance.
    :return: (int) Notification id.
    """

    response = get_event_data(ioevents.notification_list)
    logger.debug(f"Notification List: {response}")
    for _notification in response:
        if _notification["name"] == notification_title:
            return _notification["id"]
    return -1


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
        with open(notifications_file_path) as notification_config_file:
            notification_configs = yaml.safe_load(notification_config_file)["notifications"]
        logger.debug(notification_configs)
    for notification_config in notification_configs:
        required_args = ["name", "type", "isDefault", "applyExisting"]
        for notification_type, payload in notification_config.items():
            payload['type'] = notification_types[notification_type.lower()]
            logger.debug(f"Payload for '{payload['type']}': {payload}")
            # Check if necessary arguments are provided
            for key, val in notification_providers[notification_type.lower()].items():
                if val["required"]:
                    required_args.append(key)
            logger.debug(f"Required args: {required_args}")
            logger.debug(f"Payload args: {payload.keys()}")
            missing_keys = []
            for key in required_args:
                if key not in payload.keys():
                    missing_keys.append(key)
            if missing_keys:
                raise TypeError(f"'{payload['type']}' notification type is missing required arguments: {missing_keys}.")
            notification_provider_exists = list_notifications(
                notification_title=payload["name"], logger=logger, check_existence=True
            )
            if not notification_provider_exists:
                with wait_for_event(ioevents.notification_list):
                    response = _sio_call("addNotification", (payload, None))
                    if verbose:
                        print(f"{payload['type']}: {response}")
                    else:
                        if response["ok"]:
                            console.print(
                                f":floppy_disk: Notification provider '{payload['type'].title()}' added successfully.",
                                style="logging.level.info",
                            )
                        else:
                            console.print(
                                f":orange_circle: '{payload['type']}' notification provider addition failed. Response: {response['msg']}",
                                style="logging.level.warning",
                            )
            else:
                console.print(f":sunflower: '{payload['type'].title()}' notification provider already exists.")


def list_notifications(verbose=None, notification_title=None, notification_id=None, logger=None, check_existence=False):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param notification_title: (str) Uptime kuma notification process name.
    :param notification_id: (int) Uptime kuma notification process id.
    :param logger: (object) Logging object.
    :param check_existence: (bool) Check existence of notification provider by name.
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
    if notification_title is not None or notification_id is not None:
        pretty_response = _get_notification_by_name_or_id(
            response=pretty_response,
            notification_title=notification_title,
            notification_id=notification_id,
            logger=logger,
        )
    if pretty_response:
        if check_existence:
            return True
        console.print(f":megaphone: Available notification providers", style="logging.level.info")
        if verbose:
            console.print(f"{json.dumps(pretty_response, indent=4, sort_keys=True)}", style="logging.level.info")
        else:
            table = Table("id", "type", "title", "active", "isDefault")
            for item in pretty_response:
                table.add_row(str(item["id"]), item["type"], item["name"], str(item["active"]), str(item["isDefault"]))
            if table.rows:
                console.print(table, style="green")
            else:
                console.print(f":four_leaf_clover: No data available.", style="logging.level.info")
    else:
        if check_existence:
            return False
        console.print(f":four_leaf_clover: No data available.", style="logging.level.info")


def list_notification_providers(verbose=None, logger=None):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param logger: (object) Logging object.
    :return: (dict) Dictionary of arguments for a notification provider
    """

    table = Table("Supported Providers")
    for key in notification_types.keys():
        table.add_row(key.lower())
    if table.rows:
        console.print(table, style="green")


def list_notification_provider_args(verbose=None, notification_type=None, logger=None, check_existence=False):
    """
    Show list of notification processes

    :param verbose: (bool) Enable verbose output.
    :param notification_type: (str) Uptime kuma notification process name.
    :param logger: (object) Logging object.
    :param check_existence: (bool) Check existence of notification provider by name.
    :return: (dict) Dictionary of arguments for a notification provider
    """

    table = Table("Argument Key", "Required?")
    for key, val in notification_providers[notification_type.lower()].items():
        table.add_row(key, str(val["required"]))
    if table.rows:
        console.print(table, style="green")


def delete_notification(notifications_file_path=None, notification_title=None, logger=None, verbose=None):
    """
    Delete a notification provider.

    :param notifications_file_path: (Path) Path to the notification provider definition file.
    :param notification_title: (str) Whether the notification provider should be added interactively or not.
    :param logger: (object) Logger object instance.
    :param verbose: (bool) Print verbose output if True.
    :return: None
    """

    notification_provider_to_delete = []
    if notifications_file_path is not None and Path(notifications_file_path).is_file():
        with open(notifications_file_path, "r") as notification_config_file:
            notification_configs = yaml.safe_load(notification_config_file)["notifications"]
        logger.debug(notification_configs)
        for notification_config in notification_configs:
            for _notification in notification_config.values():
                notification_id = _get_notification_id_by_name(notification_title=_notification["name"], logger=logger)
                if notification_id != -1:
                    notification_provider_to_delete.append(notification_id)
    elif notification_title is not None:
        notification_id = _get_notification_id_by_name(notification_title=notification_title, logger=logger)
        if notification_id != -1:
            notification_provider_to_delete.append(notification_id)
    logger.debug(f"Notification provider IDs to delete: {notification_provider_to_delete}")
    if notification_provider_to_delete:
        for _notification_id in notification_provider_to_delete:
            with wait_for_event(ioevents.notification_list):
                delete_event_response = _sio_call("deleteNotification", _notification_id)
                if delete_event_response["ok"]:
                    console.print(
                        f":ghost: Notification provider with id: '{_notification_id}' has been deleted.",
                        style="logging.level.info",
                    )
    else:
        console.print(f":running_shoe: Notification provider(s) doesn't exist. Skipping...", style="logging.level.info")
