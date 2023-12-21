#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Connection module for kumaone"""

# Import builtin python libraries
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

# Import external python libraries
from rich.console import Console
import socketio
from socketio.exceptions import TimeoutError


# Import custom (local) python packages
from .config import ConfigActions, check_config, create_config, delete_config, edit_config
from .event_handlers import get_event_data, list_monitors_event
from .utils import app_info, log_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()
sio = socketio.Client()
monitor_list_data = None


def connect_login(config_data=None, headers=None):
    """
    Connects to uptime kuma server

    :param config_data: (dict) Uptime kuma server configs
    :param headers: (dict) Custom headers
    :return: (event) Connection event to uptime kuma server
    """

    try:
        sio.on("monitorList", list_monitors_event)
        sio.connect(config_data.url, headers=headers)
        console.print(f":white_heavy_check_mark:  Connected to {config_data.url}", style="green")
    except TimeoutError:
        console.print(f":hourglass_done: Connection timed out.", style="logging.level.info")
    except Exception as err:
        connect_error(err)
    try:
        login_data = {"username": config_data.user, "password": config_data.password}
        login_response = sio.call("login", data=login_data)
        if isinstance(login_response, dict) and "ok" in login_response:
            console.print(f":white_heavy_check_mark:  Logged into {config_data.url}", style="green")
            login_response = SimpleNamespace(**login_response)
    except Exception as err:
        console.print(f":x:  Error: {err}", style="logging.level.error")
        exit(1)


@sio.event
def connect_error(data):
    console.print(f":x: Could not connect to server. Error: {data}", style="logging.level.error")
    exit(1)


def disconnect():
    try:
        sio.disconnect()
        console.print(f":boxing_glove: Disconnected from server.", style="green")
    except Exception as err:
        console.print(f":x:  Could not disconnect from server. Error: {err}", style="logging.level.error")
        exit(1)
