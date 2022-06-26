#!/usr/bin/env python3

"""
usage: cp.py [FROM | FROM ... TO]

copy files or dirs

positional arguments:
  FROM    the Files or Dirs to copy (default: the last of the 'ls -1rt')
  TO      the new name (default: add '~%m%d~jqd~%H%M~')

options:
  --help  show this help message and exit
  -i      stop and ask before replacing file or dir
  -p      copy modified date/timestamp and permissions too, not just bytes in file
  -R      agree to copy a dir that contains files or dirs or both

examples:
  cp.py  &&: call Cp Py with no args to show these examples
  cp.py --  &&: 'cp -ipR' the last of the 'ls -1rt' to stamp name with '~%m%d~jqd~%H%M~'
  ls.py  &&: the 'ls -C' view of:  ls -w1rt |tail -3
"""

# todo: learn to faithfully copy sym links too


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
