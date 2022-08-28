#!/usr/bin/env python3

"""
usage: python3 py/0901a.py [--h] [--]

show 3 threads interleaving prints of randomly delayed lines

examples:
    python3.py py/0901a.py  # show these examples
    python3.py py/0901a.py --
"""


import os
import pdb
import random
import sys
import threading
import time

_ = pdb


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)  # one up from "py/"
BIN_DIR = os.path.join(TOP_DIR, "bin")

try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo

_ = byo


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    thread_0 = threading.Thread(target=main_0)
    thread_1 = threading.Thread(target=main_1)
    thread_2 = threading.Thread(target=main_2)

    threads = (thread_0, thread_1, thread_2)

    print("midway main")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("exit main")


def main_0():
    for _ in range(3):
        time.sleep(2 * random.random())
        print("main_0")


def main_1():
    for _ in range(3):
        time.sleep(2 * random.random())
        print("main_1")


def main_2():
    for _ in range(3):
        time.sleep(2 * random.random())
        print("main_2")


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0901a.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
