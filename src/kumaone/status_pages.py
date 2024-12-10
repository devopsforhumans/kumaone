#!/usr/bin/env python3

"""Status pages module for kumaone"""

# Import builtin python libraries
import json
import sys
import yaml

# Import external python libraries
from rich.console import Console
from rich.table import Table
import requests


# Import custom (local) python packages
from .event_handlers import get_event_data, wait_for_event
from . import ioevents
from .monitors import _check_monitor
from .payload_handler import _get_status_page_data_payload
from .settings import timeout
from .utils import _sio_call

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _get_status_page_public_group_list(public_group_list=None):
    """
    Generate public group list from monitor names

    :param public_group_list: (dict) Public group list dictionary
    :return: (list) Public group list of dictionary
    """

    # public_group_monitor_list = [
    #     {
    #         "name": "Services",
    #         "weight": 1,
    #         "monitorList": [
    #             {"id": 11}
    #         ]
    #     }
    # ]
    public_group_monitor_list = []
    if public_group_list is not None:
        for index, public_group in enumerate(public_group_list):
            public_group_monitor_item = {
                "name": public_group["name"],
                "weight": index + 1,
            }
            monitor_id_list = []
            for name in public_group["monitorList"]:
                monitor = _check_monitor(monitor_name_to_check=name)
                if monitor["exists"]:
                    monitor_id_list.append({"id": monitor["id"]})
            if monitor_id_list:
                public_group_monitor_item["monitorList"] = monitor_id_list
            public_group_monitor_list.append(public_group_monitor_item)
    return public_group_monitor_list


def list_status_pages(verbose=None, logger=None):
    """
    Show list of status pages.

    :param verbose: (bool) Enable verbose output.
    :param logger: (object) Logger object.
    :return: None
    """

    response = list(get_event_data(ioevents.status_page_list).values())
    logger.info(json.dumps(response, indent=4))
    console.print(f":hamburger: Available status pages.", style="green")
    table = Table("id", "slug", "Title")
    if not verbose:
        if response:
            for item in response:
                table.add_row(str(item["id"]), item["slug"], item["title"])
            if table.rows:
                console.print(table, style="green")
            else:
                console.print(f":four_leaf_clover: No data available.")
    else:
        console.print(json.dumps(response, indent=4, sort_keys=True), style="green")


def get_satus_page(slug=None, url=None, logger=None, show_details=False):
    """
    Get a status page by slug.

    :param slug: (str) Status page slug.
    :param url: (str) URL for uptime kuma server
    :param logger: (object) Logger object.
    :param show_details: (bool) Show details of the status page.
    :return: (dict) Python dictionary with status page info
    """

    event_response = _sio_call("getStatusPage", slug)

    try:
        http_response = requests.get(f"{url}/api/status-page/{slug}", timeout=timeout).json()
    except requests.exceptions.JSONDecodeError:
        console.print(f":cyclone: Response is not valid JSON.", style="logging.level.error")
        sys.exit(1)
    except requests.exceptions.Timeout:
        console.print(f":poodle: Response timed out.", style="logging.level.error")
        sys.exit(1)

    config = event_response["config"]
    config.update(http_response["config"])
    status_page_data = {
        **config,
        "incident": http_response["incident"],
        "publicGroupList": http_response["publicGroupList"],
        "maintenanceList": http_response["maintenanceList"],
    }
    # TODO: Check if we need to convert 'sendUrl' to boolean
    if show_details:
        console.print(f":page_facing_up: '{slug}' status page details", style="logging.level.info")
        console.print(f"{json.dumps(status_page_data, indent=4, sort_keys=True)}", style="logging.level.info")
    return status_page_data


