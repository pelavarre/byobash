#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

erase the Screen and Scrollback of the Terminal, move the Cursor to Top Left of Screen

options:
  --help  show this help message and exit
  -x      scroll up and away all the Rows of the Screen, do Not delete Scrollback

examples:

  clear.py --  &&: deletes Scrollback, like ⌘K, except GShell ignores 3J while TMux

  echo -ne '\e[H\e[2J\e[3J'  &&: deletes Scrollback, like ⌘K at Mac of Mac or Linux
  echo -ne '\e[3J\e[H\e[2J'  &&: keeps one Screen, call twice to blank that Screen
  echo -ne '\e[H\e[2J'  &&: scroll Screen away, but keep Scrollback, like ⌃L

  reset  &&: deletes all Scrollback but also sleeps 1000ms

  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  &&: fill Screens for test

  clear 2>&1 |tee >(hexdump -C)  &&: call and trace Clear
  tput clear 2>&1 |tee >(hexdump -C)  &&: call and trace TPut Clear
  reset 2>&1 |tee >(hexdump -C)  &&: call and trace Reset, at Linux
"""
# todo: find a Clear that deletes Scrollback, inside default GShell TMux Enabled
# todo: call and trace Reset, at Mac


import sys

import byotools


def main():

    parms = sys.argv[1:]
    if parms != "--".split():

        byotools.exit()

    esc = "\x1B"
    print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


if __name__ == "__main__":
    main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
