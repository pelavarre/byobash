#!/usr/bin/env python3

"""
usage: shall.py [--h]

print the table of contents of our bash manual

options:
  --help       show this help message and exit

quirks:
  most Zsh include 'man zshall', but few Bash include 'man shall'

examples:

  shall.py  # show these examples and exit
  shall.py --h  # show this help message and exit
  shall.py --  # todo: run as you like it

  shpipe.py  # show examples of working with Bash Pipes
  # todo: add more than 1 chapter here
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/shall.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
