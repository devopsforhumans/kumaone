#!/usr/bin/env python3

"""Monitors module for kumaone"""

# Import builtin python libraries
import json
import sys

# Import external python libraries
from rich.columns import Columns
from rich.console import Console
from rich import print
from rich.table import Table
import yaml

# Import custom (local) python packages
from .event_handlers import get_event_data, wait_for_event
from . import ioevents
from .payload_handler import _get_monitor_payload
from .settings import get_missing_arguments
from .utils import _sio_call

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _check_monitor(monitor_name_to_check=None, monitor_id_to_check=None):
    """
    Checks if the provided monitor exists or not. Can check both group and process monitor.

    :param monitor_name_to_check: (str) Name of the monitor to check
    :param monitor_id_to_check: (int) ID of the monitor to check
    :return: (dict) Monitor info dictionary
    """

    current_monitors = get_event_data(ioevents.monitor_list).values()
    monitor_exists = False
    monitor_info = {}
    for item in current_monitors:
        if monitor_name_to_check is not None:
            if item["name"] == monitor_name_to_check:
                m_id = item["id"]
                monitor_exists = True
                monitor_info = {"name": item["name"], "id": m_id, "exists": monitor_exists}
        elif monitor_id_to_check is not None:
            if item["id"] == monitor_id_to_check:
                monitor_exists = True
                monitor_info = {"name": item["name"], "id": item["id"], "exists": monitor_exists}
    if not monitor_exists:
        monitor_info = {"name": monitor_name_to_check, "id": None, "exists": monitor_exists}
    return monitor_info


def _get_or_create_monitor_group(group_name=None):
    """
    Get or create monitor group

    :param group_name: (str) Monitor group to create
    :return: (dict) Name and id of the group as python dict
    """

    monitor_group_check = _check_monitor(monitor_name_to_check=group_name)
    if monitor_group_check['exists']:
        console.print(f":sunflower: Monitor group '{group_name}' already exists.", style="logging.level.info")
        monitor_group_info = {"name": group_name, "id": monitor_group_check["id"]}
    else:
        # logger.info(f":blue_circle: Monitor group: '{group_name}' does not exist.", style="logging.level.info")
        monitor_group_data_payload = _get_monitor_payload(type="group", name=group_name)
        with wait_for_event(ioevents.monitor_list):
            add_event_response = _sio_call("add", monitor_group_data_payload)
        if add_event_response["ok"]:
            monitor_group_info = {"name": group_name, "id": add_event_response["monitorID"]}
            console.print(
                f":hatching_chick: Monitor group '{group_name}' has been created.", style="logging.level.info"
            )
        else:
            console.print(f":red_circle: Error! {add_event_response.get('msg')}", style="logging.level.error")
    return monitor_group_info


def _get_or_create_process_monitor(input_data=None):
    """
    Get or create monitor process

    :param input_data: (dict) Monitor process input data
    :return: (dict) 'add' event response or process exists dictionary
    """

    process_monitor_name = input_data["name"]
    process_monitor_check = _check_monitor(monitor_name_to_check=process_monitor_name)

    if process_monitor_check["exists"]:
        console.print(
            f":sunflower: Monitor process '{process_monitor_name}' already exists.", style="logging.level.info"
        )
        process_monitor_info = {"name": process_monitor_name, "id": process_monitor_check["id"]}
    else:
        # logger.info(f"Monitor process '{process_monitor_name}' doesn't exists.")
        # logger.info(f"Creating monitor process for '{process_monitor_name}'.")
        process_monitor_data_payload = _get_monitor_payload(**input_data)
        # print(process_monitor_data_payload)
        missing_arguments = get_missing_arguments(process_monitor_data_payload)
        if not missing_arguments:
            with wait_for_event(ioevents.monitor_list):
                add_event_response = _sio_call("add", process_monitor_data_payload)
            if add_event_response["ok"]:
                process_monitor_info = {"name": process_monitor_name, "id": add_event_response["monitorID"]}
                console.print(
                    f":hatching_chick: Monitor process for '{input_data['name']}' has been created.",
                    style="logging.level.info",
                )
            else:
                console.print(f":red_circle: Error! {add_event_response.get('msg')}", style="logging.level.error")
        else:
            flat_missing_arguments = ", ".join([f"'{item}'" for item in missing_arguments])
            console.print(
                f":nut_and_bolt: Missing arguments for monitor process '{process_monitor_name}'. Missing {flat_missing_arguments} key(s).",
                style="logging.level.error",
            )
            sys.exit(1)
    return process_monitor_info


def _delete_process_monitor_or_group(input_data=None):
    """
    Delete a monitor

    :param input_data: (dict) Input data about the monitor to be deleted
    :return: (bool) True if deletion is successful, False otherwise
    """

    if "name" in input_data:
        process_monitor_name = input_data["name"]
        process_monitor_check = _check_monitor(monitor_name_to_check=process_monitor_name)
    elif "id" in input_data:
        process_monitor_id = input_data["id"]
        process_monitor_check = _check_monitor(monitor_id_to_check=process_monitor_id)
    if process_monitor_check["exists"]:
        # console.print(f":wastebasket: Deleting process monitor '{process_monitor_name}'.", style="logging.level.info")
        monitor_id = process_monitor_check["id"]
        monitor_name = process_monitor_check["name"]
        delete_event_response = _sio_call("deleteMonitor", monitor_id)
        if isinstance(delete_event_response, dict):
            if delete_event_response["ok"]:
                console.print(
                    f":ghost: '{monitor_name}' monitor deletion successful!", style="logging.level.info"
                )
            else:
                console.print(
                    f":crab: '{monitor_name}' monitor deletion unsuccessful!", style="logging.level.warning"
                )
        else:
            console.print(
                f":red_circle: Something went wrong! {delete_event_response['msg']}", style="logging.level.error"
            )
            return False
    else:
        console.print(
            f":running_shoe: Monitor with provided name/id doesn't exist. Skipping...", style="logging.level.info"
        )


