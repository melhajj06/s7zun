import sys
import json
import re
import webbrowser
from urllib import request
from winsdk_toast import Notifier, Toast
from winsdk_toast.event import EventArgsActivated


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


def on_click(args: EventArgsActivated) -> None:
    if not webbrowser.open("https://github.com/ip7z/7zip/releases/latest"):
        print("there was a problem opening the url 'https://github.com/ip7z/7zip/releases/latest'")
        sys.exit(1)
    sys.exit(0)


def send_toast(latest_version: str) -> None:
    notifier = Notifier("7-Zip Update Checker")
    toast = Toast()
    toast.add_text(f"A new version found for 7-Zip: {latest_version}")
    toast.add_action("Open URL")
    notifier.show(toast, handle_activated=on_click)


def check(path: str) -> bool:
    cv = get_current_version(path)
    lv = get_latest_version()

    if cv != lv:
        send_toast(lv)
        return True
    
    return False