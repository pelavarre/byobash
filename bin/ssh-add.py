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


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
