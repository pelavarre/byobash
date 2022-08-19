#!/usr/bin/env python3

"""
usage: vi.py [--help] [-u VIMRC]

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

  vi +$ Makefile  # open up at end of file, not start of file
  vi +':set background=light' Makefile  # choose Light Mode, when they didn't
  vi +':set background=dark' Makefile  # choose Dark Mode, when they didn't
"""


import byotools as byo


byo.exit(__name__)


# todo: make sense of C E at 'one  two' does leave both spaces in place

# todo: vim options akin to less -FIRX

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

# color a multiline _ = """..."""
# much like '# '

# solve
#
#    % bash -c vi </dev/null
#    Vim: Warning: Input is not from a terminal
#    :q%
#    %
#


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/vi.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
