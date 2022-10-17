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
import string
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

    eot_stroke = unicodedata_lookup("EOT").encode()
    crlf = "\r\n"

    print("Press ^D EOT twice to quit")
    with stdtty_open(sys.stderr) as chatting:
        stroke = None
        while True:
            stroke_minus = stroke

            (millis, stroke) = chatting.read_millis_stroke()
            str_int_millis = "{:6}".format(int(millis))

            keycaps = KEYCAPS_BY_STROKE.get(stroke, DEFAULT_NONE)

            print(str_int_millis, bytes_hex_repr(stroke), keycaps, end=crlf)

            if stroke_minus == stroke == eot_stroke:

                break


#
# Draw the Keyboard of a MacBook Pro (Retina, 15-inch, Mid 2015)
#


assert string.ascii_uppercase == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
assert string.ascii_lowercase == "abcdefghijklmnopqrstuvwxyz"

KEYCAPS_BY_INDEX = [
    "Esc F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12".split(),
    "` 1 2 3 4 5 6 7 8 9 0 - = Del".split(),
    "Tab Q W E R T Y U I O P [ ] \\".split(),
    "A S D F G H J K L ; '".split(),
    "⇧ Z X C V B N M , . / ⇧".split(),
    "Fn ⌃ ⌥ ⌘ Space ⌘ ⌥ ← ↑ ↓ →".split(),
]

KEYCAPS = list(keycap for row in KEYCAPS_BY_INDEX for keycap in row)

KEYCAPS_BY_STROKE = dict()

for CH_ in string.ascii_uppercase:  # Control + Letter
    KEYCAPS_BY_STROKE[chr(ord(CH_) ^ 0x40).encode()] = "^{}".format(CH_)

_KEYCAPS_0 = "`1234567890-=" "[]\\" ";'" ",./"
_KEYCAPS_1 = "~!@#$%^&*()_+" "{}|" ':"' "<>?"  # Shifted Punctuation
for _KC1 in _KEYCAPS_1:
    _KC0 = _KEYCAPS_0[_KEYCAPS_1.index(_KC1)]
    KEYCAPS_BY_STROKE[_KC1.encode()] = "⇧{}".format(_KC0)

for _KC in KEYCAPS:  # Letter, or Shift + Letter
    _XXS = _KC.lower().encode()
    if len(_XXS) == 1:
        KEYCAPS_BY_STROKE[_XXS] = _KC
        if _KC.upper() != _KC.lower():
            KEYCAPS_BY_STROKE[_KC.encode()] = "⇧{}".format(_KC)

KEYCAPS_BY_STROKE = dict((k, list(v)) for (k, v) in KEYCAPS_BY_STROKE.items())

KEYCAPS_BY_STROKE.update(  # ⌃ ⌥ ⇧ ⌘ also spoken as Control Alt-Option Shift Command
    {
        b"\x00": "⌃ Space".split(),
        b"\x09": "Tab".split(),  # could be ⌃I  # or drawn as ⇥
        b"\x0D": "Return".split(),  # could be ⌃M  # or drawn as ↩
        b"\x1B": "Esc".split(),  # could be ⌃[ or ⌃⇧[  # or drawn as ⎋
        b"\x1B\x4F\x50": "F1",  # or drawn as:  fn F1
        b"\x1B\x4F\x51": "F2",
        b"\x1B\x4F\x52": "F3",
        b"\x1B\x4F\x53": "F4",
        b"\x1B\x5B\x31\x35\x7E": "F5",
        b"\x1B\x5B\x31\x37\x7E": "F6",  # could be ⌥ F1
        b"\x1B\x5B\x31\x38\x7E": "F7",  # could be ⌥ F2
        b"\x1B\x5B\x31\x39\x7E": "F8",  # could be ⌥ F3
        b"\x1B\x5B\x31\x3B\x32\x43": "⇧ →".split(),
        b"\x1B\x5B\x31\x3B\x32\x44": "⇧ ←".split(),
        b"\x1B\x5B\x32\x30\x7E": "F9",  # could be ⌥ F4
        b"\x1B\x5B\x32\x31\x7E": "F10",  # could be ⌥ F5
        b"\x1B\x5B\x32\x33\x7E": "F11",  # could be ⌥ F6
        b"\x1B\x5B\x32\x34\x7E": "F12",  # could be ⌥ F7
        b"\x1B\x5B\x32\x35\x7E": "⌥ F8",
        b"\x1B\x5B\x32\x36\x7E": "⌥ F9",
        b"\x1B\x5B\x32\x38\x7E": "⌥ F10",
        b"\x1B\x5B\x32\x39\x7E": "⌥ F11",
        b"\x1B\x5B\x33\x31\x7E": "⌥ F12",
        b"\x1B\x5B\x41": "↑",  # or drawn as ▲
        b"\x1B\x5B\x42": "↓",  # or drawn as ▼
        b"\x1B\x5B\x43": "→",  # or drawn as ▶
        b"\x1B\x5B\x44": "←",  # or drawn as ◀
        b"\x1B\x5B\x5A": "⇧ Tab".split(),  # or drawn as ⇤
        b"\x1B\x62": "⌥ ←".split(),
        b"\x1B\x66": "⌥ →".split(),
        b"\x1C": "⌃\\",  # could be ⌃⇧\
        b"\x1D": "⌃]",  # could be ⌃⇧]  # near to ⇧] for }
        b"\x1E": "⌃⇧6",  # near to ⇧6 for ^
        b"\x1F": "⌃-",  # could be ⌃⇧-  # near to ⇧- for _
        b"\x20": "Space".split(),
        b"\x7F": "Delete".split(),  # or drawn as ⌫ and ⌦
        b"\xC2\xA0": "⌥ Space".split(),
    }
)


#
# Take Words from the Sh Command Line into KeyCaps Py
#


def parse_keycaps_args():
    """Take Words from the Sh Command Line into KeyCaps Py"""

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
    """Form an ArgumentParser for KeyCaps Py"""

    doc = __main__.__doc__
    parser = compile_argdoc(doc, epi="quirks")

    try:

        exit_unless_doc_eq(doc, parser)

    except SystemExit:
        stderr_print("keycaps.py: ERROR: main doc and argparse parser disagree")

        raise

    return parser


#
# Layer over Import ArgParse
#


def compile_argdoc(doc, epi):
    """Form an ArgumentParser, without defining Positional Args and Options"""

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
            xxs.decode()
        except UnicodeDecodeError:
            print("UnicodeDecodeError: {}".format(xxs))

            raise

        stroke = xxs

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
