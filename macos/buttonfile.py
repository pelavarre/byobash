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

    # Define 'pdb.pm()' for instances of 'python -i main.py'

    if not hasattr(__main__, "pdb"):
        __main__.pdb = pdb

    # Place the Stack into the Dir that contains the Buttonfile Py

    module = sys.modules[__name__]
    module_file = module.__file__
    module_dirname = os.path.dirname(module_file)

    os.chdir(module_dirname)

    # Run the Basename of the Main File as a Parm,
    # but remove the PyCache created for the Buttonfile Py,
    # unless exiting abnormally or launching with that PyCache in place

    pycache_path = pathlib.Path("__pycache__")
    with_pycache = pycache_path.exists()

    parms = ["buttonfile", __main__.__file__]
    byopyvm.parms_run_some(parms)

    if with_pycache:
        if pycache_path.exists():
            shutil.rmtree(pycache_path)


# posted into:  https://github.com/pelavarre/byobash/blob/main/macos/buttonfile.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
