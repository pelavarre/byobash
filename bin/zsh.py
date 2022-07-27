#!/usr/bin/env python3

r"""
usage: zsh.py [--h] [-f] ...

shell out to a host

options:
  --help  show this help message and exit
  -f      launch without running startup files

quirks:
  classic Zsh rudely opens a new Session, with an empty "$@", when given no Parms
  classic Zsh rudely places no Scroll Limits on Sh Commands
  todo: limit Control Sequences dumped into Tty, a la 'less', 'less -R', 'less -r'

advanced Zsh install:

  function aliases () { echo + alias >&2 && alias; }

  function funcs () {
    local L="functions |grep \$'^[^ \\\\t=]* ('"  # not Bash 'set |grep'
    echo + $L >&2
    echo
    functions |grep $'^[^ \t=]* ('
    echo
    echo ': # you might next like:  declare -f funcs'
  }

examples:

  zsh.py  # show these examples and exit
  zsh.py --h  # show this help message and exit
  zsh.py --  # todo: run as you like it
  command bin/zsh.py --  # show the Advanced Bash Install of Zsh Py and exit

  export |grep SHLVL
  zsh -f  # run with less local quirks
"""


import byotools as byo


def main():
    """Run from the Sh Command Line"""

    patchdoc = r"""

  function aliases () { echo + alias >&2 && alias; }

  function funcs () {
    local L="functions |grep \$'^[^ \\\\t=]* ('"  # not Bash 'set |grep'
    echo + $L >&2
    echo
    functions |grep $'^[^ \t=]* ('
    echo
    echo ': # you might next like:  declare -f funcs'
  }

    """

    byo.exit_if_patchdoc(patchdoc)  # zsh.py --

    byo.exit(__name__)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/zsh.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
