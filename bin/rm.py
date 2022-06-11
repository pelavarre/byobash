#!/usr/bin/env python3

"""
usage: rm.py [--h] [FROM ...]

move Files or Dirs to trash, and count them

positional arguments:
  FROM      a File or Dir to trash (default: the last of the 'ls -1rt')

options:
  --help    show this help message and exit

examples:
  rm.py  &&: call Rm Py with no args to show these examples
  rm.py --  &&: move the last of the 'ls -1rt' into the '__pycache__/%m%d/' dir

examples:
  rm.py  &&: call Rm Py with no args to show these examples
  ls.py  &&: the 'ls -C' view of:  ls -1rt |tail -3
"""


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
