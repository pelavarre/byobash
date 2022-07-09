#!/usr/bin/env python3

#
# stty -a
# stty -ixon
# stty ixon
#
# stty cols 89  # and you can lie
# stty rows 50  # and you can lie
#
# echo -n $'\e[8;'$(stty size |cut -d' ' -f1)';101t'  # 'one-hundred one (101) cols'
# echo -n $'\e[8;'$(stty size |cut -d' ' -f1)';89t'  # 'eighty-nine (89) cols'
#
# echo -n $'\e[8;50;89t'  # revert Terminal to a familiar Window Size
#

"""
usage: todo

todo

options:
  --help       show this help message and exit

quirks:
  classic STty dumps the Switches, with no Scroll limit, when given no Parms

examples:
  stty.py  # show these examples and exit
  stty.py --h  # show this help message and exit
  stty.py --  # todo: run as you like it
"""


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/stty.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
