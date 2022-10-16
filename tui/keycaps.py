#!/usr/bin/env python3

"""
usage: keycaps.py [-h]

fire key caps bright when struck, fade to black, then grey, then gone

options:
  -h, --help  show this help message and exit

quirks:
  doesn't watch shift keys accurately, such as takes Option+Delete to mean Esc

examples:
  git clone https://github.com/pelavarre/byobash.git
  tui/keycaps.py
"""

# code reviewed by people, and by Black and Flake8


import __main__
import argparse
import datetime as dt
import difflib
import os
import pdb
import sys
import termios
import textwrap
import tty

_ = pdb


#
# Run from the Sh command line
#


def main():
    """Run from the Sh command line"""

    parse_keycaps_args()  # exits if no args, etc

    crlf = "\r\n"
    print("Press ^D EOF to quit")
    with stdtty_open(sys.stderr) as chatting:
        while True:
            (millis, stroke) = chatting.read_millis_stroke()
            print(int(millis), repr(stroke), end=crlf)

            break


#
# Layer over Import ArgParse
#


def parse_keycaps_args():
    """Take in Words from the Sh Command Line"""

    # Drop the '--' Separator if present, even while declaring no Pos Args

    sys_parms = sys.argv[1:]
    if sys_parms == ["--"]:
        sys_parms = list()

    # Parse the Sh Command Line, or show Help

    parser = compile_keycaps_argdoc()
    args = parser.parse_args(sys_parms)  # exits if "-h", "--h", "--he", ... "--help"
    if not sys.argv[1:]:
        doc = __main__.__doc__

        exit_via_testdoc(doc, epi="examples")  # exits because no args

    # Succeed

    return args


def compile_keycaps_argdoc():
    """Construct the ArgumentParser"""

    doc = __main__.__doc__
    parser = compile_argdoc(doc, epi="quirks")

    try:

        exit_unless_doc_eq(doc, parser)

    except SystemExit:
        stderr_print("keycaps.py: ERROR: main doc and argparse parser disagree")

        raise

    return parser


def compile_argdoc(doc, epi):
    """Construct an ArgumentParser, without defining Positional Args and Options"""

    doc_lines = doc.strip().splitlines()
    prog = doc_lines[0].split()[1]  # second word of first line

    doc_firstlines = list(_ for _ in doc_lines if _ and (_ == _.lstrip()))
    description = doc_firstlines[1]  # first line of second paragraph

    epilog_at = doc.index(epi)
    epilog = doc[epilog_at:]

    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog,
    )

    return parser


def exit_unless_doc_eq(doc, parser):
    """Exit nonzero, unless Doc equals Parser Format_Help"""

    # Fetch the Parser Doc from a fitting virtual Terminal
    # Fetch from a Black Terminal of 89 columns, not current Terminal width
    # Fetch from later Python of "options:", not earlier Python of "optional arguments:"

    with_columns = os.getenv("COLUMNS")
    os.environ["COLUMNS"] = str(89)
    try:

        parser_doc = parser.format_help()

    finally:
        if with_columns is None:
            os.environ.pop("COLUMNS")
        else:
            os.environ["COLUMNS"] = with_columns

    parser_doc = parser_doc.replace("optional arguments:", "options:")

    # Fetch the Main Doc

    file_filename = os.path.split(__file__)[-1]

    main_doc_strip = doc.strip()

    got = main_doc_strip
    got_filename = "{} --help".format(file_filename)
    want = parser_doc
    want_filename = "argparse.ArgumentParser(..."

    # Print the Diff to Parser Doc from Main Doc and exit, if Diff exists

    diff_lines = list(
        difflib.unified_diff(
            a=got.splitlines(),
            b=want.splitlines(),
            fromfile=got_filename,
            tofile=want_filename,
        )
    )

    if diff_lines:
        stderr_print("\n".join(diff_lines))

        sys.exit(1)  # trust caller to log SystemExit exceptions well


def exit_via_testdoc(doc, epi):
    """Print the last Paragraph of the Main Arg Doc"""

    testdoc = doc
    testdoc = testdoc[testdoc.index(epi) :]
    testdoc = "\n".join(testdoc.splitlines()[1:])
    testdoc = textwrap.dedent(testdoc)
    testdoc = testdoc.strip()

    print()
    print(testdoc)
    print()

    sys.exit(0)


def stderr_print(*args, **kwargs):  # todo: what if "file" in kwargs.keys() ?
    """Work like Print, but write Stderr in place of Stdout"""

    sys.stdout.flush()
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()


#
# Layer over Import Termios, Tty
#


class stdtty_open:  # Linux & Mac only?
    r"""
    Emulate a glass teletype at Stdio, such as the 1978 DEC VT100 Video Terminal

    Apply Terminal Input Magic to read ⌃@ ⌃C ⌃D ⌃J ⌃M ⌃Q ⌃S ⌃T ⌃Z ⌃\ etc as themselves,
    not as NUL SIGINT EOF LF CR SIGCONT SIGSTOP SIGINFO SIGTSTP SIGQUIT etc

    Compare Bash 'stty -a' and 'bind -p', Zsh 'bindkey', Unicode.Org U0000.pdf
    """

    # stty -a |tr -d ' \t' |tr ';' '\n' |grep '=^' |sort

    def __init__(self, stdtty):
        """Work at Sys Stderr, or elsewhere"""

        fd = stdtty.fileno()

        self.fd = fd
        self.getattr_ = None
        self.stdtty = stdtty

    def __enter__(self):
        """Flush, then start taking keystrokes literally & writing Lf as itself"""

        fd = self.fd
        getattr_ = self.getattr_
        stdtty = self.stdtty

        stdtty.flush()

        if stdtty.isatty() and (getattr_ is None):
            getattr_ = termios.tcgetattr(fd)
            assert getattr_ is not None

            self.getattr_ = getattr_

            tty.setraw(fd, when=termios.TCSADRAIN)  # not TCSAFLUSH

        chatting = self

        return chatting

    def __exit__(self, *exc_info):
        """Flush, then stop taking keystrokes literally & start writing Lf as Cr Lf"""

        _ = exc_info

        fd = self.fd
        getattr_ = self.getattr_
        stdtty = self.stdtty

        stdtty.flush()

        if getattr_ is not None:
            self.getattr_ = None  # mutate

            when = termios.TCSADRAIN
            termios.tcsetattr(fd, when, getattr_)

    def read_millis_stroke(self):
        """Read one keystroke, but also measure how long it took to arrive"""

        fd = self.fd

        t0 = dt.datetime.now()
        stroke = os.read(fd, 1)

        t1 = dt.datetime.now()
        millis = (t1 - t0).total_seconds() * 1000

        return (millis, stroke)


#
# Run from the Sh command line, when not imported
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/tui/keycaps.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
