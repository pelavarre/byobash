#!/usr/bin/env python3

"""
usage: ssh-add.py

todo

options:
  --help       show this help message and exit

quirks:
  works well with:  ssh.py
  classic Ssh-Add rudely auth's forwarding your Creds, when given no Parms

examples:

  ssh-add.py  &&: show these examples and exit
  ssh-add.py --h  &&: show this help message and exit
  ssh-add.py --  &&: todo: run as you like it

  ssh-add -l
  ssh-add -L |grep ^ssh-rsa-cert |ssh-keygen -L -f - |grep Valid
  ssh.py --h
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/ssh-add.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
