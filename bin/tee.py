#!/usr/bin/env python3

r"""
usage: tee.py [--h] [-a] [FILE ...]

read from Stdin and write the bytes read into each File in order

positional arguments:
  FILE    the file to drop trailing lines from (default: stdin)

options:
  --help  show this help message and exit
  -a      append to the Files that already exist, don't create those

quirks:
  give Args or Stdin, or print a prompt, to stop more Tee's from hanging silently

examples:
  echo {A..Z} |tr ' ' '\n' | tee >(head -2) >(sleep 0; tail -3) > /dev/null
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/tee.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
