#!/usr/bin/env python3

"""
usage: ssh.py [-h] [-t] ...

shell out to a host

options:
  -h, --help  show this help message and exit
  -t          forward control of the local terminal (-tt for more force)

examples:
  ssh -t localhost 'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
  ssh -t localhost bash -l  # '-l' for Bash to more login, not just shell out
"""

# TODO: does 'ssh -ttt' carry more force than 'ssh -tt'?


import __main__


if __name__ == "__main__":
    print(__main__.__doc__.strip())


# copied from:  git clone https://github.com/pelavarre/byobash.git
