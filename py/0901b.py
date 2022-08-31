#!/usr/bin/env python3

"""
usage: python3 py/0901b.py [--h] [--]

show 3 threads taking changes from Stdin and from PbPaste, and sending changes to PbCopy

examples:
    python3.py py/0901b.py  # show these examples
    python3.py py/0901b.py --
"""


import os
import pdb
import signal
import subprocess
import sys
import termios
import threading
import time
import tty

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


SIGINT_RETURNCODE_130 = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE_130 == 130


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    print("press Control+C to quit")
    print()

    fd = sys.stdin.fileno()
    main.with_termios = termios.tcgetattr(fd)

    tty.setraw(fd, when=termios.TCSADRAIN)  # not TCSAFLUSH

    try:
        run_threads()
    finally:
        tty_close()

    sys.exit(SIGINT_RETURNCODE_130)


def tty_close():

    fd = sys.stdin.fileno()
    when = termios.TCSADRAIN
    attributes = main.with_termios
    termios.tcsetattr(fd, when, attributes)


def run_threads():
    """Run some Threads in parallel"""

    main.exiting = False

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

    while not main.exiting:

        if main.lines:
            line = main.lines.pop(0)
            print(line + "\r")

        time.sleep(0.100)


def main_1():
    """Copy each Line of Stdin to Os Copy/Paste Buffer via PbCopy"""

    while not main.exiting:

        stdin = os.read(sys.stdin.fileno(), 1)
        if stdin == b"\x03":
            main.exiting = True

            break

        line = repr(stdin) + "\n"

        main.lines.append("Caught new Stdin:  {}".format(repr(line)))
        main.buffer = line

        subprocess.run("pbcopy".split(), input=line.encode(), check=True)

        main.lines.append("PbCopy complete for:  {}".format(repr(line)))


def main_2():
    """Watch for new revisions of Os Copy/Paste Buffer, send them onto Stdout"""

    while not main.exiting:

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


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0901b.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
