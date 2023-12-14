#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Config module for kumaone"""

# Import builtin python libraries
from enum import Enum
from pathlib import Path

# Import external python libraries
from rich.console import Console
from rich import print
import yaml

# Import custom (local) python packages
from .utils import log_manager

console = Console()

kuma_config_default_locations = ["~/.config/kumaone/kuma.conf", "~/kuma.conf", "./kuma.conf", "/etc/kumaone/kuma.conf"]


class ConfigActions(str, Enum):
    """
    Configuration actions
    """

    create = "create"
    delete = "delete"
    edit = "edit"
    show = "show"


def check_config(config_path=None, log_level=None):
    """
    Checks for uptime kuma config

    :param config_path: (Path) configuration yaml file path
    :param log_level: (str) Log level
    :return: (object) Python dictionary object with the config
    """

    logger = log_manager(log_level=log_level)

    if config_path is None or not config_path:
        config_file_found = False
        for item in kuma_config_default_locations:
            config_file = Path(item)
            logger.info(f"Looking for uptime kuma config file at: {config_file}")
            if Path.exists(config_file):
                if Path.is_file(config_file):
                    console.print(f":white_check_mark: Uptime kuma config file found at: {config_file}", style="green")
                    config_file_found = True
                    check_config(config_path=config_file)
                    break
        if not config_file_found:
            logger.critical(f"Config file not found.")
            console.print(f":x: Sorry! We couldn't find the config file.", style="logging.level.critical")
            console.print(
                f":speak_no_evil: Please run 'kumaone config --action create' to create a new config file.",
                style="logging.level.info",
            )
    else:
        config_file = Path(config_path)
        if Path.exists(config_file):
            if Path.is_file(config_file):
                with open(config_file, "r") as kuma_config:
                    config_data = yaml.safe_load(kuma_config)
                    console.print(f":white_check_mark: Uptime kuma config file found at: {config_file}", style="green")
                    logger.info(f"Config file [{config_file}] found!")
                    logger.info(f"{config_data}")
                return config_data
            else:
                logger.error(f"Config path is not a file.")
                console.print(f":x: {config_file} is not a file.", style="red")
                exit(1)
        else:
            logger.error(f"Provided config path doesn't exists.")
            console.print(f":x: {config_file} doesn't exists.", style="red")
            exit(1)
