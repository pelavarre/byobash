#!/usr/bin/env python3

"""
usage: bash.py [--help] [--noprofile] [--norc] ...

shell out to a host

options:
  --help       show this help message and exit
  --noprofile  launch without running shared startup files
  --norc       launch without running personal startup files

examples:
  bash --noprofile --norc  &&: run with less local quirks
  export |grep SHLVL  &&: show how deeply incepted
  set |grep -e ^PS1= -e ^PS4=  &&: show the outer and incepted shell prompts
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


# copied from:  git clone https://github.com/pelavarre/byobash.git
