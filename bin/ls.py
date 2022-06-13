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

examples:
  ls.py  &&: call Ls Py with no args to show these examples
  ls.py --  &&: as if:  ls -rt |tail -3
  ls  &&: as if:  ls.py -C
"""
# todo: default to:  ls -rt |tail -3
# todo: fallback from failed arg to looser, like add '*' to one arg
# todo: ls -C tabular defaults to \t Tabs, hurrah
# todo: ls -C tabular defaults to single column seps calc'ed on 8 column Tabs, boo
# todo: ls -A, as promoted by GShell for du -sh $(ls -A)


import byotools


if __name__ == "__main__":

    byotools.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
