#!/usr/bin/env python3

"""
usage: script.py [--h] [TYPESCRIPT]

limit a Terminal window to a few rows and columns shared between hosts

positional args:
  TYPESCRIPT  the name of the LogFile (default: 'typescript')

options:
  --help  show this help message and exit

quirks:
  works well with:  screen.py
  classic Script rudely opens a new anonymous Session, when given no Parms

examples:

  script.py  # show these examples and exit
  script.py --h  # show this help message and exit
  script.py --  # todo: run as you like it

  script t.typescript  # make a LogFile that doesn't much flush till Exit

  cat t.typescript  # trust and run the Esc sequences
  less -FIRX t.typescript  # trust and run the Esc sequences
  less t.typescript  # show the Esc sequences without running them
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/script.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
