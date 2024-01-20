#!/usr/bin/env python3

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

timeout = 10


def required_arguments_by_type(monitor_type=None):
    """
    Returns minimum required arguments by event type
    :param monitor_type: (str) Name of the event type
    :return:
    """

    required_arguments = {
        "dns": ["hostname", "dns_resolve_server", "port"],
        "docker": ["docker_container", "docker_host"],
        "gamedig": ["game", "hostname", "port"],
        "group": [],
        "grpc-keyword": ["grpcUrl", "keyword", "grpcServiceName", "grpcMethod"],
        "http": ["url", "maxredirects"],
        "json-query": ["url", "jsonPath", "expectedValue"],
        "kafka-producer": ["kafkaProducerTopic", "kafkaProducerMessage"],
        "keyword": ["url", "keyword", "maxredirects"],
        "mongodb": [],
        "mqtt": ["hostname", "port", "mqttTopic"],
        "mysql": [],
        "ping": ["hostname"],
        "port": ["hostname", "port"],
        "postgres": [],
        "push": [],
        "radius": [],
        "real-browser": ["hostname", "port"],
        "redis": [],
        "sqlserver": [],
        "stream": ["hostname", "port"],
        "tailscale-ping": ["hostname"],
    }

    return required_arguments[monitor_type] + ["name", "type"]


def get_missing_arguments(input_data=None):
    """
    Finds missing argument key from input based on required argument keys for monitors

    :param input_data: (dict) Monitor payload keys with values
    :return: (list) Missing keys as list or empty list if all required arguments are provided
    """

    required_argument_keys = required_arguments_by_type(monitor_type=input_data["type"])
    missing_arguments = []
    for required_argument in required_argument_keys:
        if input_data.get(required_argument) is None:
            missing_arguments.append(required_argument)
    return missing_arguments
