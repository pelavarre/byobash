#!/usr/bin/env python3

"""
usage: python3 py/0901b.py [--h] [--]

examples:
    python3.py py/0901b.py --
"""


import os
import pdb
import subprocess
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

    main.buffer = None
    main.lines = list()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def main_0():
    """Print Lines into Stdout"""

    while True:

        if main.lines:
            line = main.lines.pop(0)
            print(line)

        time.sleep(0.100)


def main_1():
    """Copy each Line of Stdin to Os Copy/Paste Buffer via PbCopy"""

    while True:
        line_plus = sys.stdin.readline()
        line = line_plus.splitlines()[0]

        main.lines.append("Caught new Stdin:  {}".format(repr(line)))
        main.buffer = line

        subprocess.run("pbcopy".split(), input=line.encode(), check=True)

        main.lines.append("PbCopy complete for:  {}".format(repr(line)))


def main_2():
    """Watch for new revisions of Os Copy/Paste Buffer, send them onto Stdout"""

    while True:

        run = subprocess.run(
            "pbpaste".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True
        )
        stdout = run.stdout.decode()

        if main.buffer != stdout:

            main.lines.append("Caught new PbPaste:  {}".format(repr(stdout)))
            main.buffer = stdout

            continue

        time.sleep(0.900)


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0827pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
