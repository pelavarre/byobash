#!/usr/bin/env python3

"""
usage: import byotools as byo

define a pile of conveniences for writing Python
"""

# TODO: less silence when run as __main__


import contextlib
import os
import pdb
import shlex
import signal
import sys

_ = pdb


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


def shlex_shortquote(arg):
    """Return the Arg quoted to pass through the Shell, but drop unnecessary quotes"""

    quoted = shlex.quote(arg)
    argv = shlex.split(arg)
    assert len(argv) == 1, (arg, argv)
    assert argv[-1] == arg, (arg, argv)

    quoteless = quoted[1:][:-1]
    quoteless_argv = shlex.split(quoteless)
    if argv == quoteless_argv:

        return quoteless

    return quoted


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
        shpath = shlex_shortquote(shortpath)

        return shpath


#
# notes:
#
#   1 ) '@dataclasses.dataclass' is new since Jun/2018 Python 3.7
#


# copied from:  git clone https://github.com/pelavarre/byobash.git
