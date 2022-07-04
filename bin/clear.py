#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

wipe the Screen, delete the Scrollback, and leave the Cursor at Top Left

options:
  --help  show this help message and exit
  -x      actually don't delete the Scrollback, just scroll the Rows on Screen into it

quirks:

  works in Mac & Linux  # but FIXME: 'clear.py -x' at Linux/GShell
  works well with: echo.py, reset.py, tput.py

  Linux 'clear -x' loses the Rows on Screen, doesn't scroll them into Scrollback
  Linux 'clear' says 3J H 2J in place of H 2 J 3J, so doesn't delete all Scrollback
  Linux 'clear && clear' says 3J H 2J 3J H 2J, to wipe Scrollback without deleting it

  GShell 'clear' goes wrong the same as Linux

  classic Clear rudely defaults to show no new output, when given no Parms

examples:

  clear.py  &&: show these examples and exit
  clear.py --h  &&: show this help message and exit
  clear.py --  &&: clear Terminal history, like ⌘K
  qbin/cls  &&: clear Terminal history, like ⌘K

  clear.py -x  &&: scroll the Rows on Screen, like ⌃L

  echo -ne '\e[H\e[2J\e[3J'  &&: clear Terminal History, like ⌘K
  echo -ne '\e[H\e[2J'  &&: scroll the Rows on Screen, like ⌃L
  echo -ne '\e[8;50;89t'  &&: change to 50 Rows x 89 Columns
  tput clear  &&: alt Clear
  reset  &&: alt Clear, commonly includes a 1s sleep

  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  &&: fill Screens for test
  clear 2>&1 |tee >(hexdump -C)  &&: call and trace Clear
  tput clear 2>&1 |tee >(hexdump -C)  &&: call and trace TPut Clear

  diff -u <(clear |hexdump -C) <(tput clear |hexdump -C)  &&: show no diff
"""


import sys


import byotools as byo


if __name__ == "__main__":

    parms = sys.argv[1:]

    esc = "\x1B"
    if parms == ["--"]:
        print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")
    elif parms == ["-x"]:
        print(r"\e[H\e[2J".replace(r"\e", esc), end="")
    else:

        byo.exit()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/clear.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
