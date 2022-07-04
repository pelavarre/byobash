#!/usr/bin/env python3

"""
usage: uptime [--h] ...

todo

options:
  --help       show this help message and exit

quirks:
  classic UpTime dumps results, rudely burying the Alt Queries, when given no Parms

examples:

  uptime.py  &&: show these examples and exit
  uptime.py --h  &&: show this help message and exit
  uptime.py --  &&: todo: run as you like it

  uptime --pretty  &: say less, more clearly, at Linux or GShell
  uptime.py --pretty  &: just as good at MacOS too
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/uptime.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
