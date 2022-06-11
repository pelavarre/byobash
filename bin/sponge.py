#!/usr/bin/env python3

r"""
usage: sponge.py [--h]

read all of Stdin, echo its Eof into Stderr, and only then write it all to Stdout

options:
  --help  show this help message and exit

note:
  Linux Terminal Stdin echoes ⌃D EOF as "" without "\n", vs macOS as "^D" without "\n"

examples:
  cat |sponge.py --  &&: let you finish typing, and press ⌃D EOF, before echoing it all
  echo $'\xC0\x80' |sponge.py -- |hexdump -C  &&: forward UnicodeDecodeError accurately
"""


import sys

import byotools


def main():

    if sys.argv[1:] != "--".split():

        byotools.exit()

    in_bytes = sys.stdin.buffer.read()

    if sys.stdin.isatty():
        sys.stderr.write("\n")
        sys.stderr.flush()

    sys.stdout.buffer.write(in_bytes)


if __name__ == "__main__":
    main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
