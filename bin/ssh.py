#!/usr/bin/env python3

r"""
usage: ssh.py [--h] [-t] [-f CONFIG] ...

shell out to a host

options:
  --help     show this help message and exit
  -t         forward control of the local terminal (-tt for more force)
  -F CONFIG  choose a file of options (default '~/.ssh/config')

quirks:
  goes well with:  ssh-add.py
  classic Ssh rudely exits via a Code 255 Usage Error, when given no Parms

examples:

  ls -d -alF ~/.ssh/ && ls -alF ~/.ssh/config

  ssh.py  # show these examples and exit
  ssh.py --h  # show this help message and exit
  ssh.py --  # todo: run as you like it

  ssh.py localhost --pb 'cd /usr/bin' --pb "export PS1='\$ '"  # choose remote PWD & PS1

  ssh.py  # call Ssh Py with no args to show these examples
  ssh -F /dev/null localhost  # go there without a custom Config File
  ssh -t localhost  'cd /usr/bin/ && bash -i'  # Ssh out to your choice of Cd
  ssh -t localhost  "cd $PWD && bash -i"  # Ssh out to remote Cd same as local
  ssh -t localhost  bash -l  # start up Bash more like Login, don't just Interact
  ssh-add -l  # list the loaded Ssh Keys
  echo "SSH_AUTH_SOCK=$SSH_AUTH_SOCK"  # show an Env Var Linux needs for Ssh Keys
  echo "SSH_AGENT_PID=$SSH_AGENT_PID"  # show another Env Var Linux needs for Ssh Keys
  ssh-add -L |grep ^ssh-rsa-cert |ssh-keygen -L -f - |grep Valid  # show expiry
"""
# loop to retry, only while exit codes nonzero

# ssh-keygen -R localhost  # to cut it out of '~/.ssh/known_hosts'
# todo: smashing SSH_AUTH_SOCK/ SSH_AGENT_PID empties 'ssh-add -l' at Linux
# todo: does 'ssh -ttt' carry more force than 'ssh -tt'?
# todo:  ssh.py --  # list recent hostnames
# todo:  ssh.py localhost  # retry when connection drops
# todo:  bin/gcloud auth login
# todo:  bin/gcloud cloud-shell ssh

# WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
# IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!

# ssh -F /dev/null $CLUSTER
#
# ssh -o UserKnownHostsFile=/dev/null $CLUSTER
# ssh -o StrictHostKeyChecking=no $CLUSTER
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $CLUSTER
#
# bash -c "echo SQUIRREL; hostname; python3 -c 'import socket; print(socket.getfqdn())'"
#
# The authenticity of host 'cluster... (...)' can't be established.
# ECDSA key fingerprint is SHA256:...
# Are you sure you want to continue connecting (yes/no/[fingerprint])?
#
# ssh-keygen -R $CLUSTER


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/ssh.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
