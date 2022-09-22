#!/usr/bin/env python3

"""
usage: json_pp.py [--h] ...

edit a stream of Json

options:
  --help       show this help message and exit

quirks:
  goes well with:  jq.py
  works hard to shove you into 3 Column Dents, out of Jq 2 Column Dents
  defaults to '"Key":Value' missing 1 Space of Jq '"Key": Value'

examples:

  json_pp.py  # show these examples and exit
  json_pp.py --h  # show this help message and exit
  json_pp.py --  # json_pp --json_opt indent,indent_length=2

  echo '[{"a": 1}, {"b": 2}]' |bin/json_pp.py --  # 2 Column Dents

  echo '[{"a": 1}, {"b": 2}]' |json_pp  # 3 Column Dents
  echo '[{"a": 1}, {"b": 2}]' |json_pp --json_opt indent,indent_length=2  # 2, not 3
"""

# todo: prompt Tty Stdin for:  json_pp.py --

#
# echo 123.000 |jq .   # 123
# echo 123.000 |json_pp  # 123
#


import shlex

import byotools as byo


if __name__ == "__main__":

    byo.exit(shparms="--")  # return only for:  json_pp.py --

    argv = shlex.split("json_pp --json_opt indent,indent_length=2")
    byo.subprocess_run_loud(argv, stdin=None)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/jq.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
