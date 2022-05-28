#!/usr/bin/env python3

"""
usage: pbcopy.py [-h]

copy Stdin into the main Os Pasteboard (aka Clipboard)

options:
  -h, --help  show this help message and exit

notes:
  switch to Apple macOS, out of Linux or G Shell, to find this built-in

examples:
  function c () { echo + pbcopy >&2; pbcopy "$@"; }
  function v () { echo + pbpaste >&2; pbcopy "$@"; }
  echo hello copy-paste world |c
  v
"""
# todo: function cv () { ... pbcopy when stdin is not tty ... }
# todo: function cv () { ... pbpaste when stdin is tty ... }
# todo: function cv () { ... tee >(pbcopy) when stdin/stdout both not tty ... }


import byotools


if __name__ == "__main__":
    byotools.main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