def add_monitor(monitor_data_files=None, logger=None):
    """
    Adds one or more monitor(s)

    :param monitor_data_files: (list) Data file path(s)
    :param logger: (object) Logger object
    :return: None
    """

    for monitor_file in monitor_data_files:
        with open(monitor_file) as monitors_:
            monitors = yaml.safe_load(monitors_)["monitors"]
            groups = [group for group in monitors.keys()]
            for group in groups:
                print(f"-" * 38 + f" {group} ".upper() + f"-" * (40 - len(group)))
                if group == "default":
                    monitor_group_info = {"name": None, "id": None}
                else:
                    monitor_group_info = _get_or_create_monitor_group(group_name=group)
                if monitor_group_info:
                    for input_data in monitors[group]:
                        if isinstance(input_data, dict):
                            if group == "default":
                                pass
                            else:
                                input_data.update({"parent": monitor_group_info["id"]})
                            process_monitor_info = _get_or_create_process_monitor(input_data=input_data)
                            if process_monitor_info:
                                pass
                        else:
                            console.print(
                                f":gloves: Monitor process data malformed, please check input.",
                                style="logging.level.error",
                            )
                            sys.exit(1)
                else:
                    console.print(
                        f":potato: Group creation failed! Couldn't create group: '{group}'", style="logging.level.info"
                    )
                    console.print(f":red_circle: Message: {monitor_group_info}", style="logging.level.error")
    print("-" * 80)


def delete_monitor(monitor_data_files=None, monitor_name=None, monitor_id=None, logger=None):
    """
    Deletes one or more monitor(s)

    :param monitor_data_files: (list) Data file path(s)
    :param monitor_name: (str) Single monitor name
    :param monitor_id: (int) Single monitor id
    :param logger: (object) Logger object
    :return: None
    """

    if monitor_name is not None:
        _delete_process_monitor_or_group(input_data={"name": monitor_name})
    elif monitor_id is not None:
        _delete_process_monitor_or_group(input_data={"id": monitor_id})
    elif monitor_data_files:
        for monitor_file in monitor_data_files:
            with open(monitor_file, "r") as monitors_:
                monitors = yaml.safe_load(monitors_)["monitors"]
                groups = [group for group in monitors.keys()]
                for group in groups:
                    print(f"-" * 38 + f" {group} ".upper() + f"-" * (40 - len(group)))
                    for process_monitor_data in monitors[group]:
                        if isinstance(process_monitor_data, dict):
                            _delete_process_monitor_or_group(input_data=process_monitor_data)
                        else:
                            console.print(
                                f":gloves: Monitor process data malformed, please check input.",
                                style="logging.level.error",
                            )
                    _delete_process_monitor_or_group(input_data={"name": group})
        print("-" * 80)


def list_monitors(monitor_id=None, show_groups=None, show_processes=None, verbose=None, logger=None):
    """
    Show list of monitor groups and processes.

    :param monitor_id: (int) Monitor ID.
    :param show_groups: (bool) Show only monitoring groups.
    :param show_processes: (bool) Show only monitoring processes.
    :param verbose: (bool) Show verbose output.
    :param logger: (object) Logger object.
    :return: None
    """

    response = list(get_event_data(ioevents.monitor_list).values())
    logger.debug(json.dumps(response, indent=4))

    if monitor_id:
        for item in response:
            if item["id"] == monitor_id:
                console.print(f":cupcake: Details about monitor '{item['name']}'")
                console.print(json.dumps(item, indent=4, sort_keys=True), style="logging.level.info")
                return True
        console.print(f":four_leaf_clover: Monitor with ID {monitor_id} does not exist.", style="logging.level.error")
    else:
        table = Table("id", "name")
        if show_groups:
            console.print(f":hamburger: Available monitor groups.", style="green")
            for item in response:
                if item["type"] == "group":
                    table.add_row(str(item["id"]), item["name"])
            if table.rows:
                console.print(table, style="green")
            else:
                console.print(f":four_leaf_clover: No data available.")
        elif show_processes:
            for item in response:
                if item["type"] != "group":
                    table.add_row(str(item["id"]), item["name"])
            console.print(f":hamburger: Available monitor processes.", style="green")
            if table.rows:
                console.print(table, style="green")
            else:
                console.print(f":four_leaf_clover: No data available.", style="logging.level.info")
        elif verbose:
            console.print(json.dumps(response, indent=4, sort_keys=True))
        else:
            console.print(f":hamburger: Available monitors (groups and processes).", style="green")
            monitors = Columns(sorted([item['name'] for item in response], key=str.lower), equal=True, expand=True)
            console.print(monitors, style="logging.level.info")
