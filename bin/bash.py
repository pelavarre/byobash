#!/usr/bin/env python3

"""
usage: bash.py [--h] [--noprofile] [--norc] ...

shell out to a host

options:
  --help       show this help message and exit
  --noprofile  launch without running shared startup files
  --norc       launch without running personal startup files

quirks:
  most Bash give no reactive meaning to env var names of 1 or 2 characters
  some Bash open a new Session, with an empty "$@", when given no Parms
  some Bash place no Scroll Limits on Sh Commands
  some Bash dump raw Control Sequences into Tty, a la 'less -R', 'less -r'
  some Bash drive apart the source for 'alias'es, vs
  Apple macOS promotes ancient Nov/2014 Bash 3.2.57 over modern Bash

advanced Bash install:

  function aliases () { echo + alias >&2 && alias; }

  function funcs () {
    local L="set |grep '^[^ =]* (' | sort"  # not Zsh 'set |grep'
    echo + $L >&2
    echo
    set |grep '^[^ =]* (' |sort
    echo
    echo ': # you might next like:  declare -f funcs'
  }

examples:

  ls ~/.bashrc ~/.bash_profile ~/.profile

  bash.py  # show these examples and exit
  bash.py --h  # show this help message and exit
  bash.py --  # todo: run as you like it
  command bin/bash.py --  # show the Advanced Bash Install of Bash Py and exit

  bash --noprofile --norc  # run with less local quirks
  export |grep SHLVL  # show how deeply incepted
  set |grep -e ^PS1= -e ^PS4=  # show the outer and incepted shell prompts
"""

# talk out how best to clear Bash History for a Bash Screen
# todo: TabTab Completion of:  mv -i *.jp
# todo: Bash already can do TabTab Completion of:  $D/
# ⌃X⌃E to edit a line


import byotools as byo


def main():
    """Run from the Sh Command Line"""

    patchdoc = r"""

  function aliases () { echo + alias >&2 && alias; }

  function funcs () {
    local L="set |grep '^[^ =]* (' | sort"  # not Zsh 'set |grep'
    echo + $L >&2
    echo
    set |grep '^[^ =]* (' |sort
    echo
    echo ': # you might next like:  declare -f funcs'
  }

    """

    byo.exit_if_patchdoc(patchdoc)  # bash.py --

    byo.exit(__name__)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/bash.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
