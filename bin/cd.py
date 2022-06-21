#!/usr/bin/env python3

r"""
usage: cd.py [--h] [DIR]

change working Dir

positional arguments:
  DIR     the directory to work in next (default: $HOME)

options:
  --help  show this help message and exit

quirks:
  spaces in Args come through Zsh just fine, but separate Args in Bash

examples:
  function cd.py () { set -x; cd "$(~/Public/byobash/bin/cd.py $@)"; set +x; }
  cd.py  &&: show these examples and exit
  cd.py --h  &&: show this help message and exit
  cd.py --  &&: go to Desktop Dir inside Home Dir, like:  cd ~/Desktop
  cd.py ~  &&: go to Home Dir, same as:  cd ~
  cd.py .  &&: stay put, same as:  cd .
  cd.py ..  &&: go one Dir up, same as:  cd ..
"""
# todo: adopt 'cd.py -- OLD NEW' from Zsh, for editing $PWD


import sys

import byotools as byo


if __name__ == "__main__":
    sys.stdout = sys.stderr  # todo: stop never printing to Stdout

    byo.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
