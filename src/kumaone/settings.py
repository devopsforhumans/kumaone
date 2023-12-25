#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings module for kumaone"""

# Import custom (local) python packages
from . import ioevents as event

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

event_data = {
    event.api_key_list: None,
    event.auto_login: None,
    event.avg_ping: None,
    event.cert_info: None,
    event.connect: None,
    event.disconnect: None,
    event.docker_host_list: None,
    event.heartbeat: None,
    event.heartbeat_list: None,
    event.important_heartbeat_list: None,
    event.info: None,
    event.init_server_timezone: None,
    event.maintenance_list: None,
    event.monitor_list: None,
    event.notification_list: None,
    event.proxy_list: None,
    event.status_page_list: None,
    event.uptime: None,
}

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

monitor_events = ["avgPing", "uptime", "heartbeatList", "importantHeartbeatList", "certInfo", "heartbeat"]

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
