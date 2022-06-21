#!/usr/bin/env python3

"""
usage: pbpaste.py [--h]

copy the main Os Pasteboard (aka Clipboard) to Stdout

options:
  --help  show this help message and exit

quirks:
  switch to Apple macOS, out of Linux or GShell, to find PBPaste and PBCopy built-in

examples:
  function c () { echo + pbcopy >&2; pbcopy "$@"; }
  function v () { echo + pbpaste >&2; pbcopy "$@"; }
  echo hello copy-paste world |c
  v
  ( pbpaste; echo )  # always close the last line
"""
# todo: function cv () { ... pbcopy when stdin is not tty ... }
# todo: function cv () { ... pbpaste when stdin is tty ... }
# todo: function cv () { ... tee >(pbcopy) when stdin/stdout both not tty ... }


import byotools as byo


byo.exit(__name__)


# copied from:  git clone https://github.com/pelavarre/byobash.git
