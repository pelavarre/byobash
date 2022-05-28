#!/usr/bin/env python3

r"""
usage: cat.py [-h] [-E] [-e] [-n] [-T] [-t] [-v] [FILE ...]

copy each line of input bytes (or chars) to output (as if "cat"enating them slowly)

positional arguments:
  FILE                  a file to copy out (default: stdin)

options:
  -h, --help            show this help message and exit
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
