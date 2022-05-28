#!/usr/bin/env python3

r"""
usage: head.py [-h] [-v] [-n COUNT] [FILE ...]

show just the leading lines of a file

positional arguments:
  FILE                  the file to drop trailing lines from (default: stdin)

options:
  -h, --help            show this help message and exit
  -v                    drop the leading lines instead, show the others
  -n COUNT, --lines COUNT
                        how many leading lines to show (default: 10)

notes:
  give '-' in place of '-n ' to get the same result more easily
  give '-n +' to mean drop leading lines, and just '+' sometimes works too
  give Args or Stdin, or print a prompt, to stop more Tail's from hanging silently

examples:
  python -c 'import this' |head.py -v 3|cat -n |expand
  python -c 'import this' |tail -n +3 |cat -n |expand
  python -c 'import this' |awk 'NR==3{f=1} f{print}' |cat -n |expand
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
