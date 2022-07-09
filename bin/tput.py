#!/usr/bin/env python3

r"""
usage: tput.py [--h] VERB [ARG ...]

send Command Lines into the Terminal

positional arguments:
  VERB     choice of SubCommand, such as 'clear' or 'reset' (default: 'reset')
  ARG      choice of Options and Arguments

options:
  --help   show this help message and exit

quirks:

  works in Mac & Linux  # but FIXME: 'tput.py clear' at Linux/ GShel0
  works well with: clear.py, echo.py, reset.py

  Clear Py explains how 'tput clear' goes wrong in Mac, Linux, & GShell
  Reset Py explains how 'tput reset' goes wrong in Mac, Linux, & GShell

  classic TPut rudely declines to choose a Verb, when given no Parms

examples:

  tput.py  # show these examples and exit
  tput.py --h  # show this help message and exit
  tput.py --  # clear Terminal history quickly, like ⌘K

  qbin/cls  # clear Terminal history, like ⌘K
  tput.py reset  # clear Terminal history, like ⌘K
  tput.py clear  # scroll away the Rows on Screen, like ⌃L

  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  # fill Screens for test
"""


import sys


import byotools as byo


if __name__ == "__main__":

    parms = sys.argv[1:]

    esc = "\x1B"
    if parms in (["reset"], ["--", "reset"]):
        print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")
    elif parms in (["clear"], ["--", "clear"]):
        print(r"\e[H\e[2J".replace(r"\e", esc), end="")
    else:

        byo.exit(shparms="--")

        print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/tput.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
