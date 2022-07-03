"""
usage: python3 py/0630pl.py --

link the end of each Sourcefile to a copy of itself on the Web, and a Git Repo inviting change to it

options:
  --help  show this help message and exit

quirks:
  semi-anonymous
  newborn

examples:
  python3 py/0630pl.py  # show these examples and exit
  python3 py/0630pl.py --h  # show this help message and exit
  python3 py/0630pl.py --  # edit the Files of these nearby Dirs
  make push  # implicitly call all Py Files near here, without Parms, as a SelfTest
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

POSTED = "# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/"
COPIED = "# copied from:  git clone https://github.com/pelavarre/byobash.git"


def main():
    """Run from the Sh Command Line"""

    byo.exit()  # do nothing without Parms

    # Choose Files to Review and Edit

    bin_hits = list(glob.glob("bin/*.py"))
    py_hits = list(glob.glob("py/*.py"))

    hits = bin_hits + py_hits
    hits.append("todo.txt")
    hits.append("tui/tui-todo.txt")

    # Visit each File once

    for hit in hits:
        filename = os.path.basename(hit)

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

            olines.append(POSTED + filename)
            olines.append(COPIED)

            olines.append("")

            # Update the File only if it needs change

            ochars = "\n".join(olines)

            if ochars != ichars:
                print(hit)  # mention which Files we are changing

                path.write_text(ochars)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/0630pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
