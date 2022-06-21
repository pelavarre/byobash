#!/usr/bin/env python3

"""
usage: jq.py [--h] ...

edit a stream of Json

options:
  --help       show this help message and exit

examples:
  echo '[{"a": 1}, {"b": 2}]' |jq .
"""


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
