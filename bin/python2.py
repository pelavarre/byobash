#!/usr/bin/env python3

# virtualenv --python=python2 --prompt=PY2 py2  # for work based in history as stale as Aug/2015 and older

"""
usage: python2.py [--h]  ...

interpret Python 2 language

options:
  --help         show this help message and exit
  -V, --version  print Python version (-VV for more force)

quirks:
  classic Python2 rudely opens a new Session, without '__file__', when given no Parms

examples:

  python2.py  &&: show these examples and exit
  python2.py --h  &&: show this help message and exit
  python2.py --  &&: todo: run as you like it

  : Jul/2010 Python 2.7  # minor release date
  : Jun/2016 Python 2.7.12  # micro release date
  : Mar/2019 Python 2.7.16  # micro release date
  : Oct/2019 Python 2.7.17  # micro release date
  : Apr/2020 Python 2.7.18  # micro release date
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/python2.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
