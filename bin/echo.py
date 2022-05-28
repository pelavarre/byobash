#!/usr/bin/env python3

r"""
usage: echo.py [-h] [-e|-E] [-n] [WORD ...]

print some words

options:
  -h, --help  show this help message and exit
  -n          print without closing the line
  -E          don't escape the \ backslant
  -e          do escape the \ backslant with \ abfnrtv 0 x, also \e and \c

note:
  \e is \x1B Esc
  \c stops the print and implies -n

examples:
  echo -n $'\e[8;50;89t'  &&: revert Terminal to 50 Rows x 89 Columns
  echo -ne '\e[H\e[2J'  &&: echo -ne '\e[2J\e[3J\e[H'  &&: clear Terminal history
  which -a echo  &&: list variations of Echo
  command echo -E hello  &&: run the first Echo saved outside Memory as File
"""


import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    doc = __main__.__doc__
    epilog = doc[doc.index("examples:") :]
    tests = "\n".join(epilog.splitlines()[1:])
    print(textwrap.dedent(tests))
