#!/usr/bin/env python3

"""
usage: df.py [-h]

help guess when file writes will fail because disk full

options:
  -h, --help  show this help message and exit

examples:
  echo ... && df |awk '{print $5"\t"$0}' |sort -n |tail -3  &&: show the three most full
"""


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
