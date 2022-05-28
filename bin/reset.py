#!/usr/bin/env python3

r"""
usage: reset.py [-h] [-x]

erase the lines of the Terminal and start again in the top left

options:
  --help  show this help message and exit

examples:
  reset  &&: 1000ms slow, but more reliable than:  clear
  reset 2>&1 |hexdump -C  &&: disclose what bytes Reset writes, if at Linux
"""
# todo: doc what bytes written


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
