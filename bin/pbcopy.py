#!/usr/bin/env python3

"""
usage: pbcopy.py [--h]

copy Stdin into the main Os Copy/Paste Clipboard (aka Pasteboard)

options:
  --help  show this help message and exit

quirks:
  goes well with:  pbedit.py, pbpaste.py
  Mac builds in PBPaste and PBCopy, but Linux & GShell don't
  classic PbCopy rudely hangs with no prompt, when given no Parms with no Stdin

examples:

  pbcopy.py  # show these examples and exit
  pbcopy.py --h  # show this help message and exit
  echo hello copy-paste world |pbcopy.py --
  pbpaste.py --

  echo hello copy-paste world |qb/cv
  qb/cv

  echo -n hello endswidth open line |qb/cv
  qb/cv |expand.py --| tee >(qb/cv)
"""


import byotools as byo


byo.exit(__name__)


# todo:
_ = """

integrate macOS 'AppKit.NSPasteboard.generalPasteboard' from 'pbpaste.py'

cv             |...  |cv  # my own custom macOS
pbpaste        |...  |pbcopy  # any merely standard macOS

wl-paste ...   |...  |wl-copy ...  # one Linux
xclip ...      |...  |xclip ...  # another Linux
xsel ...       |...  |xsl ...  # another Linux

Get-Clipboard  |...  |Set-Clipboard  # Windows

"""


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/pbcopy.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
