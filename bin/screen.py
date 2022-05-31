#!/usr/bin/env python3

"""
usage: screen.py [--h] [-t] ...

limit a Terminal window to a few rows and columns shared between hosts

options:
  --help  show this help message and exit
  -t      forward control of the local terminal (-tt for more force)

examples:
  rm -fr screenlog.0  # delete the default logfile
  screen -L -S Screen1  # make a screen, give it a name, and log what happens
  screen -ls  # list how many you have
  screen ls  # say '[screen is terminating]'
  screen -d  # ⌃A D  # detach the one you're in
  screen -ls
  screen -x Screen1  # attach the one you like
  echo $STY  # say if you're inside a Screen or not
  # ⌃A ?  # show Keyboard Shortcuts
  # ⌃A A  # send an ordinary Control+A keystroke
  # ⌃A Esc  # enter the Less mode, so ⌃B means page back
  # Esc  # exit the Less mode
  screen -X hardcopy -h t.transcript  # make a log of the last few rows shown
  exit  # ⌃D  # close and delete this Screen
  screen -ls
  cat screenlog.0  # interpret the Esc sequences in the default logfile
"""
#  screen vi  # demo as prefix
# screen.py -r  # pick the latest, and autonumber them a b c ..., don't demand just one


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
