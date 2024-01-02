#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Monitors module for kumaone"""

# Import builtin python libraries
import json
import os
from pathlib import Path
import sys


# Import external python libraries
from rich.console import Console
from rich import print
from rich.table import Table
from socketio.exceptions import TimeoutError
import yaml

# Import custom (local) python packages
from .connection import sio
from .event_handlers import get_event_data, wait_for_event
from . import ioevents
from .payload_handler import _get_monitor_payload
from .settings import get_missing_arguments

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _check_monitor_data_path(data_path=None, logger=None):
    """
    Checks data path for monitor input file or directory

    :param data_path: (Path) monitor data.
    :param logger: (object) logger object.
    :return: (int) Monitor ID.
    """

    print("-" * 80)
    console.print(f":clipboard: Checking monitor input data path.", style="logging.level.info")
    if Path(data_path).exists():
        if Path(data_path).is_dir():
            monitor_input_type = "directory"
            logger.info(f"{data_path} is a directory. All yaml files in this directory will be considered.")
            console.print(
                f":file_folder: Directory input detected. Input file directory: '{data_path}'.",
                style="logging.level.info",
            )
            with os.scandir(Path(data_path)) as items:
                monitor_data_files = []
                for item in items:
                    if item.is_file():
                        file_type = item.name.split(".")[-1]
                        if file_type == "yaml" or file_type == "yml":
                            logger.info(f"{item.name} - {item.stat().st_size} bytes.")
                            monitor_data_files.append(Path(data_path).joinpath(item.name))
                        else:
                            console.print(
                                f":bulb: '.{file_type}' file type is not supported. Skipping '{item.name}'. ",
                                style="logging.level.info",
                            )
                    else:
                        console.print(
                            f":card_index_dividers: Nested directories are not supported. Skipping '{item.name}'.",
                            style="logging.level.info",
                        )
            console.print(
                f":high_brightness: {len(monitor_data_files)} files found in supported format.",
                style="logging.level.info",
            )
            logger.debug(f"{monitor_data_files}")
            return sorted(monitor_data_files)
        elif Path(data_path).is_file():
            monitor_input_type = "singlefile"
            logger.info(f"'{data_path}' is a file.")
            console.print(
                f":high_brightness: Single file input detected. Input file: '{data_path}'.", style="logging.level.info"
            )
            return sorted([data_path])
    else:
        console.print(f":x:  Monitor data path: '{data_path}', does not exists!", style="logging.level.error")
        exit(1)


def _sio_call(event=None, data=None):
    """
    Calls socketIO event

    :param event: (str) Event name.
    :param data: (any) Event related data.
    :return: (any)
    """

    try:
        response = sio.call(event, data=data)
    except TimeoutError:
        console.print(f":hourglass:  Request timed out while waiting for '{event}' event.", style="logging.level.info")
        sys.exit(1)
    if isinstance(response, dict):
        if not response["ok"]:
            console.print(f":point_right: Error! {response.get('msg')}")
            sys.exit(1)
    return response
    # try:
    #     json_response = json.load(response)
    #     if not json_response["ok"]:
    #         console.print(f":point_right: Error: {json_response.get('msg')}")
    #     return json_response
    # except ValueError as err:
    #     console.print(f":dizzy_face: Response is not JSON serializable.", style="logging.level.error")
    #     console.print(f":point_right: Error: {err}")


def _check_monitor(monitor_name_to_check=None):
    """
    Checks if the provided monitor exists or not. Can check both group and process monitor.

    :param monitor_name_to_check: (str) Name of the monitor to check
    :return: (dict) Monitor info dictionary
    """

    current_monitors = get_event_data(ioevents.monitor_list).values()
    monitor_exists = False
    monitor_info = {}
    for item in current_monitors:
        if item["name"] == monitor_name_to_check:
            m_id = item["id"]
            monitor_exists = True
            monitor_info = {"name": item["name"], "id": m_id, "exists": monitor_exists}
        else:
            pass
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
        console.print(f":point_right: Monitor group: '{group_name}' does not exists.", style="logging.level.info")
        monitor_group_data_payload = _get_monitor_payload(type="group", name=group_name)
        with wait_for_event(ioevents.monitor_list):
            add_event_response = _sio_call("add", monitor_group_data_payload)
        if add_event_response["ok"]:
            monitor_group_info = {"name": group_name, "id": add_event_response["monitorID"]}
            console.print(
                f":hatching_chick: Monitor group '{group_name}' has been created.", style="logging.level.info"
            )
        else:
            console.print(f":point_right: Error! {add_event_response.get('msg')}", style="logging.level.error")
    return monitor_group_info


