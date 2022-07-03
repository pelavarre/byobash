#!/usr/bin/env python3

r"""
usage: clear.py [--h] [-x]

wipe the Screen, delete the Scrollback, and leave the Cursor at Top Left

options:
  --help  show this help message and exit
  -x      instead, scroll the Rows on Screen, away into the Scrollback

quirks:

  Byo Clear Py works in Mac, Linux, & Chrome GShell

  Mac Clear scrolls the Rows on Screen, away into the Scrollback, same as 'clear.py -x'
  Linux 'clear -x' loses the Rows on Screen, doesn't scroll them into Scrollback
  Linux Clear says 3J H 2J in place of H 2 J 3J, doesn't delete all Scrollback
  Linux Clear called twice says 3J H 2J 3J H 2J, so wipes Scrollback, doesn't delete it
  Chrome GShell Clear works, but its 'clear -x' breaks like Terminal Linux
  Safari GShell Clear breaks like Terminal Linux 'clear -x' & doesn't delete Scrollback

examples:

  clear.py  &&: show these examples and exit

  cls  &&: clear Terminal history, like ⌘K

  clear.py --  &&: clear Terminal history, like ⌘K
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
