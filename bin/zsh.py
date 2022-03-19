#!/usr/bin/env python3

"""
usage: zsh.py [--help] [-f] ...

shell out to a host

options:
  --help  show this help message and exit
  -f      launch without running startup files

examples:
  export |grep SHLVL
  zsh -f
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
        export |grep SHLVL
        zsh -f
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
