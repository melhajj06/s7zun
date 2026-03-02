import os
import sys
import logging
import datetime
from .checker import check
from .checker import ExecutionCodes
from enum import Enum


class ExitCodes(Enum):
    """Possible exit codes for this package when executed from __main__
    """
    SUCCESS = 0
    INVALID_USAGE = 1
    INVALID_7Z_DIRECTORY = 2
    INVALID_LOG_DIRECTORY = 3
    EXECUTION_FAILURE = 4


def setup_logger(logs_dir: str) -> bool:
    """Sets up the logging path and config

    :param str logs_dir: the directory in which to create log files
    """
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    if not os.path.isdir(logs_dir):
        return False

    date = datetime.datetime.now().date().strftime(r"%Y-%m-%d")
    time = datetime.datetime.now().time().strftime(r"%H-%M-%S")
    filename = os.path.join(logs_dir, f"{date}_{time}_sz7un.log")

    logging.basicConfig(
        filename=filename,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=logging.INFO,
        encoding="utf-8"
    )

    return True


def main(argv: list[str]) -> ExitCodes:
    """Main function to begin execution

    :param list[str] argv: command line arguments
    """
    logs_dir = os.path.join(os.getcwd(), "logs")

    if len(argv) == 3:
        logs_dir = os.path.abspath(argv[2])
    elif len(argv) != 2:
        print("usage: python -m s7zun 'path/to/7-Zip/installation' ['path/to/logs/directory']")
        return ExitCodes.INVALID_USAGE

    sz_dir = os.path.abspath(argv[1])

    if not setup_logger(logs_dir):
        return ExitCodes.INVALID_LOG_DIRECTORY

    if not os.path.isdir(sz_dir):
        logging.getLogger(__name__).error(f"'{sz_dir}' is not a valid directory")
        return ExitCodes.INVALID_7Z_DIRECTORY
    
    exit_code = check(sz_dir)

    if exit_code == ExecutionCodes.VERSION_NOT_FOUND:
        return ExitCodes.EXECUTION_FAILURE
    else:
        return ExitCodes.SUCCESS


if __name__ == "__main__":
    exit_status = main(sys.argv)
    logging.getLogger(__name__).info(f"Process exiting with exit status '{exit_status}={exit_status.value}'")
    sys.exit(exit_status.value)