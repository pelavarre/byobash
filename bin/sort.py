#!/usr/bin/env python3

"""
usage: sort.py [--h] [-tSEP [-kK,K ...] [-]

read all of Stdin, end the last Line if needed, sort the Lines, write to Stdout

options:
  --help  show this help message and exit
  -tSEP   the separator between fields (inexpressible default r"[ ]+")
  -kK,K   column to sort by, numbered up from 1
  -n      sort by numeric value, not by string value
  -R      shuffle, don't sort
  -r      reverse the sort

quirks:

  goes well with:  sponge.py
  Linux Terminal Stdin echoes ⌃D TTY EOF as "" w/out "\n", vs macOS as "^D" without "\n"

examples:

  sort.py  # show these examples and exit
  sort.py --h  # show this help message and exit
  sort.py --  # same as:  sort.py -

  echo drop=do drop2=do |tr ' ' '\n' |sort -t= -k1,1  # sort 'key=value' pairs by key
  echo $'\xC0\x80' |sort.py -- |hexdump -C  # do sort, don't say 'Illegal byte sequence'

"""

import sys


import byotools as byo


def main():

    byo.exit(shparms="--")

    if sys.stdin.isatty():
        byo.stderr_print("Press ⌃D TTY EOF to quit")

    with open("/dev/stdin", "rb") as reading:
        ibytes = reading.read()

    ichars = ibytes.decode(errors="SurrogateEscape".casefold())

    if sys.stdin.isatty():
        byo.stderr_print()

    lines = ichars.splitlines(keepends=False)
    lines.sort()

    ochars = "\n".join(lines) + "\n"
    obytes = ochars.encode(errors="SurrogateEscape".casefold())

    with open("/dev/stdout", "wb") as writing:
        writing.write(obytes)


if __name__ == "__main__":
    main()


#   goes well with:  sponge.py
# classic Sort rudely hangs with no prompt, when given no Parms with no Stdin


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sort.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
