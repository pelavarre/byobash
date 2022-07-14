#!/usr/bin/env python3

r"""
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
  lsb_release.py --  # lsb_release -a 2>&1 |grep ^Desc

  lsb_release -a  # such as 5 lines to say:  Xenial Ubuntu 16.04.3 LTS
  lsb_release -a 2>&1 |grep ^Desc  # such as 1 line of:  Description:\tUbuntu 20.04 LTS
  lsb_release -a |grep ^Description: |awk '{print $3}'  # such as:  16.04.3

  :
  : Apr/2016 Xenial Ubuntu Linux 16.04  # major release date of "Long Term Stable" (LTS)
  : Apr/2018 Bionic Ubuntu Linux 18.04  # major release date
  : Apr/2020 Focal Ubuntu Linux 20.04  # major release date
  :
"""


import byotools as byo

import shpipes


byo.exit(__name__, shparms="--")


def main():
    pass


main.sponge_shverb = None  # FIXME

shpipe = "lsb_release -a 2>&1 |grep ^Desc"
shpipes.exit_via_shpipe(shpipe)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/lsb_release.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
