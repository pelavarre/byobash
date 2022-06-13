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
"""
# todo: doc what bytes written


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
