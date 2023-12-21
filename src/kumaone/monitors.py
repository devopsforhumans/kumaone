#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Monitors module for kumaone"""

# Import builtin python libraries
from copy import deepcopy
import json
from pathlib import Path
import time
from types import SimpleNamespace

# Import external python libraries
from rich.console import Console
import socketio
from socketio.exceptions import TimeoutError


# Import custom (local) python packages
from .config import ConfigActions, check_config, create_config, delete_config, edit_config
from .event_handlers import get_event_data
from .settings import event_data, monitor_events
from .utils import app_info, log_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"


def get_monitors():
    response = list(get_event_data("monitorList").values())
    print(json.dumps(response, indent=4))
