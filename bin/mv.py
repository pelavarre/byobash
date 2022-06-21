#!/usr/bin/env python3

"""
usage: mv.py [-i] [FROM | FROM ... TO]

rename Files or Dirs

positional arguments:
  FROM    the Files or Dirs to rename (default: the last of the 'ls -1rt')
  TO      the new name (default: add '~%m%d~jqd~%H%M~')

options:


options:
  --help  show this help message and exit
  -i      stop and ask before replacing file or dir

examples:
  mv.py  &&: call Mv Py with no args to show these examples
  mv.py --  &&: 'mv -i' the last of the 'ls -1rt' to stamp name with '~%m%d~jqd~%H%M~'
  ls.py  &&: the 'ls -C' view of:  ls -1rt |tail -3
"""


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