def _get_or_create_monitor_process(input_data=None):
    """
    Get or create monitor process

    :param input_data: (dict) Monitor process input data
    :return: (dict) 'add' event response or process exists dictionary
    """

    monitor_process_name = input_data["name"]
    monitor_process_check = _check_monitor(monitor_name_to_check=monitor_process_name)

    if monitor_process_check["exists"]:
        console.print(
            f":sunflower: Monitor process '{monitor_process_name}' already exists.", style="logging.level.info"
        )
        monitor_process_info = {"name": monitor_process_name, "id": monitor_process_check["id"]}
    else:
        # logger.info(f"Monitor process '{monitor_process_name}' doesn't exists.")
        # logger.info(f"Creating monitor process for '{monitor_process_name}'.")
        monitor_process_data_payload = _get_monitor_payload(**input_data)
        # print(monitor_process_data_payload)
        missing_arguments = get_missing_arguments(monitor_process_data_payload)
        if not missing_arguments:
            with wait_for_event(ioevents.monitor_list):
                add_event_response = _sio_call("add", monitor_process_data_payload)
            if add_event_response["ok"]:
                monitor_process_info = {"name": monitor_process_name, "id": add_event_response["monitorID"]}
                console.print(
                    f":hatching_chick: Monitor process for '{input_data['name']}' has been created.",
                    style="logging.level.info",
                )
            else:
                console.print(f":point_right: Error! {add_event_response.get('msg')}", style="logging.level.error")
        else:
            flat_missing_arguments = ", ".join([f"'{item}'" for item in missing_arguments])
            console.print(
                f":nut_and_bolt: Missing arguments for monitor process '{monitor_process_name}'. Missing {flat_missing_arguments} key(s).",
                style="logging.level.error",
            )
            sys.exit(1)
    return monitor_process_info


def _delete_monitor_process_or_group(input_data=None):
    """
    Delete a monitor

    :param input_data: (dict) Input data about the monitor to be deleted
    :return: (bool) True if deletion is successful, False otherwise
    """

    monitor_process_name = input_data["name"]
    monitor_process_check = _check_monitor(monitor_name_to_check=monitor_process_name)

    if monitor_process_check["exists"]:
        # console.print(f":wastebasket: Deleting process monitor '{monitor_process_name}'.", style="logging.level.info", new_line_start=False)
        monitor_id = monitor_process_check["id"]
        delete_event_response = _sio_call("deleteMonitor", monitor_id)
        if isinstance(delete_event_response, dict):
            if delete_event_response["ok"]:
                console.print(f":ghost: '{monitor_process_name}' deletion successful!", style="logging.level.info")
            else:
                console.print(f":crab: '{monitor_process_name}' deletion unsuccessful!", style="logging.level.warning")
        else:
            console.print(f":point_right: Something went wrong! {delete_event_response['msg']}", style="logging.level.error")
            return False
    else:
        console.print(f":running_shoe: Monitor {monitor_process_name} doesn't exist. Skipping...", style="logging.level.info")


def add_monitor(monitor_data_files=None, logger=None):
    """
    Adds one or more monitor(s)

    :param monitor_data_files: (list) Data file path(s)
    :param logger: (object) Logger object
    :return: None
    """

    for monitor_file in monitor_data_files:
        with open(monitor_file, "r") as monitors_:
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
                            monitor_process_info = _get_or_create_monitor_process(input_data=input_data)
                            if monitor_process_info:
                                pass
                        else:
                            console.print(f":gloves: Monitor process data malformed, please check input.", style="logging.level.error")
                            sys.exit(1)
                else:
                    console.print(
                        f":potato: Group creation failed! Couldn't create group: '{group}'", style="logging.level.info"
                    )
                    console.print(f":point_right: Message: {monitor_group_info}", style="logging.level.error")
    print("-" * 80)


def delete_monitor(monitor_data_files=None, logger=None):
    """
    Deletes one or more monitor(s)

    :param monitor_data_files: (list) Data file path(s)
    :param logger: (object) Logger object
    :return: None
    """

    for monitor_file in monitor_data_files:
        with open(monitor_file, "r") as monitors_:
            monitors = yaml.safe_load(monitors_)["monitors"]
            groups = [group for group in monitors.keys()]
            for group in groups:
                print(f"-" * 38 + f" {group} ".upper() + f"-" * (40 - len(group)))
                for monitor_process_data in monitors[group]:
                    if isinstance(monitor_process_data, dict):
                        _delete_monitor_process_or_group(input_data=monitor_process_data)
                    else:
                        console.print(f":gloves: Monitor process data malformed, please check input.", style="logging.level.error")
                        sys.exit(1)
    print("-" * 80)

def list_monitors(show_groups=None, show_processes=None, verbose=None, logger=None):
    """
    Show list of monitor groups and processes.

    :param show_groups: (bool) Show only monitoring groups.
    :param show_processes: (bool) Show only monitoring processes.
    :param verbose: (bool) Show verbose output.
    :param logger: Logger object.
    :return: None
    """
    response = list(get_event_data(ioevents.monitor_list).values())
    logger.info(json.dumps(response, indent=4))

    table = Table("id", "name")
    if show_groups:
        for item in response:
            if item["type"] == "group":
                table.add_row(str(item["id"]), item["name"])
        console.print(f":hamburger: Available monitor groups.", style="green")
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
        for item in response:
            print(item["name"])
