#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

erase the lines of the Terminal and start again in the top left

options:
  --help  show this help message and exit
  -x      clear like Mac

examples:
  echo -ne '\e[H\e[2J\e[3J'  &&: clear Lines on and above Screen, in a MacOs Terminal
  clear.py --  &&: this first option
  echo -ne '\e[3J\e[H\e[2J'  &&: clear Lines above Screen, & scroll Lines on Screen away
  clear  &&: this second option, at Linux, but who wants this??
  echo -ne 'e[H\e[2J'  &&: scroll Lines on Screen away
  clear  &&: this third option
  clear -x  &&: this same third option, but at Linux or at Mac
  clear && clear  &&: clear Lines above, and scroll a Blank Screen above, if at Linux
  date; seq 40 ; date ; seq 40 ; date  &&: fill much Screen wih distinct lines
  reset  &&: clear Lines on and above Screen, but also sleep 1000ms
"""
# clear |hexdump -C  # show the 'e[H\e[2J' of Mac Clear, or '\e[3J\e[H\e[2J' at Linux
# reset 2>&1 |hexdump -C  # show the codes written by Linux Reset


import sys

import byotools


def main():

    if sys.argv[1:] != "--".split():

        byotools.main()  # FIXME: rename as '.exit'

    esc = "\x1B"
    print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


if __name__ == "__main__":
    main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
