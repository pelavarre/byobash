#!/usr/bin/env python3

"""
usage: scp.py [--h] ...

todo

options:
  --help       show this help message and exit

quirks:
  classic Scp rudely exits via a Code 1 Usage Error, when given no Parms

examples:
  scp.py  # show these examples and exit
  scp.py --h  # show this help message and exit
  scp.py --  # guide the next Scp with:  echo $(id -un)@$(hostname):$(pwd):/.
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/scp.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
