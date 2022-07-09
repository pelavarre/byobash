#!/usr/bin/env python3

"""
usage: python3 py/0704pl.py [--h] [--]

expand the mark SQUIRREL when found in a Bin Py File

options:
  --help  show this help message and exit

quirks:
  i ) doesn't limit itself to the Git-Add'ed Sourcefiles
  ii ) doesn't save changes till you call it with Parms

examples:
  python3 py/0704pl.py  # show these examples and exit
  python3 py/0704pl.py --h  # show this help message and exit
  python3 py/0704pl.py --  # edit the Files of these nearby Dirs
"""


import glob
import os
import pathlib
import sys
import textwrap


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)
BIN_DIR = os.path.join(TOP_DIR, "bin")


try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


# Declare Templates

BRIEF = """

  p.py  # show these examples and exit
  p.py --h  # show this help message and exit
  p.py --  # todo: run as you like it

"""


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    # Choose Files to Review and Edit

    approved_hits = list(glob.glob("bin/*.py"))

    if False:
        approved_hits = approved_hits[:1]

    # Visit each File once

    for hit in approved_hits:
        path = pathlib.Path(hit)
        if not path.is_dir():
            basename = os.path.basename(hit)

            ichars = path.read_text()
            ilines = ichars.splitlines()

            # Copy each Line, but expand as you go

            olines = list()
            for iline in ilines:
                oline = iline

                if iline == "  SQUIRREL":

                    expansion = textwrap.dedent(BRIEF)
                    expansion = expansion.strip()

                    expansion = expansion.replace("p.py", basename)

                    for xline in expansion.splitlines():
                        olines.append("  " + xline)

                    continue

                olines.append(oline)

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


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0704pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
