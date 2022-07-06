#!/usr/bin/env python3

"""
usage: bash.py [--h] [--noprofile] [--norc] ...

shell out to a host

options:
  --help       show this help message and exit
  --noprofile  launch without running shared startup files
  --norc       launch without running personal startup files

quirks:
  classic Bash rudely opens a new Session, with an empty "$@", when given no Parms
  classic Bash rudely places no Scroll Limits on Sh Commands
  todo: limit Control Sequences dumped into Tty, a la 'less', 'less -R', 'less -r'

examples:

  ls ~/.bashrc ~/.bash_profile ~/.profile

  bash.py  &&: show these examples and exit
  bash.py --h  &&: show this help message and exit
  bash.py --  &&: todo: run as you like it

  bash --noprofile --norc  &&: run with less local quirks
  export |grep SHLVL  &&: show how deeply incepted
  set |grep -e ^PS1= -e ^PS4=  &&: show the outer and incepted shell prompts
"""
# talk out how best to clear Bash History for a Bash Screen
# todo: tab completion of:  mv -i *.jp
# ⌃X⌃E to edit a line


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/bash.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
