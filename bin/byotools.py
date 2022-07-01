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
import pdb
import shlex
import signal
import subprocess
import sys
import textwrap


_ = pdb


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


def exit(name=None, str_parms=None):
    """Run a Py File with Help Lines & Examples in Main Doc, from the Sh Command Line"""

    # Actually don't exit, when just imported

    if name is not None:
        if name != "__main__":

            return

    # Actually don't exit, when the Caller wants to take the Parms

    parms = sys.argv[1:]

    if str_parms is not None:
        wants = shlex.split(str_parms)
        if parms == wants:

            return

    # Exit in one way or another

    exit_via_argdoc_last_graf()
    exit_via_argdoc()
    exit_via_command()


def exit_via_argdoc_last_graf():
    """Exit after printing last Graf, if no Parms"""

    # Pick the trailing Paragraph of Example Tests out of the Main Arg Doc

    doc = __main__.__doc__

    grafs = splitgrafs(doc)
    last_graf = grafs[-1]

    tests = graf_dehang(last_graf)
    tests = graf_strip(tests)
    testdoc = "\n".join(tests)

    # Choose an End-of-ShLine Comment Style for Paste of Sh Command Lines

    env_ps1 = os.getenv("PS1")
    env_zsh = env_ps1.strip().endswith("%#") if env_ps1 else False
    sh_testdoc = testdoc if env_zsh else testdoc.replace("&&:", "#")

    # Default to print the Example Tests, and exit zero like "--help" does

    parms = sys.argv[1:]

    if not parms:

        print()
        print(sh_testdoc)
        print()

        sys.exit(0)


def exit_via_argdoc():
    """Exit after printing ArgDoc, if '--h' or '--he' or ... '--help' before '--'"""

    doc = __main__.__doc__
    parms = sys.argv[1:]

    for parm in parms:
        if parm == "--":

            break

        if parm.startswith("--h") and "--help".startswith(parm):

            print()
            print()
            print(doc.strip())
            print()
            print()

            sys.exit(0)


def exit_via_command():
    """Forward the Command as the Argv of a Subprocess"""

    basename = os.path.basename(sys.argv[0])

    (root, ext) = os.path.splitext(basename)
    assert ext == ".py", dict(basename=basename)

    argv = list(sys.argv[:-1]) if (sys.argv[-1] in ("-", "--")) else sys.argv
    argv[0] = root

    shline = ""
    for arg in argv:
        if shline:
            shline += " "
        shline += shlex.quote(arg)

    sys.stderr.write("+ {}\n".format(shline))

    run = subprocess.run(argv)
    if run.returncode:
        sys.stderr.write("{}: + exit {}\n".format(basename, run.returncode))

    sys.exit()


def graf_dehang(graf):
    """Pick the lines below the head line of a paragraph"""

    grafdoc = "\n".join(graf[1:])
    grafdoc = textwrap.dedent(grafdoc)
    graf = grafdoc.splitlines()

    return graf


def graf_strip(graf):
    """Remove the leading Empty Lines and the trailing Empty Lines"""

    # Remove off the leading Empty Lines

    lindex = 0
    for index in range(len(graf)):
        lindex = index
        if graf[lindex]:

            break

    # Remove off the trailing Empty Lines

    rindex = len(graf)
    for index in range(len(graf)):
        rindex = len(graf) - 1 - index
        if graf[rindex]:
            rindex += 1

            break

    # Succeed

    strip = graf[lindex:rindex]

    return strip


def len_dent(line):
    """Count the Spaces at the Left of a Line"""

    result = len(line) - len(line.lstrip())

    return result


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
            os.dup2(null_fileno, sys.stdout.fileno())  # avoid the next one

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


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    print("usage: import byotools as byo", file=sys.stderr)

    sys.exit(2)


#
# quirks:
#
#   1 ) '@dataclasses.dataclass' is new since Jun/2018 Python 3.7
#


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
