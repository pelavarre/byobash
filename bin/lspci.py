#!/usr/bin/env python3

"""
usage: lspci.py ...

sketch the tree of plugged-in PCI devices

options:
  --help  show this help message and exit
  -t      sketch the tree as a tree
  -vvv    max verbosely

examples:
  lspci -t -vvv |less -FIRX
"""


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
