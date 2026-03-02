import sys
import json
import re
import webbrowser
import asyncio
import subprocess
import logging
from urllib import request
from desktop_notifier import DesktopNotifier
from enum import Enum


logger = logging.getLogger(__name__)


class ExecutionCodes(Enum):
    """Possible return codes for this module's entry point :func:`s7zun.checker.check`
    """
    UP_TO_DATE = 0
    VERSION_NOT_FOUND = 1
    MISMATCHED_VERSIONS = 2
    FAILED_TO_OPEN_WEBPAGE = 3


def get_current_version(path: str) -> str:
    """Gets the current version of 7-Zip from the installation's binary

    ``path`` must be a valid 7-Zip installation folder where the binary ``7z.exe`` exists.
    When running ``7z.exe``, the expected output is a help menu that contains the installed 7-Zip version at the top.

    "7-Zip xx.xx ..." where "xx.xx" is the version

    :param str path: path to 7-Zip installation
    :return str: the current version of 7-Zip installed
    """
    pattern = re.compile(r"7-Zip (\b\d+(?:(?:\.\d+)?)*\b)")

    try:
        result = subprocess.run(path + r"/7z.exe", capture_output=True, text=True, check=True)

        m = re.search(pattern, result.stdout)

        if m:
            current_version = m.group(1)
            logger.info(f"Current 7-Zip version found: '{current_version}'")
            return current_version
        else:
            logger.error("7-Zip version could not be found from command output")
            return ""
    except subprocess.CalledProcessError:
        logger.error("7-Zip command '7z.exe' exited with non-zero exit status", exc_info=True)
    except FileNotFoundError:
        logger.error(f"7-Zip command '7z.exe' was not found in '{path}'", exc_info=True)
    
    return ""


def get_latest_version() -> str:
    """Gets the latest version of 7-Zip posted on the `7-Zip GitHub <https://github.com/ip7z/7zip/>`_

    :return str: the latest version of 7-Zip
    """
    with request.urlopen("https://api.github.com/repos/ip7z/7zip/releases/latest") as res:
        j = json.loads(res.read().decode("utf-8"))
        logger.info(f"Latest 7-Zip version found: '{j["name"]}'")
        return j["name"]


async def send_toast(latest_version: str) -> None:
    """Sends a desktop notification (toast) notifying the user of a new 7-Zip version

    The notification is clickable and will open the `latest release <github.com/ip7z/7zip/releases/latest>`_ page on GitHub for 7-Zip

    :param str latest_version: the latest version of 7-Zip
    """
    clicked = asyncio.Event()

    # click callback that opens the latest 7-Zip version in GitHub
    def on_click() -> None:
        clicked.set()

        if not webbrowser.open("https://github.com/ip7z/7zip/releases/latest"):
            logger.warning("Failed to open latest release of 7-Zip at 'https://github.com/ip7z/7zip/releases/latest'")
            sys.exit(ExecutionCodes.FAILED_TO_OPEN_WEBPAGE.value)

    notifier = DesktopNotifier("7-Zip Update Notifier")

    await notifier.send(
        title="New Version",
        message=f"A new version was found for 7-Zip: {latest_version}",
        timeout=5,
        on_clicked=on_click
    )

    try:
        await asyncio.wait_for(clicked.wait(), timeout=25)
    except asyncio.TimeoutError:
        pass


def check(path: str) -> ExecutionCodes:
    """Checks if the currently installed 7-Zip is up-to-date

    :param str path: path to 7-Zip installation
    :return bool: ``True`` if the currently installed 7-Zip is up-to-date
    """
    cv = get_current_version(path)

    if cv == "":
        return ExecutionCodes.VERSION_NOT_FOUND

    lv = get_latest_version()

    if cv != lv:
        asyncio.run(send_toast(lv))
        logger.info("Sent toast")
        return ExecutionCodes.MISMATCHED_VERSIONS
    
    return ExecutionCodes.UP_TO_DATE