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


BUTTON_FILE_DOC = """

a popular corner of macOS configuration makes these Button Files work well


1.1 drag the Folder containing these Button Files into macOS

1.2 open this Folder, choose one Button File, and Double-Click through it

1.3 odds on, then it just works

1.3.1 like Finder > View > As List (⌘2) will show you the Fibonacci numbers

1~ 2~ 3~ 5


    1 , 2
    over over +
    over over +


2. icon layout =>

i don't already know how to ship you a copy of my Button Icon Layout

my own first Layout now is

                 7  8  9  /
           OVER  4  5  6  *
            π    1  2  3  -
    CLEAR        0  .  ,  +

    icons  README.md buttonfile.py


2. details =>

2.1 your Control+Click on Button Files says more when you press the Option/Alt key
2.1.1 it already says Always Open With > Terminal (default)
2.1.2 because each of these Button Files has an Extension (Ext) of '.command'
2.1.3 although it may be hidden from view

2.2 your Terminal > Preferences > Profiles > Shell > When The Shell Exit speaks
2.2.1 it already says Close If The Shell Exited Cleanly, or it already says Close

2.3 inside your Terminal, your 'which -a python3' says Feb/2020 Python 3.8.2 or newer

2.4 your Finder > File > Get Info on this Button File speaks
2.4.1 it says the Extension on this Button File is:  .command
2.4.2 it says Yes to Hide Extension?
2.4.3 and someone has dragged a better Icon onto the upper left of its Get Info dialog

2.5 your Finder View > As Icons (⌘1) is showing you this Folder
2.5.1 not so much ⌘2 List, ⌘3 Columns, ⌘4 Gallery

those kinds of details make this Button File work well, as a Desktop Calculator

"""

BUTTON_FILE_DOC = BUTTON_FILE_DOC.strip()


# posted into:  https://github.com/pelavarre/byobash/blob/main/macos/buttonfile.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
