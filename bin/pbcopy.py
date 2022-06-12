#!/usr/bin/env python3

"""
usage: pbcopy.py [--h]

copy Stdin into the main Os Pasteboard (aka Clipboard)

options:
  --help  show this help message and exit

quirks:
  switch to Apple macOS, out of Linux or GShell, to find PBCopy and PBPaste built-in

examples:
  function c () { echo + pbcopy >&2; pbcopy "$@"; }
  function v () { echo + pbpaste >&2; pbcopy "$@"; }
  echo hello copy-paste world |c
  v
"""
# todo: function cv () { ... pbcopy when stdin is not tty ... }
# todo: function cv () { ... pbpaste when stdin is tty ... }
# todo: function cv () { ... tee >(pbcopy) when stdin/stdout both not tty ... }


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
