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
import shlex
import signal
import string
import subprocess
import sys
import textwrap


_ = pdb


#
# Welcome Examples into 'p.py', Notes into 'p.py --h', & Preferences into 'p.py --'
#


def alt_main_doc():
    """Form an Alt Main Doc to fall back on, when no '__main__.__doc__' found"""

    filename = os.path.basename(__main__.__file__)
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
    doc = alt_main_doc() if (doc is None) else doc
    doc = alt_main_doc() if (doc is None) else doc

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
    doc = alt_main_doc() if (doc is None) else doc

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

    grafs = splitgrafs(doc)
    last_graf = grafs[-1]

    tests = graf_rip(last_graf)
    tests = list_strip(tests)
    testdoc = "\n".join(tests)

    # Choose a local End-of-ShLine Comment Style, for Paste of Sh Command Lines

    env_ps1 = os.getenv("PS1")
    env_zsh = env_ps1.strip().endswith("%#") if env_ps1 else False
    sh_testdoc = testdoc if env_zsh else testdoc.replace("&&:", "#")

    # Actually quit early, don't exit, when Parms supplied

    parms = sys.argv[1:]  # these 'parms' are the 'shlex.split' of the 'shparms'

    if not parms:

        print()
        print(sh_testdoc)
        print()

        sys.exit(0)


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
# Work well with "Grafs" = Paragraphs of Lines separated by Empty Lines
#


# deffed in many files  # missing from Python
def graf_rip(graf):
    """Pick the lines below the head line of a paragraph, and dedent them"""

    grafdoc = "\n".join(graf[1:])
    grafdoc = textwrap.dedent(grafdoc)
    graf = grafdoc.splitlines()

    return graf


# deffed in many files  # missing from Python
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


# deffed in many files  # missing from Python
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

        elif graf and (len(str_ldent(line)) > len(str_ldent(graf[0]))):

            graf.append(line)

        else:

            # Capture this Graf before the next Graf

            strip = list_strip(graf)
            if strip:
                grafs.append(strip)

            # Begin again

            graf = list()
            if line:
                graf.append(line)

    # Capture the last Graf before the End

    strip = list_strip(graf)
    if strip:
        grafs.append(strip)

    return grafs


# deffed in many files  # missing from Python
def str_ldent(chars):  # kin to 'str.lstrip'
    """Pick out the Spaces etc, at left of some Chars"""

    lstrip = chars.lstrip()
    length = len(chars) - len(lstrip)
    dent = chars[:length] if lstrip else ""

    return dent


#
# Run on top of a layer of general-purpose Python idioms,
#   while these are missing from:  https://docs.python.org
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


# deffed in many files  # missing from Python
def shlex_min_quote(parm):
    """Quote, but quote compactly despite '"' and '~', when that's still easy"""

    # Follow the Library, when they agree no quote marks required

    quoted = shlex_quote(parm)
    if quoted[:1] not in ("'", '"'):

        return quoted

    # Try accepting the ~ Tilde when the Parm does Not start with the ~ Tilde

    unplain = set(parm) - set(SH_PLAIN)
    if not parm.startswith("~"):
        if unplain == set("~"):

            return parm

    # Try the " DoubleQuote to shrink it

    unquotable = set(parm) - set(SH_QUOTABLE) - set("'")
    if not unquotable:
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


# deffed in many files  # missing from Python till Oct/2019 Python 3.8
def shlex_quote(parm):
    """Mark up a word with Quote Marks and Backslants, so Sh agrees it is one word"""

    # Trust the library, if available

    if hasattr(shlex, "quote"):
        quoted = shlex.quote(parm)

        return quoted

    # Emulate the library roughly, because often good enough

    unplain = set(parm) - set(SH_PLAIN)
    if not unplain:

        return parm

    quoted = repr(parm)  # as if the Py rules agree with Sh rules

    return quoted  # such as print(shlex_quote("<=>"))  # the 5 chars '<=>'

    # test results with:  python3 -c 'import sys; print(sys.argv)' ...


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
      cat p.py |cat -n |expand  # show how this works

"""

ALT_MAIN_DOC = textwrap.dedent(QUOTED_ALT_MAIN_DOC)
ALT_MAIN_DOC = ALT_MAIN_DOC.strip()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
