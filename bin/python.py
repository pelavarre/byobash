#!/usr/bin/env python3

# assert should, occasion

"""
usage: python.py [--help] [-i] [-m MODULE] [FILE] ...

interpret Python 3 or Python 2 language

positional arguments:
  FILE       the Python file to run (default: run without '__file__')
  ...        options or positional arguments to forward into the FILE

options:
  --help     show this help message and exit
  -i         insert a breakpoint at process exit
  -m MODULE  import the module and call it with positional arguments and options

quirks:
  quits at SyntaxError, else calls Black to reform the code, and Flake8 to review it
  creates and updates the Dir '~/.venvs/byobash/' to host Black & Flake8
  classic Python rudely opens a new Session, without '__file__', when given no Parms

examples:

  python.py  # show these examples and exit
  python.py --h  # show this help message and exit
  python.py --  # suggest:  python.py -i

  python.py bin/python.py  # test this tool on itself
  python.py p.py -xyz PARM1  # call 'p.py' after calling Black and Flake8 to polish it
"""
# todo: help trace where blank 'print()' and 'sys.stderr.write("\n")' come from
# todo: help notice 'print("python.py:' appearing outside of 'python.py'


import __main__
import argparse
import datetime as dt
import difflib
import os
import pathlib
import shlex
import signal
import subprocess
import sys
import textwrap


import byotools as byo


PYTHONX = "python3"  # todo: cope when PYTHONX != "python3"

SIGINT_RETURNCODE = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE == 130, (SIGINT_RETURNCODE, 0x80, signal.SIGINT)


def main():  # noqa: C901 complex
    """Run from the Command Line"""

    # Take Parms from the Command Line

    args = parse_pythonx_args()

    # Create or update or accept unchanged the VEnv Dir of Black & Flake8

    activate_shline = venv_refresh("%Y-%m")

    # Define 'python.py --'

    parms = sys.argv[1:]
    if parms == ["--"]:
        shline = "{} -i".format(sys.argv[0])
        print("did you mean:  {}".format(shline))

        sys.exit(0)  # Exit 0 after printing Help Lines

    # First compile

    if args.file:
        shfile = byo.shlex_quote(args.file)

        pdb_shline = "{pythonx} -m pdb {shfile}".format(pythonx=PYTHONX, shfile=shfile)

        black_shline = "black {}".format(shfile)

        black_shshline = "{} && {}".format(activate_shline, black_shline)
        black_shshline = "bash -c ''{!r}''".format(black_shshline)

        flake8_shline = "flake8"
        flake8_shline += " --max-line-length=999 --max-complexity 10 --ignore="
        flake8_shline += "E203"  # Black '[ : ]' rules over E203 whitespace before ':'
        flake8_shline += ",W503"  # Black over Flake8 W503 line break before binary op
        flake8_shline += " {}".format(shfile)

        flake8_shshline = "{} && {}".format(activate_shline, flake8_shline)
        flake8_shshline = "bash -c ''{!r}''".format(flake8_shshline)

        try:
            subprocess_run(pdb_shline, stdout=subprocess.PIPE, check=True)
            sys.stderr.write("+\n")
            subprocess_run(black_shshline, check=True)
            sys.stderr.write("+\n")
            subprocess_run(flake8_shshline, check=True)
            sys.stderr.write("+\n")
        except KeyboardInterrupt:
            sys.stderr.write("\n")
            sys.stderr.write("pythonx.py: KeyboardInterrupt\n")  # todo: python.py

            assert SIGINT_RETURNCODE == 130, SIGINT_RETURNCODE

            sys.exit(SIGINT_RETURNCODE)  # Exit 130 to say KeyboardInterrupt SIGINT

    # Form the ShLine

    pythonx_shline = PYTHONX

    if args.i:
        pythonx_shline += " -i"
    if args.module:
        shmodule = byo.shlex_quote(args.module)
        pythonx_shline += " -m {}".format(shmodule)
    if args.file:
        pythonx_shline += " {}".format(shfile)

    for parm in args.cooked_subparms:
        pythonx_shline += " {}".format(byo.shlex_quote(parm))

    # Run it

    try:
        subprocess_run(pythonx_shline, stdin=None, check=True)
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        sys.stderr.write("pythonx.py: KeyboardInterrupt\n")  # todo: python.py

        assert SIGINT_RETURNCODE == 130, SIGINT_RETURNCODE

        sys.exit(SIGINT_RETURNCODE)  # Exit 130 to say KeyboardInterrupt SIGINT


def parse_pythonx_args():  # noqa C901 complex 11
    """Take Parms from the Command Line"""

    # Call ArgParse in the presence of Parms

    parser = compile_pythonx_argdoc()
    args = parser.parse_args()

    # Call ByoTools Exit in the absence of Parms, or when Parms led by '--help'

    byo.exit_if_testdoc()  # python.py
    byo.exit_if_argdoc()  # python.py --help

    assert not args.help

    # Require the FILE to exist

    if args.file is not None:
        try:
            _ = pathlib.Path(args.file).read_text()
        except FileNotFoundError:

            byo.exit()

    # Setup to autocorrect the SubParms

    taken_parms = list()
    if args.i:
        taken_parms.append("-i")
    if args.module:
        taken_parms.append("-m")
        taken_parms.append(args.module)
    if args.file:
        taken_parms.append(args.file)

    # AutoCorrect when ArgParse wrongly pulls a leading "--" out the ShParms of the File

    parms = sys.argv[1:]

    index_minus = max(parms.index(_) for _ in taken_parms)
    index = index_minus + 1
    if "--" in parms[:index]:
        taken_parms.append("--")

    assert index == len(taken_parms)

    cooked_subparms = list(parms[index:])
    args.cooked_subparms = cooked_subparms

    # Return the Parsed Parms

    return args


