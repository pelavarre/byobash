#!/usr/bin/env python3

"""
usage: emacs.py [-h] [-nw] [-Q] [--no-splash] [-q] [--script SCRIPT] [--eval COMMAND]
                [FILE ...]

read files, accept edits, write files, in the way of classical emacs

positional arguments:
  FILE                a file to edit (default: None)

options:
  -h, --help          show this help message and exit
  -nw                 stay inside this terminal, don't open another terminal
  -Q, --quick         run as if --no-splash and --no-init-file (but slow after crash)
  --no-splash         start with an empty file, not a file of help
  -q, --no-init-file  don't default to run '~/.emacs' after args
  --script SCRIPT     file of elisp commands to run after args (default: '/dev/null')
  --eval COMMAND      another elisp command to run after args and after --script

examples:

  emacs.py  # show these examples and exit
  emacs.py --h  # show this help message and exit
  emacs.py --  # todo: run as you like it

  emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  emacs -q -nw --no-splash --eval '(menu-bar-mode -1)'
"""

# todo:  emacs.py --, emacs.py -q --


import byotools as byo


byo.exit(__name__)


# solve
#
#    % bash -c emacs </dev/null
#    Emacs: standard input is not a tty
#    Zsh: exit 1     bash -c emacs < /dev/null
#    %
#

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/emacs.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
