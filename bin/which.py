#!/usr/bin/env python3

"""
usage: which.py [-a] ...

todo

options:
  --help  show this help message and exit
  -a      show all the Search-Hit's, not just the first

examples:
  which -a  # show all the Search hits, not us
"""

# todo: list the ambiguities, like count definitions per verb

# cross-ref whence

# todo: focus on one-letter, two-letter, three-letter names
# and starts with "_" and starts with "__" when not ended with "_"

# declare -f v
# alias |grep A=
# Zsh type -f -- v


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/which.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
