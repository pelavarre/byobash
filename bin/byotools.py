#!/usr/bin/env python3

# deffed in many packages  # missing from:  https://pypi.org
"""
usage: import byotools as byo

bundle the Python you need to make Sh welcome you sincerely and competently

examples:
  byo.exit()  # take no Parms to print Examples, '--help' to print Help, else just work
  byo.exit(__name__)  # like 'byo.exit()' but return without exit when imported
  byo.exit(shparms="--")  # like 'byo.exit()' but return when the only Parm is '--'
"""


import __main__
import os
import pathlib
import pdb
import re
import shlex
import shutil
import signal
import string
import subprocess
import sys
import textwrap


_ = pdb


#
# Welcome Examples into 'p.py', Notes into 'p.py --h', & Preferences into 'p.py --'
#


def alt_main_doc(xxfilexx):
    """Form an Alt Main Doc to fall back on, when no '__main__.__doc__' found"""

    filename = os.path.basename(xxfilexx)  # such as when 'xxfilexx=__main__.__file__'
    alt_main_doc = ALT_MAIN_DOC.replace("p.py", filename)

    return alt_main_doc


def exit(name=None, shparms=None):
    """Exit after printing TestDoc, or ArgDoc, or running a Subprocess, else return"""

    # Actually quit early, don't exit, when just imported

    if name is not None:
        if name != "__main__":

            return

    # Actually quit early, don't exit, when the Caller wants to take the Parms

    parms = sys.argv[1:]  # these 'parms' are the 'shlex.split' of the 'shparms'

    if shparms is not None:
        wants = shlex.split(shparms)
        if parms == wants:

            return

    # Exit in one way or another, but always run the tests inside 'exit_via_testdoc'

    exit_via_testdoc()

    exit_via_argdoc()
    exit_via_shcommand()


def exit_via_argdoc():
    """Exit after printing ArgDoc, if '--help' or '--hel' or ... '--h' before '--'"""

    doc = __main__.__doc__
    doc = alt_main_doc(__main__.__file__) if (doc is None) else doc

    parms = sys.argv[1:]  # these 'parms' are the 'shlex.split' of the 'shparms'

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


def exit_via_shcommand():
    """Forward the Command as the Argv of a Subprocess, and exit"""

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

    doc = __main__.__doc__
    doc = alt_main_doc(__main__.__file__) if (doc is None) else doc

    parms = sys.argv[1:]  # these 'parms' are the 'shlex.split' of the 'shparms'

    patchdoc_body = textwrap.dedent(patchdoc)
    patchdoc_body = patchdoc_body.strip()
    dented_patchdoc = textwrap.indent(patchdoc_body, "  ")

    # Demand one accurate copy of the PatchDoc in the ArgDoc

    assert dented_patchdoc in doc

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
    doc = alt_main_doc() if (doc is None) else doc

    grafs = str_splitgrafs(doc)
    last_graf = grafs[-1]

    tests = str_ripgraf(last_graf)
    tests = list_strip(tests)
    testdoc = "\n".join(tests)

    # Choose a local End-of-ShLine Comment Style, for Paste of Sh Command Lines

    env_ps1 = os.environ.get("PS1")
    env_zsh = env_ps1.strip().endswith("%#") if env_ps1 else False

    sh_testdoc = testdoc
    if env_zsh:
        sh_testdoc = sh_testdoc_to_zsh_testdoc(testdoc)

    # Actually quit early, don't exit, when Parms supplied

    parms = sys.argv[1:]  # these 'parms' are the 'shlex.split' of the 'shparms'

    if not parms:

        print()
        print(sh_testdoc)
        print()

        sys.exit(0)


def sh_testdoc_to_zsh_testdoc(testdoc):
    """Reformat a classic Sh TestDoc to work inside Zsh UnSetOpt InteractiveComments"""

    zsh_lines = list()
    for line in testdoc.splitlines():
        (before, mark, after) = line.partition("  # ")

        zsh_line = line
        if mark:
            enough = after
            enough = enough.replace("#", ".")
            enough = re.sub(r"'[^'\\]*'", repl=".", string=enough)
            enough = re.sub(r"{[^,]*}", repl=".", string=enough)

            rep_after = " # {!r}".format(after)
            try:
                enough_argv = shlex.split(enough)
                if enough_argv != list(shlex_dquote(_) for _ in enough_argv):
                    rep_after = after
            except ValueError:
                pass

            zsh_line = "{}  &&: {}".format(before, rep_after)

        zsh_lines.append(zsh_line)

    zsh_testdoc = "\n".join(zsh_lines)

    return zsh_testdoc


