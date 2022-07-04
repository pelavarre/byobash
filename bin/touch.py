#!/usr/bin/env python3

"""
usage: touch.py [--h] [FILE ...]

stamp Files with date/time, to bring them to the end of the 'ls -1rt'

positional arguments:
  FILE    a File or Dir to trash (default: the last of the 'ls -1rt')

options:
  --help  show this help message and exit

quirks:
  works well with cp.py, ls.py, mv.py, rm.py, rmdir.py
  classic Touch rudely declines to create a new file, when given no FILE name for it

examples:

  touch.py  &&: show these examples and exit
  touch.py --h  &&: show this help message and exit
  touch.py --  &&: todo: run as you like it

  touch.py  &&: call Rm Touch with no args to show these examples
  touch.py --  &&: stamp the second-to-last of 'ls -1rt' to make it last
  ls.py  &&: the 'ls -C' view of:  ls -1rt |tail -3
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/touch.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
