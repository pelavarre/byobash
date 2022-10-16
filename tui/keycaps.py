#!/usr/bin/env python3

"""
usage: keycaps.py [-h]

fire key caps bright when struck, fade to black, then grey, then gone

options:
  -h, --help  show this help message and exit

quirks:
  reacts complexly to
  + Control, Fn, ⌥ Option Alt, & ⌘ Command keys for shifting keys
  + Option Grave and Option E I N U keys for prefixing other keys
  + Terminal > Preferences > Profiles > Keyboard > Use Option As Meta

examples:
  git clone https://github.com/pelavarre/byobash.git
  tui/keycaps.py  # show these examples
  tui/keycaps.py --
"""

# code reviewed by people, and by Black and Flake8


import __main__
import argparse
import datetime as dt
import difflib
import os
import pdb
import select
import sys
import termios
import textwrap
import tty
import unicodedata

_ = pdb


DEFAULT_NONE = None


#
# Run from the Sh command line
#


def main():
    """Run from the Sh command line"""

    parse_keycaps_args()  # exits if no args, etc

    eot = unicodedata_lookup("EOT")
    crlf = "\r\n"

    print("Press ^D EOT twice to quit")
    with stdtty_open(sys.stderr) as chatting:
        ch = None
        while True:
            ch_minus = ch

            (millis, stroke) = chatting.read_millis_stroke()
            str_int_millis = "{:6}".format(int(millis))

            if not isinstance(stroke, str):

                print(str_int_millis, repr(stroke), end=crlf)

            elif isinstance(stroke, str):

                ch = unicodedata_lookup(stroke)
                rep_0 = bytes_hex_repr(ch.encode())
                rep_1 = ch_encode_repr(ch)

                print(str_int_millis, rep_0, repr(stroke), rep_1, end=crlf)

                if ch_minus == ch == eot:

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
# Layer over Class Bytes and Class Str
#


def bytes_hex_repr(xxs):
    r"""Repr of the Bytes, but as only uppercase Hex, no \t \n \r nor printable Ascii"""

    hexxes = xxs.hex().upper()
    escapes = "".join(
        r"\x{}{}".format(a, b) for (a, b) in zip(hexxes[::2], hexxes[1::2])
    )
    rep = r"b'{}'".format(escapes)

    return rep  # such as b'\x09\x0A\x0D\x20' for b'\t\n\r '


def ch_encode_repr(ch):
    r"""Repr of the Encode of Ch, but b'\a', b'\b', and b'\f ' instead,for those"""

    assert len(ch) == 1, repr(ch)

    xxs = ch.encode()
    index = b"\a\b\f\t\r\n".find(xxs)

    rep = repr(xxs)
    if index >= 0:
        rep = r"b'\{}'".format("abftrn"[index])
    else:
        rep = repr(xxs)
        rep = rep[0] + rep[1:].upper()
        rep = rep.replace(r"\X", r"\x")

    return rep  # such as b'\a\b\f\n\t\r ' for itself  # such as b'\x1B' for Esc


#
# Layer over Import Termios and Import Tty
#


OPTION_E = "\N{Acute Accent}".encode()
OPTION_GRAVE = "\N{Grave Accent}".encode()
OPTION_I = "\N{Modifier Letter Circumflex Accent}".encode()
OPTION_N = "\N{Small Tilde}".encode()
OPTION_U = "\N{Diaeresis}".encode()

OPTION_PREFIXES = (OPTION_E, OPTION_GRAVE, OPTION_I, OPTION_N, OPTION_U)


class stdtty_open:  # Linux & Mac only?
    r"""
    Emulate a glass teletype at Stdio, such as the 1978 DEC VT100 Video Terminal

    Apply Terminal Input Magic to read ⌃@ ⌃C ⌃D ⌃J ⌃M ⌃Q ⌃S ⌃T ⌃Z ⌃\ etc as themselves,
    not as NUL SIGINT EOF LF CR SIGCONT SIGSTOP SIGINFO SIGTSTP SIGQUIT etc

    Compare Bash 'stty -a' and 'bind -p', Zsh 'bindkey', Unicode.Org Pdf U+0000
    """

    # stty -a |tr -d ' \t' |tr ';' '\n' |grep '=^' |sort

    def __init__(self, stdtty):
        """Work at Sys Stderr, or elsewhere"""

        fd = stdtty.fileno()

        self.fd = fd
        self.getattr_ = None
        self.stdtty = stdtty

    def __enter__(self):
        """Flush, then start taking Keystrokes literally & writing Lf as itself"""

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
        """Flush, then stop taking Keystrokes literally & start writing Lf as Cr Lf"""

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
        """Read one Keystroke, but also measure how long it took to arrive"""

        t0 = dt.datetime.now()
        stroke = self.read_stroke()
        t1 = dt.datetime.now()

        millis = (t1 - t0).total_seconds() * 1000

        return (millis, stroke)

    def read_stroke(self):
        """Read one Keystroke"""

        fd = self.fd

        xxs = os.read(fd, 1)
        while self.select_select_rlist(timeout=0):
            xxs += os.read(fd, 1)

        if xxs in OPTION_PREFIXES:
            if self.select_select_rlist(timeout=0.001):
                while self.select_select_rlist(timeout=0):
                    xxs += os.read(fd, 1)

        try:
            chars = xxs.decode()
        except UnicodeDecodeError:
            chars = None

            print("UnicodeDecodeError: {}".format(xxs))

            raise

        stroke = xxs
        if chars and (len(chars) == 1):  # if is not Paste
            ch = chars[-1]
            name = unicodedata_name(ch)
            stroke = name

        return stroke

        # b'\x1B[Z' for ⇧ Tab  # same bytes as CSI Z, aka Emacs BackTab
        # b'b'\x1b[1;2C' for ⇧ ←  # same bytes as Left(m=1, n=2), so doubled in row
        # b'b'\x1b[1;2D' ⇧ →  # same bytes as Right(m=1, n=2), so doubled in row
        # b'\x1B[Z' aka CSI Z for ⇧ Tab

        # b'\x1Bb' aka ⌥ B for ⌥ ←  # same bytes as Meta B, aka Emacs Backward-Word
        # b'\x1Bf' aka ⌥ F for ⌥ →  # same bytes as Meta F, aka Emacs Forward-Word

        # doubles of Option E I N U Grave send themselves and still mark a vowel
        # Option E I N U before consonants send the marks themselves
        # Option Grave before consonants drops itself

    def select_select_rlist(self, timeout):
        """Wait till next Byte of Keystroke, next burst of Paste pasted, or Timeout"""

        rlist = [self.stdtty]
        wlist = list()
        xlist = list()

        selected = select.select(rlist, wlist, xlist, timeout)

        (rlist2, _, _) = selected
        if rlist2 != rlist:
            assert rlist2 == [], rlist2

        return rlist2


