#!/usr/bin/env python3

r"""
usage: tail.py [--h] [-v] [-n COUNT] [FILE ...]

show just the leading lines of a file

positional arguments:
  FILE                  the file to drop trailing lines from (default stdin)

options:
  --help                show this help message and exit
  -v                    drop the leading lines instead, show the others
  -n COUNT, --lines COUNT
                        how many leading lines to show (default 25)

quirks:

  goes well with:  head.py, sed.py, tee.py
  classic Tail rudely hangs with no prompt, when given no Parms with no Stdin

  give '-' in place of '-n ' to get the same result more easily
  give '-n +' to mean drop leading lines, and just '+' sometimes works too
  give '-25' to occupy as much of a 2022 display as '-10' occupied a 1972 display
  give Args or Stdin, or print a prompt, to stop more Tail's from hanging silently

examples:

  tail.py  # show these examples and exit
  tail.py --h  # show this help message and exit
  tail.py --  # todo: run as you like it

  python -c 'import this' |tail -n +3 |cat -n |expand
  python -c 'import this' |awk 'NR==3{f=1} f{print}' |cat -n |expand
  python -c 'import this' |head.py -v 3|cat -n |expand

  echo a b c d e f |tr ' ' '\n' |sed -n -e '1p' -e '$p'
  echo a b c d e f |tr ' ' '\n' |sed -n -e '1,2p' -e $'3i\\\n...' -e '$p'
  echo a b c d e f |tr ' ' '\n' | tee >(head -2) >(sleep 0; tail -3) > /dev/null
"""

# todo: grow default w Screen Height


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/tail.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
