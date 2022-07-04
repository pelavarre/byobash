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

quirks:
  classic IPython3 rudely opens a new Session, without '__file__', when given no Parms

examples:

  ipython3.py  &&: show these examples and exit
  ipython3.py --h  &&: show this help message and exit
  ipython3.py --  &&: todo: run as you like it

  ipython3 --classic --no-banner --no-autoindent --no-confirm-exit
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/ipython3.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
