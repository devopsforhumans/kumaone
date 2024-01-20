#!/usr/bin/env python3

"""Connection module for kumaone"""

# Import builtin python libraries
import sys

# Import builtin python libraries
from types import SimpleNamespace

# Import external python libraries
from rich.console import Console

import socketio
from socketio.exceptions import TimeoutError

# Import custom (local) python packages
from .event_handlers import (
    connect_event,
    disconnect_event,
    monitor_list_event,
    notification_list_event,
    status_page_list_event,
)
from . import ioevents

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()
sio = socketio.Client(logger=False, engineio_logger=False)
monitor_list_data = None


def _register_event_handlers():
    """
    Registers event handlers

    :return: None
    """

    # sio.on(ioevents.api_key_list, api_key_list_event)
    # sio.on(ioevents.auto_login, auto_login_event)
    # sio.on(ioevents.avg_ping, avg_ping_event)
    # sio.on(ioevents.cert_info, cert_info_event)
    sio.on(ioevents.connect, connect_event)
    sio.on(ioevents.disconnect, disconnect_event)
    # sio.on(ioevents.docker_host_list, docker_host_list_event)
    # sio.on(ioevents.heartbeat, heartbeat_event)
    # sio.on(ioevents.heartbeat_list, heartbeat_list_event)
    # sio.on(ioevents.important_heartbeat_list, important_heartbeat_list_event)
    # sio.on(ioevents.info, info_events)
    # sio.on(ioevents.init_server_timezone, init_server_timezone_event)
    # sio.on(ioevents.maintenance_list, maintenance_list_event)
    sio.on(ioevents.monitor_list, monitor_list_event)
    sio.on(ioevents.notification_list, notification_list_event)
    # sio.on(ioevents.proxy_list, proxy_list_event)
    sio.on(ioevents.status_page_list, status_page_list_event)
    # sio.on(ioevents.uptime, uptime_event)


def connect_login(config_data=None, headers=None):
    """
    Connects to uptime kuma server

    :param config_data: (dict) Uptime kuma server configs
    :param headers: (dict) Custom headers
    :return: (event) Connection event to uptime kuma server
    """

    try:
        # console.print(Rule(title="Connect", style="purple"))
        _register_event_handlers()
        sio.connect(config_data.url, headers=headers)
        console.print(f":pretzel: Connected to {config_data.url}", style="logging.level.info")
    except TimeoutError:
        console.print(f":hourglass_done: Connection timed out.", style="logging.level.info")
    except Exception as err:
        connect_error(err)
    try:
        login_data = {"username": config_data.user, "password": config_data.password}
        login_response = sio.call("login", data=login_data)
        if isinstance(login_response, dict) and "ok" in login_response:
            console.print(f":locked_with_key: Successfully logged in.", style="green")
            login_response = SimpleNamespace(**login_response)
    except Exception as err:
        console.print(f":x:  Error: {err}", style="logging.level.error")
        sys.exit(1)


@sio.event
def connect_error(data):
    console.print(f":x: Could not connect to server. Error: {data}", style="logging.level.error")
    sys.exit(1)


def disconnect():
    # console.print(Rule(title="Disconnect", style="purple"))
    try:
        sio.disconnect()
        console.print(f":firecracker: Disconnected from server.", style="logging.level.info")
    except Exception as err:
        console.print(f":x:  Could not disconnect from server. Error: {err}", style="logging.level.error")
        sys.exit(1)
