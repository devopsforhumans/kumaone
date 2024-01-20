#!/usr/bin/env python3

"""Event handler module for kumaone"""

# Import builtin python libraries
from contextlib import contextmanager
from copy import deepcopy
import time

# Import external python libraries
from rich.console import Console
from socketio.exceptions import TimeoutError

# Import custom (local) python packages
from . import ioevents
from .settings import event_data, monitor_events

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


@contextmanager
def wait_for_event(event):
    """
    Waits for event

    :param event: (str) SocketIO event name.
    :return: None
    """

    try:
        yield
    except:
        raise
    else:
        timestamp = time.time()
        while event_data[event] is None:
            if time.time() - timestamp > 30:
                raise TimeoutError("Event response timed out.")
            time.sleep(0.01)


def get_event_data(event):
    """
    Get event data

    :param event: (event) socketIO event
    :return: (dict) socketIO event data
    """

    timestamp = time.time()
    while event_data[event] is None:
        if time.time() - timestamp > 30:
            raise TimeoutError("Event response timed out.")
        if event_data[event] == {} and event in monitor_events:
            return []
        time.sleep(0.01)
    time.sleep(0.2)
    return deepcopy(event_data[event].copy())


def connect_event():
    """
    Connect event handler

    :return:
    """

    pass


def disconnect_event():
    """
    Disconnect event handler

    :return: None
    """

    pass


def monitor_list_event(data):
    """
    Get all the monitors

    :param data: (dict) Event data.
    :return: None
    """

    event_data[ioevents.monitor_list] = data


def status_page_list_event(data):
    """
    Get all the status pages

    :param data: (dict) Event data.
    :return: None
    """

    event_data[ioevents.status_page_list] = data


def notification_list_event(data):
    """
    Get all notification processes

    :param data: (dict) Event data
    :return: None
    """

    event_data[ioevents.notification_list] = data
