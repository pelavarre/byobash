#!/usr/bin/env python3

r"""
usage: cat.py [--h] [-E] [-e] [-n] [-T] [-t] [-v] [FILE ...]

copy each line of input bytes (or chars) to output (as if "cat"enating them slowly)

positional arguments:
  FILE                  a file to copy out (such as '-' to mean Stdin)

options:
  --help                show this help message and exit
  -E, --show-ends       print each \n lf as $ lf
  -e                    call for -E and -v
  -n, --number          number each line of output, up from 1, with \t tabs
  -T, --show-tabs       show each \t tab as \ t backslash tee
  -t                    call for -T and -v
  -v, --show-nonprinting
                        keep \n, \t, & us-ascii r"[ -~]", convert the rest to \ escapes

notes:
  give Args or Stdin, or print a prompt, to stop more Cat's from hanging silently

examples:
  python -c 'import this' |tail -n +3 |cat -n |expand
  ... |cat -n |expand
  ... |cat -etv
"""


import byotools


if __name__ == "__main__":

    byotools.exit()

    # FIXME distinguish 'cat.py -tvn' as showing U+00A0 Nbsp and ending all lines

# copied from:  git clone https://github.com/pelavarre/byobash.git
