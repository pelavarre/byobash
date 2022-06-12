#!/usr/bin/env python3

"""
usage: source <(~/Public/byobash/bin/cat_bashrc_source.py)

print some first lines to speak into Bash

examples:
  cd ~/Public/
  git clone https://github.com/pelavarre/byobash.git
  cd byobash/
  bin/cat_bashrc_source.py  &&: see what it will do
  bin/cat_bashrc_source.py  &&: see it again
  source <(~/Public/byobash/bin/cat_bashrc_source.py)  &&: trust it
  export PATH="${PATH:+$PATH:}$HOME/Public/byobash/bin"  &&: do some of it yourself
  export PATH="$PATH:$HOME/Public/byobash/bin"  &&: work less hard on a non-empty Path
"""

# FIXME: deliver the 'alias cd.py' we promised
# FIXME: add ArgParse
# FIXME: add a --dupe option to still add what exists, just for test


import __main__
import os
import pdb
import sys

import byotools as byo

_ = pdb


FILE = __main__.__file__
DIRNAME = os.path.dirname(__main__.__file__)

DEMO_BROKEN_PIPE_SINK = False


def main():
    parms = sys.argv[1:]
    if parms:
        print(__main__.__doc__.strip())
    else:
        add_some_dirnames(dirnames=[DIRNAME])
        if DEMO_BROKEN_PIPE_SINK:
            for _ in range(54321):
                print(_)


def add_some_dirnames(dirnames):
    print(": begin Bash sourcelines from {}".format(byo.ShPath(FILE)))
    for dirname in dirnames:
        add_one_dirname(dirname)
    print(": end Bash sourcelines from {}".format(byo.ShPath(FILE)))


def add_one_dirname(dirname):
    """Make a ShLine to add the DirName into the Path"""
    absname = os.path.abspath(dirname)

    env_path = os.getenv("PATH")
    if env_path is None:
        shline = "export PATH={}".format(absname)
    else:
        shline = 'export PATH="$PATH:{}"'.format(absname)

    if absname in env_path.split(os.pathsep):

        return

    print(shline)


if __name__ == "__main__":
    if DEMO_BROKEN_PIPE_SINK:
        main()
    else:
        with byo.BrokenPipeSink():
            main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
