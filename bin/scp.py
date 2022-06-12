#!/usr/bin/env python3

"""
usage: scp.py [--h] ...

todo

options:
  --help       show this help message and exit

examples:
  scp.py --  &&: guide the next Scp with:  echo $(id -un)@$(hostname):$(pwd):/.
"""


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
