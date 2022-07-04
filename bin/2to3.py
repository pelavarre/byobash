#!/usr/bin/env python3

"""
usage: 2to3.py [--h] [-w] [-W] [--no-diffs] FILE

convert Python 2 to run as Python 3 (and perhaps no longer as Python 2)

positional arguments:
  FILE        source file to convert

quirks:
  classic 2to3 rudely exits via a Code 2 Usage Error, when given no Parms

options:
  --help      show this help message and exit
  -w          write back modified files
  -W          write back unmodified files
  --no-diffs  just leave the diffs in Git, don't print them on screen

examples:

  2to3.py  &&: show these examples and exit
  2to3.py --h  &&: show this help message and exit
  2to3.py --  &&: todo: run as you like it

  2to3 -w -W --no-diffs p.py  # do
  git checkout HEAD p.py  # undo
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/2to3.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
