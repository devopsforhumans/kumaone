#!/usr/bin/env python3

"""Utility module for kumaone"""

# Import builtin python libraries
import logging
import os
from pathlib import Path
import sys
import yaml

# Import external python libraries
from rich import print
from rich.console import Console
from rich.logging import RichHandler
import typer

# Import custom (local) python packages
from .connection import sio
from src.kumaone.__about__ import __author__ as author
from src.kumaone.__about__ import __copyright__ as app_copy_right
from src.kumaone.__about__ import __home_page__ as homepage
from src.kumaone.__about__ import __license__ as app_license
from src.kumaone.__about__ import __version__ as version

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def version_callback(value: bool):
    if value:
        print(f"{version}")
        raise typer.Exit()


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

    logger = log_manager(log_level=log_level)

    logger.info(f"Please check github repository for updated info.")
    # console.print(Rule(style="purple"))
    print(f":hatching_chick: Author: {author}")
    print(f":penguin: Version: {version}")
    print(f":memo: License: {app_license}")
    print(f":link: Home: {homepage}")
    print(f":copyright: Copyright: {app_copy_right}")
    # console.print(Rule(style="purple"))


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
    # if isinstance(response, dict):
    #     if not response["ok"]:
    #         console.print(f":orange_circle: {response.get('msg')}", style="logging.level.warning")
    #         # sys.exit(1)
    return response
    # try:
    #     json_response = json.load(response)
    #     if not json_response["ok"]:
    #         console.print(f":red_circle: Error: {json_response.get('msg')}")
    #     return json_response
    # except ValueError as err:
    #     console.print(f":dizzy_face: Response is not JSON serializable.", style="logging.level.error")
    #     console.print(f":red_circle: Error: {err}")


def _check_data_path(data_path=None, logger=None, key_to_check_for=None):
    """
    Checks data path for monitor input file or directory

    :param data_path: (Path) uptime kuma input data.
    :param logger: (object) logger object.
    :param key_to_check_for: (str) What type of data should be checked.
    :return: (int) Monitor ID.
    """

    # console.print(Rule(style="purple"))
    console.print(f":clipboard: Checking input data path.", style="logging.level.info")
    if Path(data_path).exists():
        if Path(data_path).is_dir():
            logger.info(f"{data_path} is a directory. All yaml files in this directory will be considered.")
            console.print(
                f":file_folder: Directory input detected. Input file directory: '{data_path}'.",
                style="logging.level.info",
            )
            with os.scandir(Path(data_path)) as items:
                data_files = []
                skipped_files = []
                for item in items:
                    if item.is_file():
                        file_type = item.name.split(".")[-1]
                        if file_type in ["yaml", "yml"]:
                            logger.info(f"{item.name} - {item.stat().st_size} bytes.")
                            with open(item) as tmp_read_file:
                                raw_data = yaml.safe_load(tmp_read_file)
                                logger.debug(raw_data)
                                if key_to_check_for in raw_data:
                                    data_files.append(Path(data_path).joinpath(item.name))
                                else:
                                    logger.info(f"{item.name} did not have {key_to_check_for}, skipped.")
                                    pass
                        else:
                            console.print(
                                f":bulb: '.{file_type}' file type is not supported. Skipping '{item.name}'. ",
                                style="logging.level.info",
                            )
                            skipped_files.append(Path(data_path).joinpath(item.name))
                    else:
                        console.print(
                            f":card_index_dividers: Nested directories are not supported. Skipping '{item.name}'.",
                            style="logging.level.info",
                        )
            console.print(
                f":high_brightness: {len(data_files)} files found in supported format.",
                style="logging.level.info",
            )
            logger.debug(f"{data_files}")
            logger.debug(f"{skipped_files}")
            return sorted(data_files)
        elif Path(data_path).is_file():
            logger.info(f"'{data_path}' is a file.")
            console.print(
                f":high_brightness: Single file input detected. Input file: '{data_path}'.", style="logging.level.info"
            )
            with open(data_path) as tmp_read_file:
                raw_data = yaml.safe_load(tmp_read_file)
                logger.debug(raw_data)
                logger.debug(key_to_check_for)
                if key_to_check_for in raw_data:
                    return sorted([data_path])
                else:
                    console.print(
                        f":orange_circle: Provided data file is missing necessary data. Missing {key_to_check_for} key.",
                        style="logging.level.warning",
                    )
                    sys.exit(1)
    else:
        console.print(f":x:  Data path: '{data_path}', does not exists!", style="logging.level.error")
        sys.exit(1)


def _mutual_exclusivity_check(size=None):
    """
    Checks mutual exclusivity
    :param size: (int) size of the group
    :return: None
    """

    group = set()

    def callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in group:
            group.add(param.name)
        if len(group) > size - 1:
            raise typer.BadParameter(f"{param.name} is mutually exclusive with {group.pop()}")
        return value

    return callback
