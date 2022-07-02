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

bash install:

  function cd.py () {
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      'cd' ~/Desktop && (dirs -p |head -1)
    else
      'cd' "$(~/Public/byobash/bin/cd.py $@)" && (dirs -p |head -1)
    fi
  }

examples:

  cd.py  &&: show these examples and exit
  cd.py --h  &&: show this help message and exit

  cd.py --  &&: go to Desktop Dir inside Home Dir, same as:  cd ~/Desktop

  cd.py ~  &&: go to Home Dir, same as:  cd ~
  cd.py .  &&: stay put, same as:  cd .
  cd.py ..  &&: go one Dir up, same as:  cd ..
"""
# todo: adopt 'cd.py -- OLD NEW' from Zsh, for editing $PWD


import os
import sys

import byotools as byo


if __name__ == "__main__":

    try:
        sys.stdout = sys.stderr  # todo: stop never printing to Stdout
        byo.exit_via_testdoc()
        byo.exit_via_argdoc()
    except SystemExit:
        sys.__stdout__.write(".\n")

        raise

    parms = sys.argv[1:]
    if parms == ["--"]:
        print(
            """
  function cd.py () {
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      'cd' ~/Desktop && (dirs -p |head -1)
    else
      'cd' "$(~/Public/byobash/bin/cd.py $@)" && (dirs -p |head -1)
    fi
  }
"""
        )
    elif parms == ["-"]:
        default_None = None
        env_oldpwd = os.environ.get("OLDPWD", default_None)
        if env_oldpwd is not None:
            sys.__stdout__.write("{}\n".format(env_oldpwd))
        else:
            sys.__stdout__.write("{}\n".format(sys.argv[1]))
    else:
        sys.__stdout__.write("{}\n".format(sys.argv[1]))


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/cd.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
