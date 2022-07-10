#!/usr/bin/env python3

"""
usage: mv.py [-i] [FROM_FILE | FROM_FILE ... TO_FILE]

rename Files or Dirs

positional arguments:
  FROM_FILE  the Files or Dirs to rename (default: the last of the 'ls -1rt')
  TO_FILE    the new name (default: add '~%m%d~jqd~%H%M~')

options:
  --help     show this help message and exit
  -i         stop and ask before replacing file or dir

quirks:
  goes well with:  cp.py, ls.py, rm.py, rmdir.py, touch.py
  classic Mv rudely declines to choose the FROM_FILE and TO_FILE itself

examples:

  mv.py  # show these examples and exit
  mv.py --h  # show this help message and exit
  mv.py --  # 'mv -i' the last of the 'ls -1rt' to stamp name with '~%m%d~jqd~%H%M~'

  ls.py --  # the 'ls -C' view of:  ls -1rt |tail -3
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/mv.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
