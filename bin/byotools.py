#!/usr/bin/env python3

"""
usage: import byotools as byo

define a pile of conveniences for writing Python

examples:
  byo.exit()  # take no Parms to print Examples, '--help' to print Help, else work
  byo.exit(__name__)  # like 'byo.exit()' but return without exit when imported
"""


import __main__
import os
import pathlib
import pdb
import shlex
import signal
import subprocess
import sys
import textwrap


_ = pdb


def exit(name=None, shparms=None):
    """Run a Py File with Help Lines & Examples in Main Doc, from the Sh Command Line"""

    # Actually quit early, don't exit, when just imported

    if name is not None:
        if name != "__main__":

            return

    # Actually quit early, don't exit, when the Caller wants to take the Parms

    parms = sys.argv[1:]

    if shparms is not None:
        wants = shlex.split(shparms)
        if parms == wants:

            return

    # Exit in one way or another, but always run the tests inside 'exit_via_testdoc'

    exit_via_testdoc()

    exit_via_argdoc()
    exit_via_command()


def exit_via_argdoc():
    """Exit after printing ArgDoc, if '--help' or '--hel' or ... '--h' before '--'"""

    doc = __main__.__doc__
    parms = sys.argv[1:]

    # Actually quit early, don't exit, when no '--help' Parm supplied

    for parm in parms:
        if parm == "--":

            break

        if parm.startswith("--h") and "--help".startswith(parm):

            # Else exit after printing ArgDoc

            print()
            print()
            print(doc.strip())
            print()
            print()

            sys.exit(0)


def exit_via_command():
    """Forward the Command as the Argv of a Subprocess"""

    # Collect many Args

    basename = os.path.basename(sys.argv[0])

    (root, ext) = os.path.splitext(basename)
    assert ext == ".py", dict(basename=basename)

    argv = list(sys.argv[:-1]) if (sys.argv[-1] in ("-", "--")) else sys.argv
    argv[0] = root

    # Form a ShLine

    shline = ""
    for arg in argv:
        if shline:
            shline += " "
        shline += shlex.quote(arg)

    # Trace and run the ShLine, but trace NonZero Exit Status ReturnCode, if any

    sys.stderr.write("+ {}\n".format(shline))

    run = subprocess.run(argv)
    if run.returncode:
        sys.stderr.write("{}: + exit {}\n".format(basename, run.returncode))

    sys.exit()  # Exit None, not Exit 0, after resorting to calling an Executable File


def exit_via_patchdoc(patchdoc):  # todo: pick the PatchDoc out of the ArgDoc
    """Exit after printing PatchDoc, if "--" is the only Parm"""

    # Collect many Args

    parms = sys.argv[1:]

    patchdoc_body = textwrap.dedent(patchdoc)
    patchdoc_body = patchdoc_body.strip()
    dented_patchdoc = textwrap.indent(patchdoc_body, "  ")

    # Demand one accurate copy of the PatchDoc in the ArgDoc

    assert dented_patchdoc in __main__.__doc__

    # Demand one accurate copy of the PatchDoc in the DotFiles

    bin_dir = os.path.dirname(__file__)
    dotfiles_dir = os.path.join(bin_dir, os.pardir, "dotfiles")
    pathname = os.path.join(dotfiles_dir, "dot.byo.bashrc")

    path = pathlib.Path(pathname)
    dotfiles_doc = path.read_text()

    assert patchdoc_body in dotfiles_doc

    # Actually quit early, don't exit, when no '--' Parm supplied

    if parms != ["--"]:

        return

    # Else exit after printing PatchDoc

    print()
    print(patchdoc_body)
    print()

    sys.exit(0)


def exit_via_testdoc():
    """Exit after printing last Graf, if no Parms"""

    # Collect many Args

    doc = __main__.__doc__

    grafs = splitgrafs(doc)
    last_graf = grafs[-1]

    tests = graf_dehang(last_graf)
    tests = graf_strip(tests)
    testdoc = "\n".join(tests)

    # Choose a local End-of-ShLine Comment Style, for Paste of Sh Command Lines

    env_ps1 = os.getenv("PS1")
    env_zsh = env_ps1.strip().endswith("%#") if env_ps1 else False
    sh_testdoc = testdoc if env_zsh else testdoc.replace("&&:", "#")

    # Actually quit early, don't exit, when Parms supplied

    parms = sys.argv[1:]

    if not parms:

        print()
        print(sh_testdoc)
        print()

        sys.exit(0)


