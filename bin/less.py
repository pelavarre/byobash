#!/usr/bin/env python3

"""
usage: less [-F] [-I] [-R] [-X] [FILE ...]

edit a stream of lines

positional arguments:
  FILE                  a file to copy in (such as '-' to mean Stdin)

options:
  --help                show this help message and exit
  -F, --quit-if-one-screen
                        show the lines and quit, if they fit in one screen
  -I, --IGNORE-CASE
                        ignore case in searches, till i type -I again
  -r, --raw-control-chars
                        pass arbitrary Bytes etc. through to the Screen
  -R, --RAW-CONTROL-CHARS
                        pass Colors etc. through to the Screen
  -X, --no-init         don't clear screen at quit

quirks:
  classic Less rudely exits via a Code 0 Usage Error, when given no Parms

examples:

  less.py  # show these examples and exit
  less.py --h  # show this help message and exit
  less.py --  # todo: run as you like it

  ls ~ |vi -  # much the same idea
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/less.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
