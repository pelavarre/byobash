#!/usr/bin/env python3

"""
usage: touch.py [--h] [TO ...]

stamp Files with date/time, to bring them to the end of the 'ls -1rt'

positional arguments:
  TO      a File or Dir to trash (default: the last of the 'ls -1rt')

options:
  --help  show this help message and exit

examples:
  touch.py  &&: call Rm Touch with no args to show these examples
  touch.py --  &&: stamp the second-to-last of 'ls -1rt' to make it last
  ls.py  &&: the 'ls -C' view of:  ls -1rt |tail -3
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/touch.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
