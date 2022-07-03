#!/usr/bin/env python3

r"""
usage: reset.py [--h]

wipe the Screen, delete the Scrollback, and leave the Cursor at Top Left

options:
  --help  show this help message and exit

quirks:

  Byo Reset Py works in Mac, Linux, & Chrome GShell

  Mac Reset scrolls top Screen Row into Scrollback and doesn't delete Scrollback
  Mac refuses to trace Reset:  reset: standard error: Inappropriate ioctl for device
  Chrome GShell Reset works
  Safari GShell Reset breaks like Terminal Linux 'clear -x' & doesn't delete Scrollback

examples:

  reset.py --  &&: clear Terminal history quickly, like ⌘K
  clear.py -x  &&: scroll the Rows on Screen, like ⌃L

  echo -ne '\e[H\e[2J\e[3J'  &&: clear Terminal History, like ⌘K
  echo -ne '\e[8;50;89t'  &&: change to 50 Rows x 89 Columns
  tput reset  &&: alt Clear
  reset  &&: alt Clear, commonly includes a 1s sleep

  echo && seq 40 && echo && seq 50 && echo && seq 60 && echo  &&: fill Screens for test
  reset 2>&1 |tee >(hexdump -C)  &&: call and trace Reset
  tput reset 2>&1 |tee >(hexdump -C)  &&: call and trace TPut Reset
"""
# todo: decipher the Esc Sequences written by Reset


import byotools as byo


if __name__ == "__main__":

    byo.exit(shparms="--")

    esc = "\x1B"
    print(r"\e[H\e[2J\e[3J".replace(r"\e", esc), end="")


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/reset.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
