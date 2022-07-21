#!/usr/bin/env python3

"""
usage:  import buttonfile as bf
"""


import __main__
import os
import pathlib
import pdb
import shutil
import sys

_ = pdb


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)  # one up from "macos/"
BIN_DIR = os.path.join(TOP_DIR, "bin")


try:
    import byopyvm
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byopyvm


def exit():
    """Take the name of the Main File as a Word of Command for ByoPyVm"""

    if not hasattr(__main__, "pdb"):
        __main__.pdb = pdb  # define 'pdb.pm()' for instances of 'python -i main.py'

    main_file = __main__.__file__
    main_dirname = os.path.dirname(main_file)
    os.chdir(main_dirname)

    pycache_path = pathlib.Path("__pycache__")
    with_pycache = pycache_path.exists()

    parms = ["buttonfile", main_file]
    byopyvm.parms_run(parms)

    if with_pycache:
        if pycache_path.exists():
            shutil.rmtree(pycache_path)


# did you mean:  https://github.com/pelavarre/byobash/tree/main/macos#readme
# sorry i've moved lots of words there, from:  BUTTON_FILE_DOC = """ ... """


# posted into:  https://github.com/pelavarre/byobash/blob/main/macos/buttonfile.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
