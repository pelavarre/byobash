#!/usr/bin/env python3

"""
usage: python2.py [-h]  ...

interpret Python language

options:
  -h, --help     show this help message and exit
  -V, --version  print Python version (-VV for more force)

examples:
  : Jul/2010 Python 2.7  # minor release date
  : Jun/2016 Python 2.7.12  # micro release date
  : Mar/2019 Python 2.7.16  # micro release date
  : Oct/2019 Python 2.7.17  # micro release date
  : Apr/2020 Python 2.7.18  # micro release date
"""

# FIXME: add ArgParse


import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    SUGGESTION = textwrap.dedent(
        """
        : Jul/2010 Python 2.7  # minor release date
        : Jun/2016 Python 2.7.12  # micro release date
        : Mar/2019 Python 2.7.16  # micro release date
        : Oct/2019 Python 2.7.17  # micro release date
        : Apr/2020 Python 2.7.18  # micro release date
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
