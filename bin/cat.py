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
                        forward the input formatted as a Python String or Bytes Literal

quirks:
  give Args or Stdin, or print a prompt, to stop more Cat's from hanging silently

examples:
  python -c 'import this' |tail -n +3 |cat -n |expand  &&: demo Cat N
  seq 5|cat -n |cat.py -v  &&: show Line-Breaks inside a Python String Literal
  echo $'\xC0\x80' |cat.py -v  &&: show UnicodeDecodeError inside a Python Bytes Literal
  ... |cat -n |expand  &&: make Spaces of the Cat N Tabs
  ... |cat -etv  &&: show the Spaces, if any, that precede Line-Break's
"""
# todo: code the Python String/Bytes Literals


import byotools as byo


if __name__ == "__main__":

    byo.exit()

    # FIXME distinguish 'cat.py -tvn' as showing U+00A0 Nbsp and ending all lines

# copied from:  git clone https://github.com/pelavarre/byobash.git
