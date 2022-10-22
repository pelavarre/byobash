#!/usr/bin/env python3

r"""
usage: echo.py [--h] [-e|-E] [-n] [WORD ...]

print some words

options:
  --help  show this help message and exit
  -n      print without closing the line
  -E      don't escape the \ backslant
  -e      do escape the \ backslant with any of \ abfnrtv 0 x, and also with \e and \c

quirks:
  goes well with:  clear.py, reset.py, tput.py
  classic Echo just prints an Empty Line, as if asked to print '', when given no Parms
  \e is \x1B Esc
  \c cancels the rest: it stops the print and implies -n

advanced Bash install:

  function echo.py {
    local xc=$?
    : : 'Print and clear the Process Exit Status ReturnCode, else print the Parms' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command echo.py "+ exit $xc"
    else
      command echo.py "$@"
    fi
  }

examples:

  echo.py  # show these examples and exit
  echo.py --h  # show this help message and exit
  echo.py --  # echo "+ exit $?"  # mention the last Exit Status ReturnCode once
  command bin/echo.py --  # show the Advanced Bash Install of Echo Py and exit

  echo.py -- ssh.py --pb 'cd /usr/bin' --pb "export PS1='\\$ '"  # echo five Args

  echo.py hello; echo.py --  # test Exit Code 0
  rm /dev/null/part; echo.py --  # test Exit Code 1
  bash -c 'exit 3'; echo.py --  # test Exit Code 3

  echo -ne '\e[H\e[2J\e[3J'  # clear Terminal history like Mac Terminal ⌘K

  echo -ne '\e[8;50;89t'  # change to 50 Rows x 89 Columns
  echo -ne '\e[8;'$(stty size |cut -d' ' -f1)';89t'  # change to 89 Columns
  echo -ne '\e[8;'$(stty size |cut -d' ' -f1)';101t'  # change to 101 Columns
"""

# todo:  the echo.py -- could be the 50;89

# todo:  echo.py --pb "$1" "$2" ...  # fills Os Copy/Paste Buffer with 1 Line per Arg

# todo:  do these work better when spelled differently, as:  echo -n $'...'

# print("\N{Greek Small Letter Pi}".encode())  # b'\xcf\x80'
# print("\N{No-Break Space}".encode())  # b'\xc2\xa0'


import sys

import byotools as byo


def main():
    """Run from the Sh Command Line"""

    patchdoc = """

  function echo.py {
    local xc=$?
    : : 'Print and clear the Process Exit Status ReturnCode, else print the Parms' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command echo.py "+ exit $xc"
    else
      command echo.py "$@"
    fi
  }

    """

    byo.exit_if_patchdoc(patchdoc)

    if sys.argv[1:2] == ["--"]:
        for (i, arg) in enumerate(sys.argv):
            if i:
                if (i > 1) or (arg != "--"):
                    print(
                        "argv {} is {} chars of:  {}".format(i, len(arg), arg).rstrip()
                    )

        sys.exit(0)

    byo.exit()


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/echo.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
