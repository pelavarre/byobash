#!/usr/bin/env python3

"""
usage: ls.py [--h] [TOP ...]

show the files and dirs inside a dir

positional arguments:
  TOP     the name of a dir or file to show

options:
  --help  show this help message and exit
  -1      show as one column of one file or dir per line
  -C      show as multiple columns

quirks:
  works well with cp.py, mv.py, rm.py, rmdir.py, touch.py
  classic Ls dumps all the Items, with no Scroll limit, when given no Parms

examples:

  ls.py  # show these examples and exit
  ls.py --h  # show this help message and exit
  ls.py --  # as if:  ls -rt |tail -3

  ls  # as if:  ls.py -C
"""
# todo: often default to list just the Modified Today
# todo: default to:  ls -rt |tail -3
# todo: fallback from failed arg to looser, like add '*' to one arg
# todo: ls -C tabular defaults to \t Tabs, hurrah
# todo: ls -C tabular defaults to single column seps calc'ed on 8 column Tabs, boo
# todo: ls -A, as promoted by GShell for du -sh $(ls -A)

# todo: ls DIR1 DIR2 should mark them up for paste into Mv, such as:  dir1/.


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/ls.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
