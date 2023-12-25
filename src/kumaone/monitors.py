#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Monitors module for kumaone"""

# Import builtin python libraries
import json

# Import external python libraries
from rich import print

# Import custom (local) python packages
from .event_handlers import get_event_data
from . import ioevents

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"


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