def compile_pythonx_argdoc():
    """Construct the ArgumentParser"""

    parser = compile_argdoc(add_help=False, epi="quirks:")

    parser.add_argument(
        "file",
        metavar="FILE",
        nargs=argparse.OPTIONAL,
        help="the Python file to run (default: run without '__file__')",
    )

    parser.add_argument(
        "--help", action="store_true", help="show this help message and exit"
    )
    parser.add_argument(
        "-i", action="store_true", help="insert a breakpoint at process exit"
    )
    parser.add_argument(
        "-m",
        metavar="MODULE",
        dest="module",
        help="import the module and call it with positional arguments and options",
    )
    parser.add_argument(
        "subparms",
        metavar="...",
        nargs=argparse.REMAINDER,
        help="options or positional arguments to forward into the FILE",
    )

    basename = os.path.basename(__main__.__file__)
    if basename == "python.py":  # todo: think more about when this is False

        doc = __main__.__doc__.strip()
        verbs = os.path.split(__file__)[-1]
        try:
            exit_unless_doc_eq(doc, parser=parser, verbs=verbs)
        except SystemExit:
            print("python.py: error: main doc and argparse parser disagree")

            raise

    return parser


#
# Create and update the Dir '~/.venvs/byobash/' to host Black & Flake8
#


def venv_refresh(stamper):
    """Create and update the Dir '~/.venvs/byobash/' to host Black & Flake8"""

    venv = os.path.expanduser("~/.venvs/byobash")

    if not os.path.exists(venv):

        venv_create(venv)
        venv_update(venv)

    elif venv_gone_stale(venv, stamper=stamper):  # often stamper="%Y:%m"

        venv_update(venv)

    activate_shline = "source ~/.venvs/byobash/bin/activate"

    return activate_shline


def venv_create(venv):
    """Create the VEnv Dir"""

    byobash_venv = os.path.expanduser("~/.venvs/byobash")
    assert venv == byobash_venv, dict(venv=venv, byobash_venv=byobash_venv)

    quoted_shchars = """
        mkdir -p ~/.venvs/byobash
        cd ~/.venvs/ && python3 -m venv byobash
        source ~/.venvs/byobash/bin/activate && which pip
    """  # todo: cope when PYTHONX != "python3"

    shchars = textwrap.dedent(quoted_shchars).strip()

    shlines = shchars.splitlines()
    for shline in shlines:
        shshline = "bash -c {!r}".format(shline)
        subprocess_run(shshline, check=True)

    # test with:  rm -fr ~/.venvs/byobash/


def venv_gone_stale(venv, stamper):
    """Return truthy when StrFTime of Stamper has changed"""

    stat = os.stat(venv)
    then = dt.datetime.fromtimestamp(stat.st_mtime)

    now = dt.datetime.now()

    if then.strftime(stamper) != now.strftime(stamper):  # often stamper="%Y:%m"

        return True

    # test with:  touch -d2021-12-31T00:00:00 ~/.venvs/byobash/


def venv_update(venv):
    """Init or Update the VEnv Dir"""

    byobash_venv = os.path.expanduser("~/.venvs/byobash")
    assert venv == byobash_venv, dict(venv=venv, byobash_venv=byobash_venv)

    activate_shline = "source ~/.venvs/byobash/bin/activate"

    quoted_shchars = """
        activate && pip install --upgrade pip
        activate && pip install --upgrade wheel

        activate && pip install --upgrade black
        activate && pip install --upgrade flake8
        activate && pip install --upgrade flake8-import-order

        touch ~/.venvs/byobash
    """

    shchars = textwrap.dedent(quoted_shchars).strip()
    shchars = shchars.replace("activate", activate_shline)

    shlines = shchars.splitlines()
    for shline in shlines:
        shshline = "bash -c {!r}".format(shline)
        subprocess_run(shshline, check=True)


#
# Run on top of a layer of general-purpose Python idioms
#


# deffed in many files  # missing from docs.python.org
def compile_argdoc(epi, add_help=True):
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
        add_help=add_help,
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

    difflines = list(
        difflib.unified_diff(
            a=got.splitlines(),
            b=want.splitlines(),
            fromfile=got_filename,
            tofile=want_filename,
        )
    )

    if difflines:
        print("\n".join(difflines))

        sys.exit(1)  # trust caller to log SystemExit exceptions well


def subprocess_run(shline, stdin=subprocess.PIPE, stdout=None, check=None):
    """
    Launch another Process at the LocalHost
    """

    sys.stderr.write("+ {}\n".format(shline))

    argv = shlex.split(shline)
    run = subprocess.run(argv, stdin=stdin, stdout=stdout, check=False)

    exitstatus = run.returncode
    if check and exitstatus:
        sys.stderr.write("+ exit {}\n".format(exitstatus))

        sys.exit(exitstatus)


#
# Run from the Command Line, when not imported into some other Main module
#

if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/python.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
