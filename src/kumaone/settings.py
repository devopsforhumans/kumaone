#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings module for kumaone"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
from rich.console import Console
from rich import print
import typer
from typing_extensions import Annotated

# Import custom (local) python packages
from .utils import log_manager, app_info

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

accepted_status_codes = ["200-299"]

authentication_methods = [
    "basic",
    "mtls",
    "none",
    "ntlm",
    "oauth2-cc",
]

docker_engine_connection_types = ["socket", "tcp"]

incident_styles = [
    "danger",
    "dark",
    "info",
    "light",
    "primary",
    "warning",
]

maintenance_strategies = [
    "cron",
    "manual",
    "recurring-interval",
    "recurring-weekday",
    "recurring-day-of-month",
    "single",
]

monitor_status_mapping = {"down": 0, "maintenance": 3, "pending": 2, "up": 1}

monitor_types = [
    "dns",
    "docker",
    "gamedig",
    "group",
    "grpc-keyword",
    "http",
    "json-query",
    "kafka-producer",
    "keyword",
    "mongodb",
    "mqtt",
    "mysql",
    "ping",
    "port",
    "postgres",
    "push",
    "radius",
    "real-browser",
    "redis",
    "sqlserver",
    "stream",
    "tailscale-ping",
]

proxy_protocols = ["http", "https", "socks", "socks4", "socks5", "socks5h"]
