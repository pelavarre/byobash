#!/usr/bin/env python3

r"""
usage: reset.py [--h]

wipe the Screen, delete the Scrollback, and leave the Cursor at Top Left

options:
  --help  show this help message and exit

quirks:

  works in Mac & Linux
  works well with: clear.py, echo.py, tput.py

  Mac 'reset' scrolls top Screen Row into Scrollback and doesn't delete Scrollback
  Mac & Linux 'reset' waste 1000 ms of time to no purpose
  GShell 'reset' goes wrong the same as Linux 'clear'

  classic Reset rudely defaults to show no new output, when given no Parms

examples:

  reset.py  # show these examples and exit
  reset.py --h  # show this help message and exit
  reset.py --  # clear Terminal history quickly, like ⌘K

  qbin/cls  # clear Terminal history, like ⌘K
  clear.py -x  # scroll the Rows on Screen, like ⌃L

  echo -ne '\e[H\e[2J\e[3J'  # clear Terminal History, like ⌘K
  echo -ne '\e[8;50;89t'  # change to 50 Rows x 89 Columns
  tput reset  # alt Clear
  reset  # alt Clear, commonly includes a 1s sleep

  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  # fill Screens for test
  reset 2>&1 |tee >(hexdump -C)  # call and trace Reset
  tput reset 2>&1 |tee >(hexdump -C)  # call and trace TPut Reset
"""
# todo: decipher the Esc Sequences written by Reset


import byotools as byo


if __name__ == "__main__":

    byo.exit(shparms="--")

    esc = "\x1B"
    print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/reset.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
