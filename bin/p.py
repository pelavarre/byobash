"""
usage: cd bin/ && python3 p.py [--h]

demo how to fork ByoBash by downloading 1 File and writing 3 Lines of Code

options:
  --help  show this help message and exit

examples:

  ls -1 byotools.py p.py  # show you have come to work here with us

  python3 p.py  # show these examples and exit
  python3 p.py --h  # show this help message and exit
  python3 p.py --  # do your choice of some other work for you

  cat p.py |cat -n |expand  # show how this works
"""

import byotools as byo

byo.exit(shparms="--")

print("welcome to CLI NoteTaking with ByoBash Flair, can you dig it?")


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/p.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
