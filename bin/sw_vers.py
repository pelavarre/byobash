#!/usr/bin/env python3

"""
usage: sw_vers.py [--h]  ...

print macOS version

options:
  --help  show this help message and exit

quirks:
  classic Sw_Vers dumps Key-Value Pairs, when given no Parms
  goes well with:  lsb_release.py, uname.py

examples:

  sw_vers.py  # show these examples and exit
  sw_vers.py --h  # show this help message and exit
  sw_vers.py --  # todo: run as you like it

  sw_vers  # such as:  macOS 12.4 21F79
  sw_vers |grep ^ProductVersion: |awk '{print $2}'  # such as:  12.4

  :
  : Sep/2018 Mojave macOS X 10.14  # yearly major release date, miscoded as minor
  : Oct/2019 Catalina macOS X 10.15  # yearly major release date, miscoded as minor
  : Nov/2020 Big Sur macOS 11  # major release date
  : Oct/2021 Monterey macOS 12  # major release date
  :
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sw_vers.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
