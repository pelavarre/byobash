#!/usr/bin/env python3

"""
usage: bind.py [--h] ...

look at what each keystroke means, or mess with it

options:
  --help  show this help message and exit

quirks:
  classic Bind rudely does nothing but exit zero, when given no Parms

examples:

  bind.py  # show these examples and exit
  bind.py --h  # show this help message and exit
  bind.py --  # todo: run as you like it

  : bash chrome emacs macos screen slack ssh stty tmux vim
"""
# consistency across distribution of:  £ ← ↑ → ↓ ⇧ ⋮ ⌃ ⌘ ⌥ ⎋


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/bind.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
