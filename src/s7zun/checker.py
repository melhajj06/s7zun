import sys
import json
import re
import webbrowser
import asyncio
from urllib import request
from desktop_notifier import DesktopNotifier


def get_current_version(path: str) -> str:
    with open(path, 'r') as v:
        pattern = re.compile(r"(?<![\w\-\.])\d+(?:\.?\d+)*(?![\w\-\.])")
        line = v.readline()
        m = re.search(pattern, line)

        if m is None:
            print(f"no version info found in {path}\tis this a valid 7zip readme.txt?")
            sys.exit(1)
        
        return m.group(0)


def get_latest_version() -> str:
    with request.urlopen("https://api.github.com/repos/ip7z/7zip/releases/latest") as res:
        j = json.loads(res.read().decode("utf-8"))
        return j["name"]


async def send_toast(latest_version: str) -> None:
    clicked = asyncio.Event()

    def on_click() -> None:
        clicked.set()

        if not webbrowser.open("https://github.com/ip7z/7zip/releases/latest"):
            print("there was a problem opening the url 'https://github.com/ip7z/7zip/releases/latest'")
            sys.exit(1)

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


def check(path: str) -> bool:
    cv = get_current_version(path)
    lv = get_latest_version()

    if cv != lv:
        asyncio.run(send_toast(lv))
        return True
    
    return False