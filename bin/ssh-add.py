#!/usr/bin/env python3

"""
usage: ssh-add.py

todo

options:
  --help       show this help message and exit

examples:
  ssh-add -l
  ssh-add -L |grep ^ssh-rsa-cert |ssh-keygen -L -f - |grep Valid
  ssh.py --h
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/ssh-add.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
