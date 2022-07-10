#!/usr/bin/env python3

"""
usage: uname.py [--h] [-a] ...

show the clan name of this Unix (often the Darwin BSD C*pyright License, else Linux)

options:
  --help  show this help message and exit
  -a      show all the default Key-Value Pairs
  -s      show just the clan name of this Unix, just its value, such as 'Darwin'

quirks:
  classic UName dumps the 'uname -s', when given no Parms
  goes well with:  lsb_release.py, uname.py

examples:

  uname.py  # show these examples and exit
  uname.py --h  # show this help message and exit
  uname.py --  # todo: run as you like it

  uname  # such as:  Darwin

  :
  : Darwin  # shown by Zsh or Bash in Terminal at Mac
  : Linux  # shown by Zsh or Bash in Terminal at Ubuntu Linux
  :
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/uname.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