#
# Layer over Import UnicodeData
#


# List the short Uppercase names from Unicode Org U000 Pdf to C0 Control Chars

C0_NAMES_MINUS = """
    NUL SOH STX ETX EOT ENQ ACK BEL BS HT LF VT FF CR SO SI
    DLE DC1 DC2 DC3 DC4 NAK SYN ETB CAN EM SUB ESC FS GS RS US
""".split()  # "\x00".."\x1F" apart from "\x7F" DEL

# b"\x00" NUL at ⌃ Space and ⌃ ⇧ Space
# b"\x00" NUL at ⌃ ⇧ 2 and not at ⌃ 2
# b"\x09" HT at ⌃ I and Tab and not at ⌃ ⇧ I
# b"\x0D" CR at ⌃ J and Return and not at ⌃ ⇧ J
# b"\x19" EOM at ⌃ Y in Python, despite "EM" in Unicode Org U000 Pdf
# b"\x1B" ESC at ⌃ [ and ⌃ ⇧ [ and Esc
# b"\x1E" RS at ⌃ ⇧ 6 and not at ⌃ 6
# b"\x1F" US at ⌃ ⇧ - and at ⌃ -

# b"\x7F" DEL at Delete and not at ⌃ ?


# List the short Uppercase names from Unicode Org U000 Pdf to C1 Control Chars

C1_NAMES_PLUS = """
    . . BPH NBH IND NEL SSA ESA HTS HTJ VTS PLD PLU RI SS2 SS3
    DCS PU1 PU2 STS CCH MW SPA EPA SOS . SCI CSI ST OSC PM APC
""".split()  # "\x80..\x9F" except not "\x80\x81\x99"

# "\x9B" is 1 Char CSI encoded by UTF-8 as b"\xC2\x9B"
# "\x1B\x5B" is 2 Char CSI encoded by UTF-8 as b"\x1B\x5B" == b"\x1B["

# "\xA0" aka "\N{NBSP}" is the first Char just past the C1 Chars, at ⌥ Space


# Index C0 & C1 Control Chars by their short Uppercase names from Unicode Org U000 Pdf

CC_NAME_BY_CH = dict()

CC_NAME_BY_CH.update({chr(i): k for (i, k) in enumerate(C0_NAMES_MINUS)})
CC_NAME_BY_CH[chr(0x7F)] = "DEL"

CC_NAME_BY_CH.update(
    {chr(0x80 + i): k for (i, k) in enumerate(C1_NAMES_PLUS) if k != "."}
)

# Index C0 & C1 short Uppercase names by Control Chars from Unicode Org U000 Pdf

CC_CH_BY_NAME = {v: k for (k, v) in CC_NAME_BY_CH.items()}

assert len(CC_NAME_BY_CH) == len(CC_CH_BY_NAME)


# Show "\x19" also has "EOM" short name in Python, vs only "EM" short name in Unicode

EM = unicodedata.lookup("EOM")
assert "\x19" == EM, (b"\x19", EM)


def unicodedata_lookup(name):
    r"""Char of a \N{name}"""

    try:
        ch = unicodedata.lookup(name)
    except KeyError:
        if name == "EM":  # recover from mystic irregular KeyError at "EM"
            ch = CC_CH_BY_NAME[name]
        else:

            raise

    return ch


def unicodedata_name(ch):
    r"""One of the \N{name}s of a Char"""

    if ch == "\u00A0":

        return "NBSP"  # vs "No-Break Space"

    try:
        name = unicodedata.name(ch).title()
    except ValueError:  # recover from ValueError's across C0 & C1 of Category 'Cc'
        name = CC_NAME_BY_CH.get(ch, DEFAULT_NONE)
        if name is None:

            raise

    return name


#
# Run from the Sh command line, when not imported
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/tui/keycaps.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
