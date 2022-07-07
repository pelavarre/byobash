#!/usr/bin/env python3

"""
usage: byochatpy.py [--h] [--] [WORD ...]

chat with clone of self

options:
  --help  show this help message and exit

positional args:
  WORD    words of client messsage to send

quirks:
  writes client message to "{stamp}.in" file at server
  launches clone of self as server if server not found
  launches clone into '__pycache__/byochatpy/' dir

examples:
  byochatpy.py  # show these examples and exit
  byochatpy.py --h  # show this help message and exit
  byochatpy.py --  # find else launch the server without sending a client message
"""


import os
import sys


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)
BIN_DIR = os.path.join(TOP_DIR, "bin")


try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    # FIXME


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0704pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