#
# Start dreaming of compacting ShLine's well
#


# todo: def shlex_compact(shline), shlex_compact(argv)


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


class ShPath:
    """Wrap a Sh Path to print it more concisely"""

    def __init__(self, pathname):
        self.pathname = pathname

    def __str__(self):
        shortpath = os_path_shortpath(self.pathname)
        shpath = shlex.quote(shortpath)

        return shpath

    # could depend on '@dataclasses.dataclass', since Jun/2018 Python 3.7


#
# Add some Def's to List's
#


def list_strip(items):
    """Drop the leading and trailing Falsey Items"""

    # Find the leftmost Truthy Item, else 0

    index = 0
    while items[index:]:
        if items[index]:

            break

        index += 1

    # Find the rightmost Truthy Item, else -1

    rindex = -1
    while items[:rindex]:
        if items[rindex]:

            break

        rindex -= 1

    # Drop the leading and trailing Falsey Items,
    # by way of picking all the Items from leftmost through rightmost Truthy Item

    lstrip = items[index:]
    strip = lstrip[: (rindex + 1)] if (rindex < -1) else lstrip

    return strip


#
# Add some Def's to Str's, while not found in 'import textwrap'
#


def str_ldent(chars):  # kin to 'str.lstrip'
    """Pick out the Spaces etc, at left of some Chars"""

    lstrip = chars.lstrip()
    length = len(chars) - len(lstrip)
    dent = chars[:length] if lstrip else ""

    return dent


def str_ripgraf(graf):
    """Pick the lines below the head line of a paragraph, and dedent them"""

    grafdoc = "\n".join(graf[1:])
    grafdoc = textwrap.dedent(grafdoc)
    graf = grafdoc.splitlines()

    return graf


def str_removeprefix(chars, prefix):  # missing from Python till Oct/2020 Python 3.9
    """Remove Prefix from Chars if present"""

    result = chars
    if chars.startswith(prefix):
        result = chars[len(prefix) :]

    return result


def str_removesuffix(chars, suffix):  # missing from Python till Oct/2020 Python 3.9
    """Remove Suffix from Chars if present"""

    result = chars
    if chars.endswith(suffix):
        result = chars[: -len(suffix)]

    return result


def str_splitgrafs(doc, keepends=False):  # todo:
    """Form a List of every Paragraph of Lines, out of a DocString"""

    assert not keepends  # todo: develop keepends=True

    grafs = list()

    lines = doc.splitlines()

    graf = list()
    for line in lines:

        # Add an Empty Line

        if not line:
            if graf:

                graf.append(line)

        # Add a More Dented Line

        elif graf and (len(str_ldent(line)) > len(str_ldent(graf[0]))):

            graf.append(line)

        # Strip and close this Graf, and pick it up if it's not Empty

        else:
            strip = list_strip(graf)
            if strip:

                grafs.append(strip)

            # Open the next Graf, with a No More Dented Line, else as Empty

            graf = list()
            if line:

                graf.append(line)

    # Strip and close the last Graf too, and pick it up too if it's not Empty

    strip = list_strip(graf)
    if strip:

        grafs.append(strip)

    return grafs


#
# Add some Def's that 'import pdb' forgot
#


def pdb_iobreakif(flag):
    """Breakpoint after reconnecting Py Stdio to Dev Tty, if Flag is Truthy"""

    if flag:
        pdb_iobreak()


def pdb_iobreak():
    """Breakpoint after reconnecting Py Stdio to Dev Tty"""

    reading = open("/dev/tty", "r")
    writing = open("/dev/tty", "w")

    sys.stdin = reading
    sys.stdout = writing

    pdb.set_trace()


#
# Add some Def's that 'import shlex' and 'import string' forgot
#


SH_PLAIN = (  # all printable Ascii except not " !#$&()*;<>?[]^`{|}~" and " and ' and \
    "%+,-./"
    + string.digits
    + ":=@"
    + string.ascii_uppercase
    + "_"
    + string.ascii_lowercase
)


SH_QUOTABLE = SH_PLAIN + " " + "!#&()*;<>?[]^{|}~"
# all printable Ascii except not $ Dollar and ` Backtick, and not " and ' and \


