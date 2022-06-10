#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

erase the Screen and Scrollback of the Terminal, move the Cursor to Top Left of Screen

options:
  --help  show this help message and exit
  -x      scroll up and away all the Rows of the Screen, do Not delete Scrollback

examples:
  clear.py --  &&: deletes all Scrollback
  echo -ne '\e[3J\e[H\e[2J'  &&: deletes all Scrollback
  echo -ne '\e[H\e[2J\e[3J'  &&: keeps one Screen, call twice to blank that Screen
  echo -ne '\e[H\e[2J'  &&: deletes no Scrollback
  reset  &&: deletes all Scrollback but also sleeps 1000ms
  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  &&: fill Screens for test
  clear |tee >(hexdump -C)  &&: call and trace Clear, at Mac or Linux
  tput clear 2>&1 |tee >(hexdump -C)  &&: call and trace TPut Clear, at Mac or Linux
  reset 2>&1 |tee >(hexdump -C)  &&: call and trace Reset, at Linux
"""


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
