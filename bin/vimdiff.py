#!/usr/bin/env python3

"""
usage: todo

todo

options:
  --help       show this help message and exit

quirk:
  classic VimDiff rudely silently falls back to Vim with No Parms, when given No Parms

examples:

  vimdiff.py  &&: show these examples and exit
  vimdiff.py --h  &&: show this help message and exit
  vimdiff.py --  &&: todo: run as you like it

  :
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/vimdiff.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
