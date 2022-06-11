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
  \c stops the print and implies -n
  try 'echo' with no args, when your Echo mistakes 'echo --' to mean 'echo.py -- --'

examples:
  echo.py  &&: call Echo Py with no args to show these examples
  echo.py --  &&: echo one empty line
  echo -n $'\e[8;50;89t'  &&: revert Terminal to 50 Rows x 89 Columns
  echo -ne '\e[H\e[2J'  &&: echo -ne '\e[2J\e[3J\e[H'  &&: clear Terminal history
  which -a echo  &&: list variations of Echo
  command echo -E hello  &&: run the first Echo saved outside Memory as File
"""


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
