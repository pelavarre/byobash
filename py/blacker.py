#!/usr/bin/env python3

"""
usage: python3 py/blacker.py [--h] [--]

tweak up the Sourcefiles found in this Dirs of Dirs, for people

options:
  --help  show this help message and exit

quirks:
  i ) adds a Posted-Into Link to this File as found on the Web
  ii ) adds a Copied-From Git Clone Line to invite you into editing this File for us
  iii ) trusts the Makefile to call Black and Flake8 before this File
  iv ) doesn't limit itself to the Git-Add'ed Sourcefiles
  v ) doesn't save changes till you call it with Parms

examples:
  python3 py/blacker.py  # show these examples and exit
  python3 py/blacker.py --h  # show this help message and exit
  python3 py/blacker.py --  # edit the Files of these nearby Dirs
"""


import glob
import os
import pathlib
import sys


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)
BIN_DIR = os.path.join(TOP_DIR, "bin")


try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


# Declare Templates

POSTED = "# posted into:  https://github.com/pelavarre/byobash/blob/main/"
COPIED = "# copied from:  git clone https://github.com/pelavarre/byobash.git"


def main():  # todo  # noqa C901 complex
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    # Choose Files to Review and Edit

    bin_hits = list(glob.glob("bin/*.py"))
    py_hits = list(glob.glob("py/*.py"))

    hits = bin_hits + py_hits
    hits.append("todo.txt")
    hits.append("tui/tui-todo.txt")

    approved_hits = list()
    for hit in hits:
        (_, ext) = os.path.splitext(hit)
        if ext:
            approved_hits.append(hit)

    # Visit each File once

    for hit in approved_hits:
        path = pathlib.Path(hit)
        if not path.is_dir():

            ichars = path.read_text()
            ilines = ichars.splitlines()

            # Strip off whole or half-finished efforts trailing at End of File

            olines = list(ilines)

            if olines and not olines[-1]:
                olines = olines[:-1]
            if olines and olines[-1].split()[:2] == "# copied".split():
                olines = olines[:-1]
            if olines and olines[-1].split()[:2] == "# posted".split():
                olines = olines[:-1]
            if olines and not olines[-1]:
                olines = olines[:-1]  # once
            if olines and not olines[-1]:
                olines = olines[:-1]  # twice

            # Add a whole effort

            if olines:
                olines.append("")
                olines.append("")

            olines.append(POSTED + hit)
            olines.append(COPIED)

            olines.append("")

            # Update the File if it needs change

            ochars = "\n".join(olines)

            if ochars != ichars:
                print(hit)  # mention which Files we are changing

                path.write_text(ochars)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/blacker.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
