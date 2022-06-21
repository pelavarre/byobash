#!/usr/bin/env python3

r"""
usage: reset.py [--h] [-x]

wipe the Screen, delete the Scrollback, leave the Cursor at Top Left

options:
  --help  show this help message and exit

quirks:
  GShell default TMux keeps Scrollback

examples:
  reset  &&: 1000ms slow, but more reliable than:  clear
  reset 2>&1 |tee >(hexdump -C)  &&: call and trace Reset, at Linux
  reset.py  &&: about as reliable as 'clear', but much faster
  echo -ne '\e[8;'$(stty size | cut -d' ' -f1)';89t'  &&: 89 cols
"""
# todo: doc what bytes written


import sys


import byotools as byo


if __name__ == "__main__":

    parms = sys.argv[1:]
    if parms != "--".split():

        byo.exit()

    esc = "\x1B"
    print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


# copied from:  git clone https://github.com/pelavarre/byobash.git
