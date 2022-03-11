#!/usr/bin/env python3

"""
usage: ssh.py [-h] [-t] ...

shell out to a host

options:
  -h, --help  show this help message and exit
  -t          forward control of the local terminal (-tt for more force)

examples:
  ssh -t localhost  'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
  ssh -t localhost  "cd $PWD && bash -i"  # Ssh to same Cd but out there
  ssh -t localhost  bash -l  # '-l' for Bash to more login, not just shell out
"""

# TODO: does 'ssh -ttt' carry more force than 'ssh -tt'?

# FIXME: add ArgParse


import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    SUGGESTION = textwrap.dedent(
        """
        ssh -t localhost  'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
        ssh -t localhost  "cd $PWD && bash -i"  # Ssh to same Cd but out there
        ssh -t localhost  bash -l  # '-l' for Bash to more login, not just shell out
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
