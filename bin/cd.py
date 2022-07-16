#!/usr/bin/env python3

r"""
usage: cd.py [--h] [--pwd] [DIR]

change the Working Dir in Sh Memory

positional arguments:
  DIR          the directory to work in next (default '~/Desktop')

options:
  --help       show this help message and exit
  --for-chdir  print to Stdout what the in-memory Sh Cd needs to hear

quirks:
  goes well with:  hostname.py, pwd.py
  classic Cd rudely jumps back into the legacy '~/' Home Dir, when given no Parms
  classic Cd rudely loses all Parms past the first
  Zsh and Bash take '(dirs -p |head -1)', but only Bash takes 'dirs +0'

advanced bash install:

  function - () { echo + cd - && cd - >/dev/null && (dirs -p |head -1); }
  # Bash will say 'bash: cd: OLDPWD not set' and fail, till after Cd

  function .. () { echo + cd .. && cd .. && (dirs -p |head -1); }

  function cd.py () {
    : : 'Print some kind of Help, else change the Sh Working Dir' : :
    if [ "$#" = 0 ]; then
      command cd.py
    elif [ "$#" = 1 ] && [ "$1" = "-" ]; then
      'cd' -
    elif [ "$#" = 1 ] && [[ "$1" =~ ^--h ]] && [[ "--help" =~ ^"$1" ]]; then
      command cd.py --help
    else
      'cd' "$(command cd.py --for-chdir $@)" && (dirs -p |head -1)
    fi
  }

examples:

  cd.py  # show these examples and exit
  cd.py --h  # show this help message and exit
  cd.py --  # go to Desktop Dir inside Home Dir, same as:  cd ~/Desktop
  command bin/cd.py --  # show the Advanced Bash Install of Cd Py and exit

  cd.py -  # toggle back to previous Sh Working Dir, same as:  cd -
  cd.py ~  # go to Home Dir, same as:  cd ~
  cd.py .  # stay put, same as:  cd .
  cd.py ..  # go one Dir up, same as:  cd ..
"""
# todo: adopt 'cd.py -- OLD NEW' from Zsh, for editing $PWD


import os
import sys

import byotools as byo


def main():
    """Run from the Sh Command Line"""

    parms = sys.argv[1:]

    patchdoc = """

  function - () { echo + cd - && cd - >/dev/null && (dirs -p |head -1); }
  # Bash will say 'bash: cd: OLDPWD not set' and fail, till after Cd

  function .. () { echo + cd .. && cd .. && (dirs -p |head -1); }

  function cd.py () {
    : : 'Print some kind of Help, else change the Sh Working Dir' : :
    if [ "$#" = 0 ]; then
      command cd.py
    elif [ "$#" = 1 ] && [ "$1" = "-" ]; then
      'cd' -
    elif [ "$#" = 1 ] && [[ "$1" =~ ^--h ]] && [[ "--help" =~ ^"$1" ]]; then
      command cd.py --help
    else
      'cd' "$(command cd.py --for-chdir $@)" && (dirs -p |head -1)
    fi
  }

    """

    # Define some forms of 'cd.py'

    byo.exit_if_patchdoc(patchdoc)  # command cd.py --
    byo.exit_if_testdoc()  # cd.py
    byo.exit_if_argdoc()  # cd.py --help

    # Pick out the '--for-chdir' option in full, or abbreviated

    for_chdir = None
    if parms:
        if parms[0].startswith("--f"):
            if "--for-chdir".startswith(parms[0]):
                for_chdir = True

    # Define 'command cd.py --for-chdir --'

    if for_chdir and (parms[1:] == ["--"]):
        print(os.path.expanduser("~/Desktop"))

        sys.exit(0)  # Exit 0 to call for Sh Os ChDir to expanded '~/Desktop'

    # Define 'command cd.py --for-chdir DIR'

    if for_chdir and not parms[2:]:
        print(parms[1])

        sys.exit(0)  # Exit 0 to call for Sh Os ChDir to 1th Parm

    # Reject other usage

    sys.stderr.write("usage: cd.py [--h] [--for-chdir] [DIR]\n")

    sys.exit(2)  # Exit 2 for rare usage


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/cd.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
