#!/usr/bin/env python3

r"""
usage: byopyvm.py [--help] [WORD ...]

work quickly and concisely, over Dirs of Dirs of Files

positional arguments:
  WORD   the name of the next Func to run, a la the Forth Programming Language

options:
  --help               show this help message and exit

advanced bash install

  function = {
    : : 'Show Stack, else else do other Stack Work' : :
    if [ "$#" = 0 ]; then
        ~/Public/byobash/bin/byopyvm.py ls
    else
        ~/Public/byobash/bin/byopyvm.py "$@"
    fi
  }

examples:

  byopyvm.py  # show these examples and exit
  byopyvm.py --h  # show this help message and exit
  byopyvm.py --  # ls -1rtc |tail -4

  # Stack Work

  byopyvm.py ls  # ls -1rtc |tail -4
  byopyvm.py cp  # cp -ip ... ...~$(date +%m%dpl%H%M%S)
  byopyvm.py cp  # cp -ipR .../ ...~$(date +%m%dpl%H%M%S)
  byopyvm.py mv  # mv -i ... ...~$(date +%m%dpl%H%M%S)

  # Maths

  byopyvm.py math.pi  # echo 3.141592653589793 >3.142~
  byopyvm.py 2 *  # echo 2 >2~ && rm -f 3.142~ 2~ && echo 6.283185307179586 >6.283~
  byopyvm.py .  # cat 6.283~ && rm -f 6.283~
"""


import sys

import byotools as byo

import shpipe as shpipes  # FIXME: git mv shpipe.py shpipes.py


def main():
    """Run from the Sh Command Line"""

    parms = sys.argv[1:]
    main.parms = parms

    main.sponge_shverb = None  # FIXME
    func_by_verb = form_func_by_verb()

    patchdoc = """

      function = {
        : : 'Show Stack, else else do other Stack Work' : :
        if [ "$#" = 0 ]; then
            ~/Public/byobash/bin/byopyvm.py ls
        else
            ~/Public/byobash/bin/byopyvm.py "$@"
        fi
      }

    """

    byo.exit_via_patchdoc(patchdoc)  # command byopyvm.py --
    byo.exit_via_testdoc()  # byopyvm.py
    byo.exit_via_argdoc()  # byopyvm.py --help

    shverb = parms[0]
    # parms[::] = parms[1:]

    func = None
    kwargs = dict()

    if shverb in func_by_verb:
        func = func_by_verb[shverb]

    func(**kwargs)


#
# Wrap many many Shim's around Sh Commands
#


def form_func_by_verb():
    """Declare the Pipe Filter Abbreviations"""

    func_by_verb = dict(ls=do_ls)

    return func_by_verb


def do_ls():
    """ls -1rtc |tail -4"""

    shpipe = "ls -1rtc |tail -4"
    shpipes.exit_via_shpipe(shpipe)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byopyvm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
