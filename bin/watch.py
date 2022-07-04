#!/usr/bin/env python3

"""
usage: watch.py [--h] ...

todo

options:
  --help       show this help message and exit

quirks:
  classic Watch rudely dumps Help & exits via a Code 1 Usage Error, when given no Parms

examples:

  watch.py  &&: show these examples and exit
  watch.py --h  &&: show this help message and exit
  watch.py --  &&: todo: run as you like it

  :
"""
# todo: summary transcript at exit, whole & summary transcript while it runs


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/watch.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
