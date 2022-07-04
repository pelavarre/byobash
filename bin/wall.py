#!/usr/bin/env python3

"""
usage: todo

todo

options:
  --help       show this help message and exit

quirks:
  classic WAll rudely hangs with no prompt, when given no Parms with no Stdin

examples:

  wall.py  &&: show these examples and exit
  wall.py --h  &&: show this help message and exit
  wall.py --  &&: todo: run as you like it

  :
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/wall.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
