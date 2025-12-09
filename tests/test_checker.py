import s7zun.checker
import os

def test_checker():
    path = os.path.join(os.getcwd(), "tests\\test_readme.txt")
    assert(s7zun.checker.check(path) is True)