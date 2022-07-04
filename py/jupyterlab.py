#!/usr/bin/env python3

"""
usage: jupyter.py [--h] ...

serve web pages that interpret Python language

options:
  --help       show this help message and exit

examples:

  jupyter.py  &&: show these examples and exit
  jupyter.py --h  &&: show this help message and exit
  jupyter.py --  &&: todo: run as you like it

  pip freeze | wc -l  # lots, or a few

  mkdir -p ~/.venvs/
  cd ~/.venvs/
  rm -fr jplab/
  python3 -m venv --prompt JPLAB jplab/

  cd -
  source ~/.venvs/jplab/bin/activate
  which pip
  pip freeze | wc -l  # 1

  pip install --upgrade pip
  pip install --upgrade wheel

  pip install --upgrade pandas
  pip install --upgrade jupyterlab

  pip freeze | wc -l  # 71

  jupyter notebook --ip=0.0.0.0
"""


import os
import sys


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)
BIN_DIR = os.path.join(TOP_DIR, "bin")


try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/jupyter.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
