#!/usr/bin/env python3

"""
usage: ssh.py [--h] [-t] ...

shell out to a host

options:
  --help  show this help message and exit
  -t      forward control of the local terminal (-tt for more force)

examples:
  ssh.py  &&: call Ssh Py with no args to show these examples
  ssh -t localhost  'cd /usr/bin/ && bash -i'  # Ssh to your choice of Cd
  ssh -t localhost  "cd $PWD && bash -i"  # Ssh to same Cd but out there
  ssh -t localhost  bash -l  # '-l' for Bash to more login, not just shell out
  ssh-add -l
  ssh-add -L |grep ^ssh-rsa-cert |ssh-keygen -L -f - |grep Valid
"""
# todo: does 'ssh -ttt' carry more force than 'ssh -tt'?

# todo:  ssh.py --  &&: list recent hostnames
# todo:  ssh.py localhost  &&: retry when connection drops


import byotools as byo


if __name__ == "__main__":

    byo.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
