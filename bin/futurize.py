#!/usr/bin/env python3

"""
usage: futurize.py [--h] [-w] [-W] [--no-diffs] FILE

convert Python 2 to run as Python 3 or as Python 2

positional arguments:
  FILE        source file to convert

options:
  --help      show this help message and exit
  -w          write back modified files
  -W          write back unmodified files
  --no-diffs  just leave the diffs in Git, don't print them on screen

quirks:
  classic Futurize rudely exits via a Code 130 Usage Error, when given no Parms

examples:

  futurize.py  # show these examples and exit
  futurize.py --h  # show this help message and exit
  futurize.py --  # todo: run as you like it

  futurize -w -W --no-diffs p.py  # do
  git checkout HEAD p.py  # undo
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/futurize.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
