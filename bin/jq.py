#!/usr/bin/env python3

"""
usage: jq.py [--h] ...

edit a stream of Json

options:
  --help       show this help message and exit

quirks:
  classic Jq rudely dumps Help & exits via a Code 1 Usage Error, when given no Parms

examples:

  jq.py  # show these examples and exit
  jq.py --h  # show this help message and exit
  jq.py --  # todo: run as you like it

  echo '[{"a": 1}, {"b": 2}]' |jq .
"""
# echo 123.000 |jq .   # 123
# echo 123.000 |json_pp  # 123


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/jq.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
