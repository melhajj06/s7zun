# 7-Zip Update Notifier
## s7zun

This is a simple [Python](https://www.python.org/) package that checks for [7-Zip](https://7-zip.org/) updates

## Usage

Install via [pip](https://pypi.org/project/pip/) using: `pip install git+https://github.com/melhajj06/s7un@2025.1` (see [this](https://stackoverflow.com/questions/20101834/pip-install-from-git-repo-branch) for more details)\
The main script takes a single command line argument: the path to the 7-Zip installation\
**Example:** `s7zun "path/to/7-Zip"`

## Dependencies
- [Desktop Notifier](https://pypi.org/project/desktop-notifier/)

## Remarks
This can easily be ran on startup using a batch script along with the Task Scheduler or by placing the script in the startup folder (Windows):
```bat
@echo off

cd /d "%~dp0"
call ".venv\scripts\activate.bat"
python -m s7zun "path/to/7-Zip"
call "deactivate.bat"
exit /b 0
```