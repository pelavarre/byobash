#!/usr/bin/env python3

r"""
usage: tee.py [-h] [-a] [FILE ...]

read from Stdin and write the bytes read into each File in order

positional arguments:
  FILE                  the file to drop trailing lines from (default: stdin)

options:
  -h, --help            show this help message and exit
  -a                    append to the Files that already exist, don't create those

notes:
  give Args or Stdin, or print a prompt, to stop more Tee's from hanging silently

examples:
  echo {A..Z} |tr ' ' '\n' | tee >(head -2) >(sleep 0; tail -3) > /dev/null
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
