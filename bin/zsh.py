#!/usr/bin/env python3

"""
usage: zsh.py [--h] [-f] ...

shell out to a host

options:
  --help  show this help message and exit
  -f      launch without running startup files

examples:
  export |grep SHLVL
  zsh -f  &&: run with less local quirks
"""


import byotools as byo


if __name__ == "__main__":

    byo.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
