#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

erase the lines of the Terminal and start again in the top left

options:
  --help  show this help message and exit
  -x      clear like Mac

notes:
  fall back to Echo, to clear your Terminal as well as ⌘W ⌘N does
  call Clear twice

  substitute the examples of 'echo -ne' for 'clear' if you can't accept a default of '-x'
  some Clear never clear scrollback, as if 'clear -x' always
  some Clear never clear scrollback, as if 'clear -x' always

examples:
  clear.py  &&: clear Terminal history
  clear.py -x  &&: echo -ne '\e[H\e[2J'  # scroll all lines up and away
  clear && clear  &&: clear Terminal history, and write a screen of history, if at Linux
  echo -ne '\e[H\e[2J' && echo -ne '\e[2J\e[3J\e[H'  &&: clear Terminal history
  reset  &&: clear Terminal history, but also sleep 1000ms
"""

# FIXME: do the for-real Clear Terminal History when called as:  clear.py --


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
