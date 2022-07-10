#!/usr/bin/env python3

"""
usage: rm.py [--h] [FILE ...]

move Files or Dirs to trash, and count them

positional arguments:
  FILE    a File or Dir to trash (default: the last of the 'ls -1rt')

options:
  --help  show this help message and exit

quirks:
  goes well with:  cp.py, ls.py, mv.py, rmdir.py, touch.py
  classic Rm rudely declines to choose a FILE to destroy

examples:

  rm.py  # show these examples and exit
  rm.py --h  # show this help message and exit
  rm.py --  # todo: run as you like it

  rm.py  # call Rm Py with no args to show these examples
  rm -fr dirname/  # remove Dir if present, but don't remove a File of the same name
  rm.py --  # move the last of the 'ls -1rt' into the '__pycache__/%m%d/' dir
  ls.py  # the 'ls -C' view of:  ls -1rt |tail -3
"""
# todo:  rm -fr dir/  ^^


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/rm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