def shlex_dquote(parm):  # see also 'shlex.join' since Oct/2019 Python 3.8
    """Quote, but quote compactly despite '"' and '~', when that's still easy"""

    # Follow the Library, when they agree no quote marks required

    quoted = shlex_quote(parm)
    if quoted[:1] not in ("'", '"'):

        return quoted

    # Accept the ^ Caret when the Parm does start with the ^ Caret
    # Accept the ~ Tilde when the Parm does Not start with the ~ Tilde

    unplain_set = set(parm) - set(SH_PLAIN)
    if parm.startswith("^"):
        unplain_set = set(parm[1:]) - set(SH_PLAIN)  # restart
    if not parm.startswith("~"):
        unplain_set = unplain_set - set("~")  # mutate

    unplain_ascii_set = "".join(_ for _ in unplain_set if ord(_) < 0x80)
    if not unplain_ascii_set:

        return parm

    # Try the " DoubleQuote to shrink it

    unquotable_set = set(parm) - set(SH_QUOTABLE) - set("'")
    unquotable_ascii_set = "".join(_ for _ in unquotable_set if ord(_) < 0x80)
    if not unquotable_ascii_set:
        doublequoted = '"' + parm + '"'
        if len(doublequoted) < len(quoted):

            return doublequoted

    # Give up and settle for the Library's work

    return quoted

    # todo: figure out when the ^ Caret is plain enough to need no quoting
    # todo: figure out when the {} Braces are plain enough to need no quoting
    # todo: figure out when the ! Bang is plain enough to need no quoting

    # todo: figure out when the * ? [ ] are plain enough to need no quoting
    # so long as we're calling Bash not Zsh
    # and the Dirs don't change out beneath us


def shlex_quote(parm):  # see also 'shlex.join' since Oct/2019 Python 3.8
    """Mark up a word with Quote Marks and Backslants, so Sh agrees it is one word"""

    # Trust the library, if available

    if hasattr(shlex, "quote"):
        quoted = shlex.quote(parm)

        return quoted

    # Emulate the library roughly, because often good enough

    unplain_set = set(parm) - set(SH_PLAIN)
    if not unplain_set:

        return parm

    quoted = repr(parm)  # as if the Py rules agree with Sh rules

    return quoted  # such as print(shlex_quote("<=>"))  # the 5 chars '<=>'

    # test results with:  python3 -c 'import sys; print(sys.argv)' ...


def shlex_parms_partition(parms):
    """Split Options from Positional Args, in the classic way of ArgParse and Sh"""

    options = list()
    first_seps = list()
    positional_args = list()

    for (index, parm) in enumerate(parms):

        # Pick out the First Sep
        # and take the remaining Parms as Positional Args, not as Options

        if parm == "--":
            first_seps.append(parm)
            positional_args.extend(parms[(index + 1) :])

            break

        # Pick out each Option, before the First Sep

        if (parm != "-") and parm.startswith("-"):
            options.append(parm)

        # Pick out each Arg, before the First Sep

        else:
            positional_args.append(parm)

    return (options, first_seps, positional_args)


#
# Add some Def's that 'import shutil' forgot
#


def shutil_get_std_else_tty_height():  # from $LINES, else Stdout, else DevTty
    "Count Rows in the Terminal Screen"

    size = get_std_else_tty_size()

    return size.lines


def shutil_get_std_else_tty_width():  # from $COLUMNS, else Stdout, else DevTty
    "Count Rows in the Terminal Screen"

    size = get_std_else_tty_size()

    return size.columns


def get_std_else_tty_size():  # from $LINES and $COLUMNS, else Stdout, else DevTty
    "Count Rows and Columns in the Terminal Screen"

    _ = os.get_terminal_size(sys.stdout.fileno())  # fail fast, or not

    with open("/dev/tty", "r") as tty:  # fallback to Dev Tty, before (80, 24)
        fallback_size = os.get_terminal_size(tty.fileno())

    size = shutil.get_terminal_size(fallback=fallback_size)

    return size  # (.lines, .columns)


#
# Add some Def's that 'import sys' forgot
#


class BrokenPipeSink:  # todo: add calls of it, don't just define it
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


#
# Define the Arg Doc to fall back on, when no Arg Doc found at:  __main.__doc__
#


QUOTED_ALT_MAIN_DOC = """

    usage: cd bin/ && python3 p.py [--h]

    demo how to fork ByoBash by downloading 1 File and writing 3 Lines of Code

    options:
      --help  show this help message and exit

    examples:

      ls -1 byotools.py p.py  # show you have come to work here with us

      python3 p.py  # show these examples and exit
      python3 p.py --h  # show this help message and exit
      python3 p.py --  # do your choice of some other work for you

      less -N -FIRX p.py  # show how this works

"""

ALT_MAIN_DOC = textwrap.dedent(QUOTED_ALT_MAIN_DOC)
ALT_MAIN_DOC = ALT_MAIN_DOC.strip()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
