#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Monitors module for kumaone"""

# Import builtin python libraries
import json
from pathlib import Path
import os

import yaml
# Import external python libraries
from rich.console import Console
from rich import print

# Import custom (local) python packages
from .event_handlers import get_event_data
from . import ioevents

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _check_monitor_data_path(data_path=None, logger=None):
    """
    Adds monitor to uptime kuma server

    :param data_path: (Path) monitor data.
    :param logger: (object) logger object.
    :return: (int) Monitor ID.
    """

    if Path(data_path).exists():
        if Path(data_path).is_dir():
            monitor_input_type = "directory"
            logger.info(f"{data_path} is a directory. All yaml files in this directory will be considered.")
            console.print(f":file_folder: '{data_path}' is a directory.", style="logging.level.info")
            with os.scandir(Path(data_path)) as items:
                monitor_data_files = []
                for item in items:
                    if item.is_file():
                        file_type = item.name.split(".")[-1]
                        if file_type == "yaml" or file_type == "yml":
                            logger.info(f"{item.name} - {item.stat().st_size} bytes.")
                            monitor_data_files.append(Path(data_path).joinpath(item.name))
                        else:
                            console.print(f":bulb: '.{file_type}' file type is not supported. Skipping '{item.name}'. ", style="logging.level.info")
                    else:
                        console.print(f":card_index_dividers: Nested directories are not supported. Skipping '{item.name}'.", style="logging.level.info")
            console.print(f":high_brightness: {len(monitor_data_files)} files found in supported format.", style="logging.level.info")
            logger.debug(f"{monitor_data_files}")
            return monitor_data_files, monitor_input_type
        elif Path(data_path).is_file():
            monitor_input_type = "singlefile"
            logger.info(f"'{data_path}' is a file.")
            console.print(f":high_brightness: '{data_path}' is a file.", style="logging.level.info")
            return [data_path], monitor_input_type
    else:
        console.print(f":x:  Monitor data path: {data_path}, does not exists!", style="logging.level.error")
        exit(1)


def list_monitors(show_groups=None, show_processes=None, logger=None):
    """
    Show list of monitor groups and processes.

    :param show_groups: (bool) Show only monitoring groups.
    :param show_processes: (bool) Show only monitoring processes.
    :param logger: Logger object.
    :return: None
    """
    response = list(get_event_data(ioevents.monitor_list).values())
    logger.info(json.dumps(response, indent=4))

    if show_groups:
        for item in response:
            if item["type"] == "group":
                print(item["name"])
    elif show_processes:
        for item in response:
            if item["type"] != "group":
                print(item["name"])
    else:
        for item in response:
            print(item["name"])
