#!/usr/bin/env python3

r"""
usage: sed.py [--h] [-i BAK] [-n] [[-e CODE] ...] [FILE ...]

edit

positional arguments:
  FILE     one File to edit

options:
  --help   show this help message and exit
  -i BAK   the File Ext to add to name the backups of the edited File's
  -n       run without the default Code of:  1,$p
  -e CODE  some Code to run

quirks:
  goes well with:  head.py, tail.py, tee.py
  classic Sed rudely hangs with no prompt, when given no Parms with no Stdin

examples:

  sed.py  # show these examples and exit
  sed.py --h  # show this help message and exit
  sed.py --  # todo: run as you like it

  sed -i~ 's,STALE,FRESH,g' *.py  # global edit find search replace
  echo a b c d e |tr ' ' '\n' |sed -n -e '1p' -e '$p'  # first, last
  echo a b c d e |tr ' ' '\n' |sed -n -e '1,2p' -e $'3i\\\n...' -e '$p'  # head, tail
"""

# todo: grow default w Screen Height
# todo: demo how to code Sed to replace with color, a la:  grep --color=yes


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sed.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
