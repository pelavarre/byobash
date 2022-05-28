#!/usr/bin/env python3

r"""
usage: reset.py [-h] [-x]

erase the lines of the Terminal and start again in the top left

options:
  --help  show this help message and exit

examples:
  reset  &&: 1000ms slow, but more reliable than:  clear
  reset 2>&1 |hexdump -C  &&: disclose what bytes Reset writes, if at Linux
"""
# todo: doc what

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
