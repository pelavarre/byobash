#!/usr/bin/env python3

"""
usage: ipython3.py [--h] [--classic] [--no-banner] [--no-autoindent] [--no-confirm-exit]

interpret Python language

options:
  --help             show this help message and exit
  --classic          look and feel more like ordinary Python3
  --no-banner        launch without printing a welcome
  --no-autoindent    take input as source code, not as unindented source code
  --no-confirm-exit  take Control+D to mean exit

examples:
  ipython3 --classic --no-banner --no-autoindent --no-confirm-exit
"""


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
