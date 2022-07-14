#!/usr/bin/env python3

"""
usage: lspci.py ...

sketch the tree of plugged-in PCI devices

options:
  --help  show this help message and exit
  -t      sketch the tree as a tree
  -vvv    max verbosely

quirks:
  classic LsPci dumps all the Top Lines, with no Scroll limit, when given no Parms
  Linuxes install LsPci by default

examples:

  lspci.py  # show these examples and exit
  lspci.py --h  # show this help message and exit
  lspci.py --  # todo: run as you like it

  lspci -t -vvv |less -FIRX
  lspci -t -nn -vvv |less -FIRX
"""

# lspci -t -nn -vvv |less -FIRX
# -+-[0000:12]-+-00.0  Acme Corporation Widget [8086:89ab]
# per the 'misc/pci.ids' in the '/usr/share/' dir, from https://pci-ids.ucw.cz


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/lspci.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
