#!/usr/bin/env python3

"""
usage: zsh.py [--help] [-f] ...

shell out to a host

options:
  --help  show this help message and exit
  -f      launch without running startup files

examples:
  export |grep SHLVL
  zsh -f  &&: run with less local quirks
"""


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
