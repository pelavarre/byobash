#!/usr/bin/env python3

"""
usage: cp.py [FROM_FILE | FROM_FILE ... TO_FILE]

copy files or dirs

positional arguments:
  FROM_FILE  the Files or Dirs to copy (default: the last of the 'ls -1rt')
  TO_FILE    the new name (default: add '~%m%d~jqd~%H%M~')

options:
  --help     show this help message and exit
  -i         stop and ask before replacing file or dir
  -p         copy modified date/timestamp and permissions too, not just bytes in file
  -R         agree to copy a dir that contains files or dirs or both

quirks:
  works well with ls.py, mv.py, rm.py, rmdir.py, touch.py
  classic Cp rudely declines to choose the FROM_FILE and TO_FILE itself

examples:

  cp.py  &&: show these examples and exit
  cp.py --h  &&: show this help message and exit
  cp.py --  &&: 'cp -ipR' the last of the 'ls -1rt' to stamp name with '~%m%d~jqd~%H%M~'

  ls.py --  &&: the 'ls -C' view of:  ls -1rt |tail -3
"""

# todo: learn to faithfully copy sym links too


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/cp.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
