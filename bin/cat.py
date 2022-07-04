#!/usr/bin/env python3

r"""
usage: cat.py [--h] [-E] [-e] [-n] [-T] [-t] [-v] [FILE ...]

copy each line of input bytes (or chars) to output (as if "cat"enating them slowly)

positional arguments:
  FILE                  a file to copy out (such as '-' to mean Stdin)

options:
  --help                show this help message and exit
  -E, --show-ends       print each \n lf as $ lf
  -e                    call for -E and -v
  -n, --number          number each line of output, up from 1, with \t tabs
  -T, --show-tabs       show each \t tab as \ t Backslant-Tee
  -t                    call for -T and -v
  -v, --show-nonprinting
                        forward the input formatted as a Python String or Bytes Literal

quirks:
  classic Cat forces you to guess when to prompt for input
  Mac 'cat -tv' does Not distinguish $'\xC2\xA0' NonBreakingSpace from $'\x20' Space
  few Linux bother to define 'pbpaste' and 'pbcopy'

temporary workaround:
  alias cat.py=~/Public/pybashish/bin/cat.py

examples:

  cat  &&: hangs till you provide input
  cat.py  &&: show these examples and exit

  cat -  &&: hangs till you provide input
  cat.py -  &&: prompts for input

  echo $'some Spaces "\x20\xC2\xA0" more equal than others' |cat -tv  &&: fails at Mac

  echo $'some Spaces "\x20\xC2\xA0" more equal than others' |pbcopy
  pbpaste |cat -tv  &&: fails for macOS Paste, wrongly showing Nbsp as Sp

  echo $'some Spaces "\x20\xC2\xA0" more equal than others' |cat.py -tv  &&: works
  echo $'\xC0\x80' |cat.py -tv  &&: still works, despite UnicodeDecodeError

  seq 100 105|cat -n |expand  &&: demo Cat N numbering things
  seq 100 105|cat -n |cat.py -tv  &&: show Tabs as \t, but don't show Line-Break's
  paste <(seq 4 9) <(seq 100 105) |cat -tv  &&: show counting up from 4, not from 1

  echo "   " |cat -etv  &&: show the Spaces before each Line-Break

  cat /proc/cpuinfo |grep processor |wc -l  &&: count Cpu Cores at Linux
"""
# todo: stop needing the Temporary Workaround


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/cat.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
