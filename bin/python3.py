#!/usr/bin/env python3

"""
usage: python3.py [-h]  ...

interpret Python language

options:
  -h, --help     show this help message and exit
  -V, --version  print Python version (-VV for more force)

examples:
  : Dec/2008 Python 3  # major release date
  : Feb/2011 Python 3.2  # minor release date
  : Sep/2012 Python 3.3  # minor release date
  : Mar/2014 Python 3.4  # minor release date
  : : Feb/2015 Python 3.4.3  # micro release date
  : Sep/2015 Python 3.5  # minor release date
  : : Jun/2016 Python 3.5.2  # micro release date
  : Dec/2016 Python 3.6  # minor release date
  : : Jul/2019 Python 3.6.9  # micro release date
  : Dec/2016 CPython 3.6  # minor release date  # key-insertion-ordered dict's
  : Jun/2018 Python 3.7  # minor release date  # key-insertion-ordered dict's
  : : Mar/2019 Python 3.7.3  # micro release date
  : : Dec/2019 Python 3.7.6  # micro release date
  : Oct/2019 Python 3.8  # minor release date
  : : May/2021 Python 3.8.10  # micro release date
  : Oct/2020 Python 3.9  # minor release date
  : : Dec/2020 Python 3.9.1  # micro release date
  : : Apr/2021 Python 3.9.4  # micro release date
  : : May/2021 Python 3.9.5  # micro release date
  : : Jun/2021 Python 3.9.6  # micro release date
  : Oct/2021 Python 3.10  # minor release date
"""

# https://packages.ubuntu.com/bionic/python/ Ubuntu Apr/2018  => Jul/2019 Python 3.6.9
# https://packages.ubuntu.com/focal/python/ Ubuntu Apr/2020  => May/2021 Python 3.8.10

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
        : Dec/2008 Python 3  # major release date
        : Feb/2011 Python 3.2  # minor release date
        : Sep/2012 Python 3.3  # minor release date
        : Mar/2014 Python 3.4  # minor release date
        : : Feb/2015 Python 3.4.3  # micro release date
        : Sep/2015 Python 3.5  # minor release date
        : : Jun/2016 Python 3.5.2  # micro release date
        : Dec/2016 Python 3.6  # minor release date
        : : Jul/2019 Python 3.6.9  # micro release date
        : Dec/2016 CPython 3.6  # minor release date  # key-insertion-ordered dict's
        : Jun/2018 Python 3.7  # minor release date  # key-insertion-ordered dict's
        : : Mar/2019 Python 3.7.3  # micro release date
        : : Dec/2019 Python 3.7.6  # micro release date
        : Oct/2019 Python 3.8  # minor release date
        : : May/2021 Python 3.8.10  # micro release date
        : Oct/2020 Python 3.9  # minor release date
        : : Dec/2020 Python 3.9.1  # micro release date
        : : Apr/2021 Python 3.9.4  # micro release date
        : : May/2021 Python 3.9.5  # micro release date
        : : Jun/2021 Python 3.9.6  # micro release date
        : Oct/2021 Python 3.10  # minor release date
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
