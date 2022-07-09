#!/usr/bin/env python3

"""
usage: todo

todo

options:
  --help       show this help message and exit

quirks:
  classic PSql rudely exits via a Code 2 Usage Error, when given no Parms

examples:
  psql.py  # show these examples and exit
  psql.py --h  # show this help message and exit
  psql.py --  # todo: run as you like it
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/psql.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
