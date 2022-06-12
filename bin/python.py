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
import sys

import byotools


def main():

    # Forward the absence of CLI Parms into ByoTools Exit

    parms = sys.argv[1:]
    if not parms:

        byotools.exit()

    # Take Parms from the Command Line

    parser = compile_python_argdoc()
    args = parser.parse_args()

    try:
        lines = pathlib.Path(args.file).read_text()
    except FileNotFoundError:

        byotools.exit()

    _ = lines

    # todo: call echo |python3 -m pdb
    # todo: call Black
    # todo: call Flake8
    # todo: call the file

    sys.stderr.write("python.py: not yet implemented at {}\n".format(args))

    sys.exit(3)


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


# do run from the Command Line, when not imported into some other main module
if __name__ == "__main__":

    main()


# copied from:  git clone https://github.com/pelavarre/byobash.git
