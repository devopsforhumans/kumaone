#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility module for kumaone"""

# Import builtin python libraries
from datetime import datetime
import logging
import sys

# Import external python libraries
from rich import print
from rich.console import Console
from rich.logging import RichHandler

# Import custom (local) python packages
from .connection import sio
from src.kumaone.__about__ import __author__ as author
from src.kumaone.__about__ import __copy_right__ as app_copy_right
from src.kumaone.__about__ import __home_page__ as homepage
from src.kumaone.__about__ import __license__ as app_license
from src.kumaone.__about__ import __version__ as version

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


# Turn on/off logging visibility
def log_manager(log_level=None):
    """
    This function acts accordingly with --debug switch

    :param log_level: (str) Log level
    :return: (object) logger
    """

    if log_level is None or log_level == "NOTSET":
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        return logger
    else:
        log_format = "[%(funcName)s()] %(message)s"
        logging.basicConfig(
            level="NOTSET", format=log_format, datefmt="[%m-%d-%Y %X]", handlers=[RichHandler(rich_tracebacks=True)]
        )
        level = logging.getLevelName(f"{log_level}".upper())
        if not log_level.upper().startswith("W"):
            console.print(f":beetle: {log_level} mode is ON.".upper(), style="logging.keyword")
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        logger.propagate = True
        return logger


def app_info(log_level=None):
    """
    Shows application information

    :param log_level: (str) Log levels
    :return: application information
    """

    length = 60
    logger = log_manager(log_level=log_level)

    logger.info(f"Please check github repository for updated info.")
    print("=" * length)
    print(f":hatching_chick: Author: {author}")
    print(f":penguin: Version: {version}")
    print(f":memo: License: {app_license}")
    print(f":link: Home: {homepage}")
    print(f":copyright: Copyright: {app_copy_right}")
    print("=" * length)


def _sio_call(event=None, data=None):
    """
    Calls socketIO event

    :param event: (str) Event name.
    :param data: (any) Event related data.
    :return: (any)
    """

    try:
        response = sio.call(event, data=data)
    except TimeoutError:
        console.print(f":hourglass:  Request timed out while waiting for '{event}' event.", style="logging.level.info")
        sys.exit(1)
    if isinstance(response, dict):
        if not response["ok"]:
            console.print(f":point_right: Error! {response.get('msg')}", style="logging.level.error")
            sys.exit(1)
    return response
    # try:
    #     json_response = json.load(response)
    #     if not json_response["ok"]:
    #         console.print(f":point_right: Error: {json_response.get('msg')}")
    #     return json_response
    # except ValueError as err:
    #     console.print(f":dizzy_face: Response is not JSON serializable.", style="logging.level.error")
    #     console.print(f":point_right: Error: {err}")
