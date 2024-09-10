#!/usr/bin/env python3

"""Config module for kumaone"""

# Import builtin python libraries
from pathlib import Path
import sys
from types import SimpleNamespace
import yaml

# Import external python libraries
from rich.console import Console
from rich.prompt import Prompt
import validators

# Import custom (local) python packages
from src.kumaone.utils import log_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()

kuma_config_default_locations = [
    Path.home().joinpath(".config/kumaone/kuma.yaml"),
    Path.home().joinpath("kuma.yaml"),
    "./kuma.yaml",
    "/etc/kumaone/kuma.yaml",
]


def __write_config_file(data_to_write=None, file_path=None):
    """
    Writes data to configuration file.

    :param data_to_write: (dict) Data to write to configuration file.
    :param file_path: (Path) File path to write configuration data.
    :return: (file) Creates a file in file system.
    """

    try:
        with open(file_path, "w") as kuma_config:
            yaml.safe_dump(data_to_write, kuma_config)
            return True
    except Exception as err:
        console.print(f":x: {err} Exception occurred.", style="logging.level.error")
        sys.exit(1)


def check_config(config_path=None, log_level=None, logger=None, get_url=False):
    """
    Checks for uptime kuma config

    :param config_path: (Path) configuration yaml file path
    :param log_level: (str) Log level
    :param logger: (object) Logger object for logging
    :param get_url: (bool) Get uptime kuma url
    :return: (object) Python SimpleNamespace object with the config
    """

    if logger is None:
        logger = log_manager(log_level=log_level)
    else:
        logger = logger

    if config_path is None or not config_path:
        for item in kuma_config_default_locations:
            config_file = Path(item)
            logger.info(f"Looking for uptime kuma config file at: {config_file}")
            if Path.exists(config_file):
                if Path.is_file(config_file):
                    return check_config(config_path=config_file, logger=logger, get_url=get_url)
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
                    logger.info(f"Config file {config_file} found!")
                    logger.debug(f"{config_data}")
                console.print(f":partying_face: Uptime kuma config file found at: {config_file}", style="green")
                return SimpleNamespace(**config_data["kuma"])
            else:
                logger.error(f"Config path is not a file.")
                console.print(f":x: {config_file} is not a file.", style="red")
                sys.exit(1)
        else:
            logger.error(f"Provided config path doesn't exist.")
            console.print(f":x: {config_file} doesn't exist.", style="red")
            sys.exit(1)


def create_config(config_path=None, log_level=None):
    """
    Create a new config for kumaone with necessary info about uptime kuma

    :param config_path: (Path) Custom configuration path.
    :param log_level: (str) Log level
    :return: (file) Cerates a file with configuration
    """

    logger = log_manager(log_level=log_level)

    logger.info(f"Provided location: {config_path}")
    config_data = {}
    if config_path is None or not config_path:
        logger.info(f"Provided config path is either empty or set to None.")
        console.print(
            f":bear: No custom config path provided. Default path will be used for configuration.",
            style="logging.level.info",
        )
        config_file_path = kuma_config_default_locations[0]
    else:
        logger.info(f"Custom config path provided.")
        console.print(
            f":teddy_bear: Custom config path provided. {config_path} will be used for configuration.",
            style="logging.level.info",
        )
        config_file_path = config_path
    logger.info(f"Uptime kuma configuration will be written in: {config_file_path}")
    console.print(f":honey_pot: Creating config file at: {config_file_path}", style="logging.level.info")
    while True:
        config_data["url"] = Prompt.ask(":link: Uptime kuma URL (https://example.com)")
        if validators.url(config_data["url"]):
            logger.info("URL syntax is valid.")
            break
        else:
            console.print(":lying_face: Invalid URL syntax.", style="prompt.invalid")
    config_data["user"] = Prompt.ask(":goat: Uptime kuma username")
    config_data["password"] = Prompt.ask(":see_no_evil: Uptime kuma password", password=True)

    parent_directory = Path(config_file_path).parent
    config_data_to_write = {"kuma": config_data}

    if parent_directory.exists():
        logger.info(f"Parent directory {parent_directory} exists. Creating config file.")
        console.print(":file_folder: Parent directory exists.", style="logging.level.info")
        console.print(f":pencil: Creating configuration file.", style="logging.level.info")
        if __write_config_file(data_to_write=config_data_to_write, file_path=config_file_path):
            logger.info("Configuration file creation was successful.")
            console.print(f":white_heavy_check_mark:  Successfully created the configuration file!", style="green")
    else:
        logger.info(f"Parent directory {parent_directory} doesn't exist. The directory will be created.")
        console.print(
            f":file_folder: Parent directory doesn't exist. {parent_directory} directory will be created.",
            style="logging.level.info",
        )
        try:
            Path(parent_directory).mkdir(parents=True, exist_ok=True)
            console.print(f":open_file_folder: Successfully created {parent_directory} directory.", style="green")
            console.print(f":pencil: Creating configuration file.", style="logging.level.info")
            if __write_config_file(data_to_write=config_data_to_write, file_path=config_file_path):
                logger.info("Configuration file creation was successful.")
                console.print(f":white_heavy_check_mark:  Successfully created the configuration file!", style="green")
        except Exception as err:
            logger.error(f"{err} exception occurred.")
            console.print(f":x: {err} exception occurred.", style="logging.level.error")
            sys.exit(1)


def delete_config(config_path=None, remove_parent=False, log_level=None):
    """
    Delete uptime kuma config

    :param config_path: (Path) Custom configuration path.
    :param remove_parent: (boolean) Remove parent directory if True. Default is False.
    :param log_level: (str) Log level
    :return: None
    """

    logger = log_manager(log_level=log_level)

    logger.info(f"Deleting {config_path} configuration file.")
    files_to_delete = []
    if config_path is None or not config_path:
        logger.info("Empty config path provided.")
        console.print(
            f":zipper-mouth_face: Empty config path provided. Looking for default config file.",
            style="logging.level.info",
        )
        for item in kuma_config_default_locations:
            if Path(item).exists():
                logger.info(f"Config file found at: {item}")
                files_to_delete.append(item)
    else:
        if Path(config_path).exists():
            logger.info(f"Config file found at: {config_path}")
            files_to_delete.append(config_path)
        else:
            logger.info(f"Provided config file doesn't exist!")
            console.print(
                f":lollipop: Provided config file path doesn't exist. Nothing to delete.", style="logging.level.info"
            )
            sys.exit(0)
    if not files_to_delete:
        logger.info(f"No config file found.")
        console.print(f":lollipop: No config file found. Nothing to delete.", style="logging.level.info")
        sys.exit(0)
    else:
        for item in files_to_delete:
            console.print(f":llama: Deleting {item} file.", style="logging.level.info")
            try:
                Path.unlink(item, missing_ok=True)
                logger.info(f"File {item} removed.")
                console.print(f":watermelon: File {item} has been deleted.", style="green")
            except Exception as err:
                console.print(f":x: Exception occurred. ERROR: {err}", style="logging.level.error")
                logger.error(f"{err}")
                sys.exit(1)
