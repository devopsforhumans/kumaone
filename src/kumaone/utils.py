#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility module for kumaone"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
from rich.console import Console
from rich.logging import RichHandler
from rich import print

# Import custom (local) python packages
from .__about__ import __version__ as version
from .__about__ import __author__ as author
from .__about__ import __license__ as app_license
from .__about__ import __home_page__ as homepage
from .__about__ import __copy_right__ as app_copy_right

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


# Turn on/off debugging
def debug_manager(log_level=None):
    """
    This function acts accordingly with --debug switch

    :param log_level: (str) Log level
    :return: (object) logger
    """

    if log_level is not None:
        log_format = "[%(funcName)s()] %(message)s"
        logging.basicConfig(
            level="NOTSET",
            format=log_format,
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        level = logging.getLevelName(f"{log_level}".upper())
        console.print(f":beetle: {log_level} mode is ON.".upper(), style="logging.keyword")
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        logger.propagate = True
        return logger
    else:
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        return logger


def app_info():
    """
    Shows application information

    :return: application information
    """

    print("=" * 50)
    print(f":hatching_chick: Author: {author}")
    print(f":penguin: Version: {version}")
    print(f":memo: License: {app_license}")
    print(f":link: Home: {homepage}")
    print(f":copyright: Copyright: {app_copy_right}")
    print("=" * 50)
