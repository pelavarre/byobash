#!/usr/bin/env python3

"""
usage: lsb_release.py [--h] [-a] ...

print Linux Standard Base version, like to distinguish one Ubuntu LTS from the next

options:
  --help  show this help message and exit
  -a, --all  show Distributor Id, Description, Release, and Codename

quirks:
  goes well with:  sw_vers.py, uname.py
  but classic Lsb_Release, given no parms, commonly spits 'No LSB modules are available'
  Ubuntu Linux made 'cat /etc/lsb-release' work before they made 'lsb-release -a' work

examples:

  lsb_release.py  # show these examples and exit
  lsb_release.py --h  # show this help message and exit
  lsb_release.py --  # todo: run as you like it

  lsb_release -a  # such as:  Xenial Ubuntu 16.04.3 LTS
  lsb_release -a |grep ^Description: |awk '{print $3}'  # such as:  16.04.3

  :
  : Apr/2016 Xenial Ubuntu Linux 16.04  # major release date of "Long Term Stable" (LTS)
  : Apr/2018 Bionic Ubuntu Linux 18.04  # major release date
  : Apr/2020 Focal Ubuntu Linux 20.04  # major release date
  :
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/lsb_release.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
