#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Monitors module for kumaone"""

# Import builtin python libraries

# Import external python libraries

# Import custom (local) python packages
from .event_handlers import get_event_data
from . import ioevents

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"


def list_monitors():
    response = list(get_event_data(ioevents.monitor_list).values())
    # print(json.dumps(response, indent=4))
    groups = []
    processes = []
    for item in response:
        if item["type"] == "group":
            groups.append(item)
        else:
            processes.append(item)
    for group in groups:
        print(group["name"])
    print("============")
    for process in processes:
        print(process["name"])
