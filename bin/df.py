#!/usr/bin/env python3

"""
usage: df.py [-h]

help guess when file writes will fail because disk full

options:
  -h, --help  show this help message and exit

examples:
  echo ... && df |awk '{print $5"\t"$0}' |sort -n |tail -3  &&: show the three most full
"""


import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    doc = __main__.__doc__
    epilog = doc[doc.index("examples:") :]
    tests = "\n".join(epilog.splitlines()[1:])
    print(textwrap.dedent(tests))
