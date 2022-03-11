#!/usr/bin/env python3

"""
usage: bash.py [--help] [--noprofile] [--norc] ...

shell out to a host

options:
  --help       show this help message and exit
  --noprofile  launch without running shared startup files
  --norc       launch without running personal startup files

examples:
  bash --noprofile --norc
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
        bash --noprofile --norc
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
