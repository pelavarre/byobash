#!/usr/bin/env python3

"""
usage: df.py [--h]

help guess when file writes will fail because disk full

options:
  --help  show this help message and exit

quirks:
  classic Df dumps all the top lines, with no Scroll limit, when given no Parms

examples:

  df.py  # show these examples and exit
  df.py --h  # show this help message and exit
  df.py --  # todo: run as you like it

  echo ... && df |awk '{print $5"\t"$0}' |sort -n |tail -3  # show the three most full
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/df.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
