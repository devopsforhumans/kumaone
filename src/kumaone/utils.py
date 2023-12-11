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
def debug_manager():
    """This function acts accordingly with --debug switch"""

    try:
        from http.client import HTTPConnection
    except ImportError:
        console.print(f":x: Can't import http client", style="logging.level.error")
        sys.exit(1)
    console.print(f":beetle: DEBUG mode is ON.", style="logging.keyword")
    debug_format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    HTTPConnection.debuglevel = 4
    logging.basicConfig(
        level="NOTSET",
        format=debug_format,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    log = logging.getLogger("kumaone")
    log.setLevel(logging.DEBUG)
    log.propagate = True
    return log


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
