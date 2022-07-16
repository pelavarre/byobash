#!/usr/bin/env python3

"""
usage: vim.py [--help] [-u VIMRC]

todo

options:
  --help    show this help message and exit
  -u VIMRC  edit after running a file (default '~/.vimrc')

quirks:
  classic Vi rudely runs ahead and creates a new Scratchpad, when given no Parms
  classic Vi rudely declines to quit when asked to ':n' past the last File

examples:

  vi.py  # show these examples and exit
  vi.py --h  # show this help message and exit
  vi.py --  # todo: run as you like it

  vim -u /dev/null ~/.vimrc
"""

# todo: vim $(which ...)
# todo: ) lights for matching/ not
# demo +123
# demo +startinsert
# ⌥ to not care if in Insert Mode or not
# ⌥a ⌥i ⌥o ⌥A ⌥I ⌥O, also ⌥Z, also ⌃G
# vim.py to take:  triage/scraps/jv_sad_builds.py:775
# integrate with 'pbpaste, pbcopy'
#
# todo: Linux Vim splits lines from Command+Click, Linux Less does Not, Mac Vim hmm


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/vi.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
