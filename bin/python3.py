#!/usr/bin/env python3

# python3 -m venv --prompt=PY3 py3  # standard since Sep/2015 Python 3.5

# python3 -i
# echo |python3 -m pdb
# pdb pm post-mortem
# pdb bt back-trace

"""
usage: python3.py [--h]  ...

interpret Python 3 language

options:
  --help         show this help message and exit
  -V, --version  print Python version (-VV for more force)

quirks:
  falls back to run 'python.py' instead, except at 'python3.py' and 'python3.py --help'
  classic Python3 rudely opens a new Session, without '__file__', when given no Parms

examples:

examples:

  python3.py  &&: show these examples and exit
  python3.py --h  &&: show this help message and exit
  python3.py --  &&: todo: run as you like it

  : Dec/2008 Python 3  # major release date
  : Feb/2011 Python 3.2  # minor release date
  : Sep/2012 Python 3.3  # minor release date
  : Mar/2014 Python 3.4  # minor release date
  : : Feb/2015 Python 3.4.3  # micro release date
  : Sep/2015 Python 3.5  # minor release date
  : : Jun/2016 Python 3.5.2  # micro release date
  : Dec/2016 Python 3.6  # minor release date
  : : Mar/2018 Python 3.6.5  # micro release date
  : : Jul/2019 Python 3.6.9  # micro release date
  : Dec/2016 CPython 3.6  # minor release date  # Dict Keys ordered by Insertion
  : Jun/2018 Python 3.7  # minor release date  # Dict Keys ordered by Insertion
  : : Mar/2019 Python 3.7.3  # micro release date
  : : Dec/2019 Python 3.7.6  # micro release date
  : Oct/2019 Python 3.8  # minor release date
  : : Feb/2020 Python 3.8.2  # micro release date
  : : May/2021 Python 3.8.10  # micro release date
  : Oct/2020 Python 3.9  # minor release date
  : : Dec/2020 Python 3.9.1  # micro release date
  : : Apr/2021 Python 3.9.4  # micro release date
  : : May/2021 Python 3.9.5  # micro release date
  : : Jun/2021 Python 3.9.6  # micro release date
  : Oct/2021 Python 3.10  # minor release date
  : : Mar/2022 Python 3.10.4  # micro release date
"""

# https://packages.ubuntu.com/ > Long Term Stable (LTS)
# https://packages.ubuntu.com/bionic/python/ Ubuntu Apr/2018  => Jul/2019 Python 3.6.9
# https://packages.ubuntu.com/focal/python/ Ubuntu Apr/2020  => May/2021 Python 3.8.10
# https://packages.ubuntu.com/jammy/python/ Ubuntu Apr/2022  => Mar/2022 Python 3.10.4


import byotools as byo

import python as python


if __name__ == "__main__":

    byo.exit_via_testdoc()  # python3.py

    byo.exit_via_argdoc()  # python3.py --help

    python.main()


_ = """

python3 AttributeError: 'Namespace' object has no attribute 'c'
should tell us

from argparse import Namespace as space

s = space(a=1, b=2)
print(s)
# Namespace(a=1, b=2)

print(list(_ for _ in dir(s) if not _.startswith("_")))
# ['a', 'b']
print(list(vars(s).keys()))
# ['a', 'b']

s.c
# AttributeError: 'Namespace' object has no attribute 'c'

"""


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/python3.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
