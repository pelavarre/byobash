#!/usr/bin/env python3

r"""
usage: echo.py [--h] [-e|-E] [-n] [WORD ...]

print some words

options:
  --help  show this help message and exit
  -n      print without closing the line
  -E      don't escape the \ backslant
  -e      do escape the \ backslant with \ abfnrtv 0 x, also \e and \c

note:
  \e is \x1B Esc
  \c cancels the rest: it stops the print and implies -n

bash install:

  function echo.py {
    local xc=$?
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      echo "+ exit $xc"
    else
      command echo.py "$@"
    fi
  }

examples:

  echo.py  &&: show these examples and exit

  rm /dev/null/child  &&: test Exit Code 1
  bash -c 'exit 3'  &&: test Exit Code 3
  echo.py -- &&: echo "+ exit $?"  &&: mention the last Exit Status ReturnCode once

  echo -ne '\e[H\e[2J\e[3J'  &&: clear Terminal history, like ⌘, but see:  clear.py --h

  echo -ne '\e[8;50;89t'  &&: change to 50 Rows x 89 Columns
  echo -ne '\e[8;'$(stty size |cut -d' ' -f1)';89t'  &&: change to 89 Columns
  echo -ne '\e[8;'$(stty size |cut -d' ' -f1)';101t'  &&: change to 101 Columns
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/echo.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
