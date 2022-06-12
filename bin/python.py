#!/usr/bin/env python3

"""
usage: python.py [-h] [-i] [-m MODULE] FILE

interpret Python 3 or Python 2 language

positional arguments:
  FILE        the Python file to run

options:
  -h, --help  show this help message and exit
  -i          insert a breakpoint at process exit
  -m MODULE   import the module and call it with positional arguments and options

examples:
  bin/python.py bin/python.py  &&: test this tool on itself
  python.py p.py hi BYO Python  &&: run 'p.py' after calling Black & Flake8 to polish it
"""


import __main__
import argparse
import difflib
import os
import pathlib
import shlex
import string
import subprocess
import sys

import byotools


def main():
    """Run from the Command Line"""

    args = parse_python_args()

    # First compile

    if args.file:
        shfile = shlex_quote(args.file)

        pdb_shline = "python3 -m pdb {}".format(shfile)

        black_shline = "black {}".format(shfile)

        flake8_shline = "flake8"
        flake8_shline += " --max-line-length=999 --max-complexity 10 --ignore="
        flake8_shline += "E203"  # Black '[ : ]' rules over E203 whitespace before ':'
        flake8_shline += ",W503"  # Black over Flake8 W503 line break before binary op
        flake8_shline += " {}".format(shfile)

        subprocess_run(pdb_shline, check=True)
        subprocess_run(black_shline, check=True)
        subprocess_run(flake8_shline, check=True)

    # Run after compiline

    shparms = ""
    if args.i:
        shparms += " -i"
    if args.module:
        shmodule = shlex_quote(args.module)
        shparms += " -m {}".format(shmodule)
    if args.file:
        shparms += " {}".format(shfile)

    python3_shline = "python3 {}".format(shparms)

    subprocess_run(python3_shline, check=True)


def parse_python_args():
    """Take Parms from the Command Line"""

    # Call ByoTools Exit in the absence of Parms

    parms = sys.argv[1:]
    if not parms:

        byotools.exit()

    # Call ArgParse in the presence of Parms

    parser = compile_python_argdoc()
    args = parser.parse_args()

    try:
        _ = pathlib.Path(args.file).read_text()
    except FileNotFoundError:

        byotools.exit()

    # Return the Parsed Parms

    return args


def compile_python_argdoc():
    """Construct the ArgumentParser"""

    parser = compile_argdoc(epi="examples:")

    parser.add_argument("file", metavar="FILE", help="the Python file to run")

    parser.add_argument(
        "-i", action="store_true", help="insert a breakpoint at process exit"
    )
    parser.add_argument(
        "-m",
        metavar="MODULE",
        dest="module",
        help="import the module and call it with positional arguments and options",
    )

    doc = __main__.__doc__.strip()
    verbs = os.path.split(__file__)[-1]
    try:
        exit_unless_doc_eq(doc, parser=parser, verbs=verbs)
    except SystemExit:
        print("python.py: error: main doc and argparse parser disagree")

        raise

    return parser


#
# Run on top of a layer of general-purpose Python idioms
#


# deffed in many files  # missing from docs.python.org
def compile_argdoc(epi):
    """Construct an ArgumentParser, without defining Positional Args and Options"""

    doc = __main__.__doc__

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


# deffed in many files  # missing from docs.python.org
def exit_unless_doc_eq(doc, verbs, parser):
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

    main_doc = __main__.__doc__.strip()

    got = main_doc
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
        print("\n".join(diff_lines))

        sys.exit(1)  # trust caller to log SystemExit exceptions well


# deffed in many files  # missing from Python till Oct/2019 Python 3.8
def shlex_quote(arg):
    """Mark up with quote marks and backslashes , but only as needed"""

    # Trust the library, if available

    if hasattr(shlex, "quote"):
        quoted = shlex.quote(arg)

        return quoted

    # Emulate the library roughly, because often good enough

    mostly_harmless = set(
        "%+,-./"  # not: !"#$&'()*
        + string.digits
        + ":=@"  # not ;<>?
        + string.ascii_uppercase
        + "_"  # not [\]^
        + string.ascii_lowercase
        + ""  # not {|}~
    )

    likely_harmful = set(arg) - set(mostly_harmless)
    if likely_harmful:
        quoted = repr(arg)  # as if the Py rules agree with Sh rules

        return quoted

    return arg


# deffed in many files  # since Sep/2015 Python 3.5
def subprocess_run(shline, check):
    """
    Launch another Process at the LocalHost
    """

    sys.stderr.write("+ {}\n".format(shline))

    argv = shlex.split(shline)
    run = subprocess.run(argv, stdin=subprocess.PIPE)

    exitstatus = run.returncode
    if check and exitstatus:
        sys.stderr.write("+ exit {}\n".format(exitstatus))

        sys.exit(exitstatus)


# do run from the Command Line, when not imported into some other main module
if __name__ == "__main__":

    main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
