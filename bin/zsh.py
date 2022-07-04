#!/usr/bin/env python3

"""
usage: zsh.py [--h] [-f] ...

shell out to a host

options:
  --help  show this help message and exit
  -f      launch without running startup files

quirks:
  classic Zsh rudely opens a new Session, with an empty "$@", when given no Parms
  classic Zsh rudely places no Scroll Limits on Sh Commands
  todo: limit Control Sequences dumped into Tty, a la 'less', 'less -R', 'less -r'

examples:

  zsh.py  &&: show these examples and exit
  zsh.py --h  &&: show this help message and exit
  zsh.py --  &&: todo: run as you like it

  export |grep SHLVL
  zsh -f  &&: run with less local quirks
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/zsh.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
