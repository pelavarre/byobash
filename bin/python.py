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
import os
import pathlib
import shlex
import signal
import subprocess
import sys
import textwrap


import byotools as byo


PYTHONX = "python3"  # todo: cope when PYTHONX != "python3"

SIGINT_RETURNCODE_130 = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE_130 == 130, (SIGINT_RETURNCODE_130, 0x80, signal.SIGINT)


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

        # Form the ShPipe's

        pdb_shline = "{pythonx} -m pdb {shfile}".format(pythonx=PYTHONX, shfile=shfile)
        pdb_shpipe = "{} >/dev/null".format(pdb_shline)

        black_shline = "black {}".format(shfile)

        black_shpipe = "{} && {}".format(activate_shline, black_shline)
        black_shshline = "bash -c ''{!r}''".format(black_shpipe)

        flake8_shline = "flake8"
        flake8_shline += " --max-line-length=999 --max-complexity 10 --ignore="
        flake8_shline += "E203"  # Black '[ : ]' rules over E203 whitespace before ':'
        flake8_shline += ",W503"  # Black over Flake8 W503 line break before binary op
        flake8_shline += " {}".format(shfile)

        flake8_shpipe = "{} && {}".format(activate_shline, flake8_shline)
        flake8_shshline = "bash -c ''{!r}''".format(flake8_shpipe)

        # Form the ArgV's

        pdb_argv = shlex.split(pdb_shline)
        black_argv = shlex.split(black_shshline)
        flake8_argv = shlex.split(flake8_shshline)

        # Run the ArgV's

        try:
            byo.subprocess_run_loud(pdb_argv, shpipe=pdb_shpipe, stdout=subprocess.PIPE)
            sys.stderr.write("+\n")
            byo.subprocess_run_loud(black_argv, shpipe=black_shpipe)
            sys.stderr.write("+\n")
            byo.subprocess_run_loud(flake8_argv, shpipe=flake8_shpipe)
            sys.stderr.write("+\n")
        except KeyboardInterrupt:
            sys.stderr.write("\n")
            sys.stderr.write("pythonx.py: KeyboardInterrupt\n")  # todo: python.py

            assert SIGINT_RETURNCODE_130 == 130, SIGINT_RETURNCODE_130

            sys.exit(SIGINT_RETURNCODE_130)  # Exit 130 to say KeyboardInterrupt SIGINT

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

    pythonx_argv = shlex.split(pythonx_shline)
    try:
        byo.subprocess_run_loud(pythonx_argv, stdin=None)
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        sys.stderr.write("pythonx.py: KeyboardInterrupt\n")  # todo: python.py

        assert SIGINT_RETURNCODE_130 == 130, SIGINT_RETURNCODE_130

        sys.exit(SIGINT_RETURNCODE_130)  # Exit 130 to say KeyboardInterrupt SIGINT


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

    parser = byo.compile_epi_argdoc(add_help=False, epi="quirks:")

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
        try:
            byo.exit_unless_doc_eq(doc, parser=parser)
        except SystemExit:
            print("python.py: ERROR: main doc and argparse parser disagree")

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
        argv = shlex.split(shshline)
        byo.subprocess_run_loud(argv)  # implicit 'stdin=subprocess.PIPE'

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
        argv = shlex.split(shshline)
        byo.subprocess_run_loud(argv)  # implicit 'stdin=subprocess.PIPE'


#
# Run from the Command Line, when not imported into some other Main module
#

if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/python.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