def add_status_page(
    status_page_data_files=None, status_page_title=None, status_page_slug=None, logger=None, url=None, save=None
):
    """
    Creates/Adds/Updates a status page in uptime kuma.

    :param status_page_data_files: (Path) Status page config file location. File or Directory.
    :param status_page_title: (str) Title of the status page.
    :param status_page_slug: (str) Slug of the status page.
    :param logger: (object) Logger object for logging purposes.
    :param url: (str) URL of uptime kuma server
    :return: None.
    """

    if status_page_data_files:
        # console.print(Rule(style="purple"))
        for status_page_data_file in status_page_data_files:
            with open(status_page_data_file, "r") as tmp_data_file_read:
                status_pages = yaml.safe_load(tmp_data_file_read)["status_pages"]
                for status_page in status_pages:
                    logger.debug(status_page)
                    status_page_info = add_status_page(
                        status_page_title=status_page["title"].title(),
                        status_page_slug=status_page["slug"],
                        logger=logger,
                        url=url,
                    )
                    logger.debug(status_page_info)
                    if save:
                        if "ok" in status_page_info:
                            status_page_info.pop("ok")
                        if "msg" in status_page_info:
                            status_page_info.pop("msg")
                        status_page_info.update(status_page)
                        public_group_list = _get_status_page_public_group_list(status_page["publicGroupList"])
                        status_page_info["publicGroupList"] = public_group_list
                        status_page_data_to_save = _get_status_page_data_payload(**status_page_info)
                        logger.debug(status_page_data_to_save)
                        status_page_save_response = _sio_call("saveStatusPage", status_page_data_to_save)
                        if status_page_save_response["ok"]:
                            console.print(f":floppy_disk: Status page saved successfully!", style="logging.level.info")
                        else:
                            console.print(
                                f":cyclone: Status page ({status_page['slug']}) couldn't be saved. Error: {status_page_save_response.get('msg')}",
                                style="logging.level.error",
                            )
    else:
        status_page_info = _sio_call("getStatusPage", status_page_slug)
        if status_page_info["ok"]:
            status_page_details = get_satus_page(slug=status_page_slug, url=url, logger=logger)
            status_page_id = status_page_details["id"]
            console.print(
                f":sunflower: Status page '{status_page_id} - {status_page_title} ({status_page_slug})' already exists. Updating.",
                style="logging.level.info",
            )
            logger.debug(status_page_details)
            status_page_details.pop("incident")
            status_page_details.pop("maintenanceList")
            return status_page_details
        with wait_for_event(ioevents.status_page_list):
            response = _sio_call("addStatusPage", (status_page_title.title(), status_page_slug))
            if response["ok"]:
                console.print(
                    f":hatching_chick: Status page '{status_page_title.title()} ({status_page_slug})' has been created or updated.",
                    style="logging.level.info",
                )
                logger.debug(f"Status page creation response: {response}")
                return response
            else:
                console.print(f":red_circle: Error: {response['msg']}")
                sys.exit(1)
    # console.print(Rule(style="purple"))


def delete_status_page(status_page_data_files=None, status_page_slug=None, logger=None):
    """
    Deletes a status page from uptime kuma.

    :param status_page_data_files: (Path) Status page config file location. File or Directory.
    :param status_page_slug: (str) Slug of the status page.
    :param logger: (object) Logger object for logging purposes.
    :return: None.
    """

    # console.print(Rule(title="Delete Status Page", style="purple"))
    if status_page_data_files:
        for status_page_data_file in status_page_data_files:
            with open(status_page_data_file, "r") as tmp_data_file_read:
                status_pages = yaml.safe_load(tmp_data_file_read)["status_pages"]
                for status_page in status_pages:
                    delete_status_page(status_page_slug=status_page["slug"], logger=logger)
    elif status_page_slug:
        status_page_info = _sio_call("getStatusPage", status_page_slug)
        if status_page_info["ok"]:
            response = _sio_call("deleteStatusPage", status_page_slug)
            if response["ok"]:
                console.print(
                    f":wastebasket: Status page '{status_page_slug}' has been deleted.", style="logging.level.info"
                )
        else:
            console.print(
                f":orange_circle: Status page '{status_page_slug}' does not exist.", style="logging.level.info"
            )