def graf_dehang(graf):
    """Pick the lines below the head line of a paragraph, and dedent them"""

    grafdoc = "\n".join(graf[1:])
    grafdoc = textwrap.dedent(grafdoc)
    graf = grafdoc.splitlines()

    return graf


def graf_strip(graf):
    """Remove the leading Empty Lines and the trailing Empty Lines"""

    join = "\n".join(graf)
    strip = join.strip("\n")
    splitlines = strip.splitlines()

    return splitlines


def len_dent(line):
    """Count the Spaces at the Left of a Line"""

    length = len(line) - len(line.lstrip())

    return length


def os_path_homepath(path):
    """Return the Path relative to Env Home if below Env Home, else the AbsPath"""

    absname = os.path.abspath(path)

    env_home = os.environ["HOME"]
    if (absname == env_home) or absname.startswith(env_home + os.sep):
        home_relname = "~" + os.sep + os.path.relpath(absname, start=env_home)

        return home_relname

    return absname


def os_path_shortpath(path):
    """Return the shortest of the AbsPath, the RelPath, and the HomePath"""

    names = list()

    absname = os.path.abspath(path)
    names.append(absname)

    cwd = os.getcwd()
    if (absname == cwd) or absname.startswith(cwd + os.sep):
        cwd_relname = os.path.relpath(absname, start=cwd)
        names.append(cwd_relname)

    env_home = os.environ["HOME"]
    if (absname == env_home) or absname.startswith(env_home + os.sep):
        home_relname = "~" + os.sep + os.path.relpath(absname, start=env_home)
        names.append(home_relname)

    names.sort(key=lambda _: (len(_), _))

    concise = names[0]
    return concise


def splitgrafs(doc, keepends=False):
    """Pick each Paragraph out of a DocString"""

    assert not keepends  # FIXME: develop keepends=True

    grafs = list()

    lines = doc.splitlines()

    graf = list()
    for line in lines:

        # Collect every Empty Line and every More Dented Line

        if not line:

            if graf:
                graf.append(line)

        elif graf and (len_dent(line) > len_dent(graf[0])):

            graf.append(line)

        else:

            # Capture this Graf before the next Graf

            strip = graf_strip(graf)
            if strip:
                grafs.append(strip)

            # Begin again

            graf = list()
            if line:
                graf.append(line)

    # Capture the last Graf before the End

    strip = graf_strip(graf)
    if strip:
        grafs.append(strip)

    return grafs


class BrokenPipeSink:
    """
    Exit nonzero, but leave Stderr empty, at unhandled BrokenPipeError's

    Test with large Stdout cut sharply, such as:

        python3 -c 'for _ in range(54321): print(_)' |head -3

    as per:  https://docs.python.org/3/library/signal.html#note-on-sigpipe
    """

    DEFAULT_RETURN_CODE = 0x80 | signal.SIGPIPE
    assert DEFAULT_RETURN_CODE == 141, DEFAULT_RETURN_CODE  # viva Mac & Linux

    def __enter__(self, returncode=DEFAULT_RETURN_CODE):
        self.returncode = returncode

        return self

    def __exit__(self, *exc_info):
        (_, exc, _) = exc_info

        if exc is None:
            try:
                sys.stderr.flush()
                sys.stdout.flush()
            except BrokenPipeError as broken_pipe_error:
                exc = broken_pipe_error

        if isinstance(exc, BrokenPipeError):  # catch this one
            null_fileno = os.open(os.devnull, flags=os.O_WRONLY)
            os.dup2(null_fileno, sys.stdout.fileno())  # duck the rest of them

            sys.exit(self.returncode)

        # intervenes more narrowly than:
        #
        #   signal.signal(signal.SIGPIPE, handler=signal.SIG_DFL)
        #


class ShPath:
    """Wrap a Sh Path to print it more concisely"""

    def __init__(self, pathname):
        self.pathname = pathname

    def __str__(self):
        shortpath = os_path_shortpath(self.pathname)
        shpath = shlex.quote(shortpath)

        return shpath

    # could depend on '@dataclasses.dataclass', since Jun/2018 Python 3.7


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
