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
  works well with:  find.py
  classic Cat rudely hangs with no prompt, when given no Parms with no Stdin
  classic Cat rudely dumps raw Bytes, like 'less -r', unlike 'less -R' and 'less'
  Mac 'cat -tv' misprints the same ink for $'\xC2\xA0' NonBreakingSpace as $'\x20' Space

temporary workaround:
  alias cat.py=~/Public/pybashish/bin/cat.py

examples:

  cat.py  &&: show these examples and exit
  cat.py --h  &&: show this help message and exit
  cat.py --  &&: todo: run as you like it

  cat  &&: hangs till you provide input
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
