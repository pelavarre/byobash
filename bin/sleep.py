#!/usr/bin/env python3

"""
usage: sleep.py [--h] ...

todo

options:
  --help       show this help message and exit

quirks:
  classic Sleep rudely exits via a Code 1 Usage Error, when given no Parms

examples:
  sleep.py  # show these examples and exit
  sleep.py --h  # show this help message and exit
  sleep.py --  # sleep for 3 Seconds, but reply to ⌃T and quit at ⌃C
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sleep.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
