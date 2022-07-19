#!/usr/bin/env python3

"""
usage: pbpaste.py [--h]

copy the main Os Copy/Paste Clipboard (aka Pasteboard) to Stdout

options:
  --help  show this help message and exit

quirks:
  goes well with:  pbcopy.py, pbedit.py
  Mac builds in PBPaste and PBCopy, but Linux & GShell don't
  classic PbPaste dumps the full Pasteboard, with no Scroll limit, when given no Parms
  classic PbPaste rudely dumps raw Paste, like 'less -r', unlike 'less -R' and 'less'

examples:

  pbpaste.py  # show these examples and exit
  pbpaste.py --h  # show this help message and exit
  echo hello copy-paste world |pbcopy.py --
  pbpaste.py --

  echo hello copy-paste world |qb/cv
  qb/cv

  echo -n hello endswidth open line |qb/cv
  qb/cv |expand.py --| tee >(qb/cv)
"""


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


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/pbpaste.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
