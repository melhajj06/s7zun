import os
import sys
from checker import check


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("usage: python -m 7zun 'path/to/7zip/installation'")
        sys.exit(1)

    path = os.path.join(args[1], "readme.txt")

    if not os.path.isfile(path):
        print(f"{path} is not a valid path")
        sys.exit(1)
    
    check(path)