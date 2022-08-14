#!/usr/bin/env python3

"""
usage: hellos/select_hello.py [-h]

demo taking ⌃D TTY EOF, ⌃C KeyboardInterrupt, Return, or other Terminal Input or Paste

examples:
  hellos/select_hello.py --
"""


import __main__
import select
import signal
import sys


def main():
    """Take one typed or many pasted Lines of Terminal Input, then quit"""

    if sys.argv[1:] != ["--"]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    stderr_print()
    stderr_print("Type a line and press Return, or paste, or press ⌃D TTY EOF to quit")

    line = stdin_readline_else()
    stderr_print("got =>  ", end="")
    print(repr(line))

    while select_select(sys.stdin):
        line = stdin_readline_else()
        stderr_print("got =>  ", end="")
        print(repr(line))

    stderr_print("got pause at Stdin")


# deffed in many files  # missing from docs.python.org
def select_select(stdio):
    """Return truthy if 'stdio.read(1)' won't now hang till more Input comes"""

    rlist = [stdio]
    wlist = list()
    xlist = list()
    timeout = 0
    (r, w, x) = select.select(rlist, wlist, xlist, timeout)

    assert not w, w
    assert not x, x

    return r


# deffed in many files  # missing from docs.python.org
def stderr_print(*args, **kwargs):
    """Work like Print, but write Stderr in place of Stdout"""

    sys.stdout.flush()
    print(*args, file=sys.stderr, **kwargs)  # todo: what if "file" in kwargs.keys() ?
    sys.stderr.flush()


# deffed in many files  # missing from docs.python.org
def stdin_readline_else():
    """Block till the Chars of an Input Line arrive, else exit zero or nonzero"""

    SIGINT_RETURNCODE = 0x80 | signal.SIGINT
    assert SIGINT_RETURNCODE == 130, SIGINT_RETURNCODE

    try:
        line = sys.stdin.readline()
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        sys.stderr.write("KeyboardInterrupt\n")

        sys.exit(SIGINT_RETURNCODE)  # Exit 130 to say KeyboardInterrupt SIGINT

    if not line:  # echoed as "^D\n" at Mac, echoed as "\n" at Linux

        sys.exit(0)  # Exit 0 to say Stdin Closed

    chars = line.splitlines()[0]

    return chars


main()
