#!/usr/bin/env python3

r"""
usage: tput.py [--h] COMMAND

send Commands to the Terminal

positional arguments:
  COMMAND  a command, such as 'clear' or 'reset'

options:
  --help   show this help message and exit

quirks:
  works in Mac, Linux, & Chrome GShell
  works well with: clear.py, echo.py, reset.py

examples:
  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  &&: fill Screens for test
  tput.py clear  &&: clear Terminal history, like ⌘K
  tput.py reset  &&: scroll the Rows on Screen, like ⌃L
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

        byo.exit()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/tput.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
