#!/usr/bin/env python3

r"""
usage: sed.py [--h] [-i BAK] [-n] [[-e CODE] ...] [FILE ...]

edit

positional arguments:
  FILE     one File to edit

options:
  --help   show this help message and exit
  -i BAK   the File Ext to add to name the backups of the edited File's
  -n       run without the default Code of:  1,$p
  -e CODE  some Code to run

quirks:
  goes well with:  head.py, tac.py, tail.py, tee.py
  often forwards the last line as is, without adding a line break to close it
  classic Sed rudely hangs with no prompt, when given no Parms with no Stdin

examples:

  sed.py  # show these examples and exit
  sed.py --h  # show this help message and exit
  sed.py --  # todo: run as you like it

  sed -i~ 's,STALE,FRESH,g' *.py  # global edit find search replace
  echo a b c d e |tr ' ' '\n' |sed -n -e '1p' -e '$p'  # first, last
  echo a b c d e |tr ' ' '\n' |sed -n -e '1,2p' -e $'3i\\\n...' -e '$p'  # head, tail

  echo a b c |tr ' ' '\n' |sed 's,.*,&\n,'  # insert empty lines between lines

  echo $'\xCF\x4D\x2D' |sed 's,^,,'  # 'sed: RE error: illegal byte sequence' at Mac
"""

# todo: grow default w Screen Height
# todo: demo how to code Sed to replace with color, a la:  grep --color=yes

# todo: stop hassling me with:  sed: -e expression #1, char 7: unterminated `s' command


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sed.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
