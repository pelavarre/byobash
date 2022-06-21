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
  -R, --RAW-CONTROL-CHARS
                        pass colors etc. through to the screen
  -X, --no-init         don't clear screen at quit

examples:
  ls ~ |vi -  &&: much the same idea
"""


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
