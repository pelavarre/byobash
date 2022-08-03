#!/usr/bin/env python3

"""
usage: python3 py/makeover.py [--h] [--]

conform the Files of nearby Dirs to some convention of the moment

options:
  --help  show this help message and exit

quirks:
  doesn't save changes till you call it with Parms, such as:  --

examples:
  python3 py/makeover.py  # show these examples and exit
  python3 py/makeover.py --h  # show this help message and exit
  python3 py/makeover.py --  # edit the Files of these nearby Dirs
"""


import glob
import os
import pathlib
import pdb
import sys

_ = pdb


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)  # one up from "py/"
BIN_DIR = os.path.join(TOP_DIR, "bin")

try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    # Choose Files to Review and Edit

    if False:

        GLOB = "bin/*.py"

        authed_hits = list(glob.glob(GLOB))
        if False:
            authed_hits = authed_hits[:1]

    # Choose Different Files to Review and Edit

    shline = "git grep -il Posted"
    byo.stderr_print("+ {}".format(shline))
    lines = byo.subprocess_run_somelines(shline)

    authed_hits = lines

    # Visit each File once

    byo.stderr_print("py/makeover.py: Reading {} files".format(len(authed_hits)))
    byo.stderr_print()

    patched_hits = list()
    for hit in authed_hits:
        path = pathlib.Path(hit)
        if not path.is_dir():
            relpath = os.path.relpath(path)
            ext = os.path.splitext(path)[-1]

            ichars = path.read_text()
            ilines = ichars.splitlines()

            # Compose some Lines

            posted = "https://github.com/pelavarre/byobash/blob/main/"
            posted += relpath

            copied = "git clone https://github.com/pelavarre/byobash.git"

            # Edit the File

            olines = list(ilines)

            if ext == ".md":
                occasion = (hit, ilines[-4:])

                assert ilines[-4] == "", occasion
                assert ilines[-3].startswith("posted "), occasion
                assert ilines[-2] == "<br>", occasion
                assert ilines[-1].startswith("copied "), occasion

                olines[-3] = "posted into:  {}".format(posted)
                olines[-1] = "copied from:  {}".format(copied)

            else:
                occasion = (hit, ilines[-3:])

                assert ilines[-3] == "", occasion
                assert ilines[-2].startswith("# posted "), occasion
                assert ilines[-1].startswith("# copied "), occasion

                olines[-2] = "# posted into:  {}".format(posted)
                olines[-1] = "# copied from:  {}".format(copied)

            # Only mutate the File if the Edit made changes

            ochars = "\n".join(olines) + "\n"

            if ochars != ichars:
                patched_hits.append(hit)

                byo.stderr_print(hit)

                path.write_text(ochars)

    byo.stderr_print()
    byo.stderr_print("py/makeover.py: Wrote {} files".format(len(patched_hits)))


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/makeover.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
