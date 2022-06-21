#!/usr/bin/env python3

r"""
usage: head.py [--h] [-v] [-n COUNT] [FILE ...]

show just the leading lines of a file

positional arguments:
  FILE                  the file to drop trailing lines from (default: stdin)

options:
  --help                show this help message and exit
  -v                    drop the leading lines instead, show the others
  -n COUNT, --lines COUNT
                        how many leading lines to show (default: 25)

quirks::
  give '-' in place of '-n ' to get the same result more easily
  give '-n +' into Tail's to mean drop leading lines, and just '+' sometimes works too
  give '-25' to occupy as much of a 2022 display as '-10' occupied a 1972 display
  give Args or Stdin, or print a prompt, to stop more Head's from hanging silently

examples:
  python -c 'import this' |head.py -v 3|cat -n |expand
  python -c 'import this' |tail -n +3 |cat -n |expand
  python -c 'import this' |awk 'NR==3{f=1} f{print}' |cat -n |expand
  vim $(head.py -v -9 bin/*.py |tail -n +11)
  echo {A..Z} |tr ' ' '\n' | tee >(head -2) >(sleep 0; tail -3) > /dev/null
"""


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
