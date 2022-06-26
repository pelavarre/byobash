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


import sys


import byotools as byo


try:
    import AppKit  # often from VEnv of:  pip install --upgrade pyobjc
except ModuleNotFoundError:
    AppKit = None


if AppKit:

    pb = AppKit.NSPasteboard.generalPasteboard()

    pbpaste = pb.stringForType_(AppKit.NSStringPboardType)
    in_chars = str(pbpaste)

    print(in_chars)

    out_chars = in_chars + in_chars

    pbcopy = out_chars
    nsobject = AppKit.NSObject.alloc().init()
    pb.declareTypes_owner_([AppKit.NSStringPboardType], nsobject)
    pb.setString_forType_(pbcopy, AppKit.NSStringPboardType)

    print(out_chars)

    sys.exit(3)


byo.exit(__name__)


# todo:
_ = """
"""


# todo: posted as
# copied from:  git clone https://github.com/pelavarre/byobash.git
