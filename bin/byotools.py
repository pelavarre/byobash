#!/usr/bin/env python3

# deffed in many packages  # missing from:  https://pypi.org

"""
usage: import byotools as byo  # define Func's
usage: python3 bin/byotools.py  # run Self-Test's

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


DEFAULT_NONE = None


#
# Welcome Examples at 'p.py', Notes at 'p.py --h', & Preferences/ Setup at 'p.py --';
# else exit after calling Subprocess of Sh Path;
# else exit nonzero for rare usage
#


def exit(name=None, shparms=None):
    """Exit after printing TestDoc, or ArgDoc, or running a Subprocess, else return"""

    parms = sys.argv[1:]

    # Return if imported, not called to run as the Main Module

    if name is not None:
        if name != "__main__":

            return

    # Return if given ShParms that the Caller wants to take

    if shparms is not None:
        wants = shlex.split(shparms)
        if parms == wants:

            return

    # Exit after printing the Test Doc of the Arg Doc, for no Parms

    exit_if_testdoc()

    # Exit after printing the Arg Doc, for '--help' or '--hel' or ... '--h' before '--'

    exit_if_argdoc()

    # Exit after calling Subprocess of Sh Path, else exit nonzero for rare usage

    exit_after_shverb()


#
# Welcome Examples at 'p.py', Notes at 'p.py --h', & Preferences/ Setup at 'p.py --'
#


def exit_if_testdoc():
    """Exit after printing last Graf, if no Parms"""

    parms = sys.argv[1:]

    _ = fetch_testdoc()  # always fetch, sometimes print

    if not parms:

        exit_after_testdoc()


def exit_after_testdoc():
    """Exit after printing a TestDoc of Examples"""

    testdoc = fetch_testdoc()

    print()
    print(testdoc.strip())  # frame by 1 Empty Line above, and 1 Empty Line below
    print()

    sys.exit(0)  # Exit 0 after printing Help Lines


def fetch_testdoc():
    """Fetch the TestDoc of Examples"""

    # Collect many Args

    argdoc = fetch_argdoc()

    grafs = str_splitgrafs(argdoc)
    last_graf = grafs[-1]

    tests = str_ripgraf(last_graf)
    tests = list_strip(tests)
    testdoc = "\n".join(tests)

    # Choose a local End-of-ShLine Comment Style, for Paste of Sh Command Lines

    env_ps1 = os.environ.get("PS1", DEFAULT_NONE)
    env_zsh = env_ps1.strip().endswith("%#") if env_ps1 else False

    sh_testdoc = testdoc
    if env_zsh:
        sh_testdoc = _sh_testdoc_to_zsh_testdoc(testdoc)

    # Suceed

    return sh_testdoc


def _sh_testdoc_to_zsh_testdoc(testdoc):
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
# Welcome Notes at 'p.py --h'
#


def exit_if_argdoc():
    """Exit after printing ArgDoc, if '--help' or '--hel' or ... '--h' before '--'"""

    parms = sys.argv[1:]

    _ = fetch_argdoc()  # always fetch, sometimes print

    if shlex_parms_want_help(parms):

        exit_after_argdoc()


def fetch_argdoc():
    """Fetch the ArgDoc of Help Lines"""

    main_doc = __main__.__doc__

    filename = os.path.basename(__main__.__file__)
    alt_main_doc = ALT_MAIN_DOC.replace("p.py", filename)

    argdoc = alt_main_doc if (main_doc is None) else main_doc

    return argdoc


def exit_after_argdoc():
    """Exit after printing an ArgDoc of Help Lines"""

    argdoc = fetch_argdoc()  # always fetch, sometimes print

    print()
    print()
    print(argdoc.strip())  # frame by 2 Empty Lines above, and 2 Empty Lines below
    print()
    print()

    sys.exit(0)  # Exit 0 after printing Help Lines


#
# Welcome Preferences at 'p.py --', and Preference else Setup at 'command p.py --'
#


def exit_if_patchdoc(fetched_patchdoc):
    """Exit after printing PatchDoc, if "--" is the only Parm"""

    parms = sys.argv[1:]

    _ = fetch_patchdoc(fetched_patchdoc)  # always fetch, sometimes print

    if parms == ["--"]:

        exit_after_patchdoc(fetched_patchdoc)


def exit_after_patchdoc(fetched_patchdoc):
    """Exit after printing a PatchDoc of how to poke the Memory of the Sh Process"""

    patchdoc = fetch_patchdoc(fetched_patchdoc)

    print()
    print(patchdoc.strip())  # frame by 1 Empty Line above, and 1 Empty Line below
    print()

    sys.exit(0)  # Exit 0 after printing Help Lines


def fetch_patchdoc(fetched_patchdoc):  # todo: pick the PatchDoc out of the ArgDoc
    """Fetch the PatchDoc of how to poke the Memory of the Sh Process"""

    # Collect many Args

    argdoc = fetch_argdoc()

    patchdoc = fetched_patchdoc
    patchdoc = textwrap.dedent(patchdoc)
    patchdoc = patchdoc.strip()
    dented_patchdoc = textwrap.indent(patchdoc, "  ")

    # Demand one accurate copy of the PatchDoc in the ArgDoc
    # Hope it doesn't have more Lines before or after it that we wrongly drop here

    assert dented_patchdoc in argdoc

    # Demand one accurate copy of the PatchDoc in the DotFiles
    # Again hope it doesn't have more Lines before or after it that we wrongly drop here

    bin_dir = os.path.dirname(__file__)
    dotfiles_dir = os.path.join(bin_dir, os.pardir, "dotfiles")
    pathname = os.path.join(dotfiles_dir, "dot.byo.bashrc")

    path = pathlib.Path(pathname)
    dotfiles_doc = path.read_text()

    assert patchdoc in dotfiles_doc  # else you need:  vi dotfiles/dot.byo.bashrc

    # Succeed

    return patchdoc


#
# Else exit after calling Subprocess of Sh Path, else exit nonzero for rare usage
#


def exit_if_rare_parms(shline, parms):
    """Exit 2 for rare usage if Parms truthy, else return"""

    if not parms:

        return

    shparms = shlex_djoin(parms)
    stderr_print("{}: ERROR: unrecognized arguments: {}".format(shline, shparms))

    sys.exit(2)  # Exit 2 for rare usage


def exit_after_shverb():
    """Exit after calling Subprocess of Sh Path, else exit nonzero for rare usage"""

    # Exit after calling Subprocess, if dropping the Py Ext Mark finds a Sh Verb

    exit_if_shverb(argv=sys.argv)

    # Else complain and exit 2 for rare usage

    main_py_basename = os.path.basename(sys.argv[0])
    shverb = str_removesuffix(main_py_basename, suffix=".py")

    stderr_print(
        "{}: ERROR: called while no {!r} found in Sh Path".format(
            main_py_basename, shverb
        )
    )

    sys.exit(2)  # Exit 2 for rare usage


def exit_if_shverb(argv):
    """Exit after calling Subprocess, if dropping the Py Ext Mark finds a Sh Verb"""

    alt_argv = sys.argv if (argv is None) else argv

    # Drop the Py Ext Mark

    main_py_basename = os.path.basename(alt_argv[0])

    (root, ext) = os.path.splitext(main_py_basename)  # Ext may be empty

    shverb = root
    shverb_argv = [shverb] + list(alt_argv[1:])

    # Actually quit early, don't exit, when Sh Verb not found in Sh Path

    which = shutil.which(shverb)
    if which is None:

        return

    if os.path.realpath(which) == os.path.realpath(sys.argv[0]):
        stderr_print(
            "byotools.py: declining to recurse through:  which -a {!r}".format(shverb)
        )

        return

    # Else exit after calling Subprocess

    exit_after_one_argv(argv=shverb_argv)


def exit_after_some_argv(argvs):
    """Run the ArgV's in order, till exit nonzero, else exit zero after the last one"""

    for argv in argvs:
        subprocess_run_loud_else_exit(argv)

    sys.exit()  # Exit None after every ArgV exits Falsey


def exit_after_one_argv(argv):
    """Call a Subprocess to run the ArgV, and then exit"""

    subprocess_run_loud_else_exit(argv)

    sys.exit()  # Exit None after an ArgV exits Falsey


def exit_after_print_raise(exc):
    """Stderr Print the Exec and then Exit Nonzero"""

    typename = dotted_typename(type(exc))
    str_raise = "byotools.py: {}: {}".format(typename, exc)
    stderr_print(str_raise)

    sys.exit(1)  # Exit 1 for Unhandled Exception


def dotted_typename(cls):
    """Return the 'module.type' name for most types, but 'type' for 'builtins.type's"""

    modulename = cls.__module__
    typename = cls.__name__
    dotted_typename = "{}.{}".format(modulename, typename)

    enough_typename = typename
    if modulename != "builtins":
        enough_typename = dotted_typename

    return enough_typename


def subprocess_run_loud_else_exit(argv, shpipe=None):
    """Call a Subprocess to run the ArgV and return, except exit if exit nonzero"""

    main_py_basename = os.path.basename(sys.argv[0])

    alt_shpipe = shpipe if shpipe else shlex_djoin(argv)
    stderr_print("+ {}".format(alt_shpipe))

    run = subprocess.run(argv)  # close kin to 'subprocess.run(argv, check=True)'
    if run.returncode:
        stderr_print("{}: + exit {}".format(main_py_basename, run.returncode))

        sys.exit(run.returncode)  # Pass back a NonZero Exit Status ReturnCode


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


bytes_removeprefix = str_removeprefix


def str_removesuffix(chars, suffix):  # missing from Python till Oct/2020 Python 3.9
    """Remove Suffix from Chars if present"""

    result = chars
    if chars.endswith(suffix):
        result = chars[: -len(suffix)]

    return result


bytes_removesuffix = str_removesuffix


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


def shlex_djoin(parms):  # see also 'shlex.join' since Oct/2019 Python 3.8
    """Quote, but quote compactly despite '"' and '~', when that's still easy"""

    shline = " ".join(shlex_dquote(_) for _ in parms)

    return shline  # such as:  echo "let's" speak freely, even casually


def shlex_dquote(parm):
    """Quote 1 Parm, but quote compactly despite '"' and '~', when that's still easy"""

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


def shlex_quote(parm):  # missing from Python till Oct/2019 Python 3.8
    """Mark up 1 Parm with Quote Marks and Backslants, so Sh agrees it is 1 Word"""

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


def shlex_parms_want_help(parms):
    """Return Truthy if '--help' or '--hel' or ... '--h' before '--'"""

    for parm in parms:
        if parm == "--":  # ignore '--help' etc after '--'

            break

        if parm.startswith("--h") and "--help".startswith(parm):

            return True


def shlex_parms_pop_opt_count(parms, opt):  # todo: add tests of this
    """Pop the usage '[-opt]' out of the Parms"""

    count = 0

    # Visit each Parm, except quit before first "--" Dash-Dash

    for (index, parm) in enumerate(parms):  # commonly taken from:  parms = sys.argv[1:]
        if parm == "--":

            break

        # Find and count and pop the wanted Option

        if parm == opt:

            stop = index + 1
            parms[::] = parms[:index] + parms[stop:]

            count += 1

    # Succeed

    return count


def shlex_parms_pop_option_value(parms, option, enough, const):
    """Pop the usage '[--option [VALUE]]' out of the Parms"""

    main_py_basename = os.path.basename(__main__.__file__)

    # Visit each Parm, except quit before first "--" Dash-Dash

    for (index, parm) in enumerate(parms):  # commonly taken from:  parms = sys.argv[1:]
        if parm == "--":

            break

        # Find the wanted Option, or enough of its Leftmost Chars

        comparable = parm.split("=")[0]
        if comparable.startswith(enough) and option.startswith(comparable):

            # Pick out the Value of this Option

            option_index = index
            option_value = "=".join(parm.split("=")[1:])
            if not option_value:
                if const is not None:
                    option_value = const
                else:
                    option_index = index + 1
                    if option_index < len(parms):
                        option_value = parms[option_index]

                    else:

                        stderr_print(
                            "{}: ERROR: argument {}: expected one argument".format(
                                main_py_basename, option
                            )
                        )

                        sys.exit(2)  # Exit 2 for rare usage

            # Pop the Option and its Value too

            stop = option_index + 1
            parms[::] = parms[:index] + parms[stop:]

            # Succeed

            return option_value


def shlex_parms_partition(parms):
    """Split Options from Positional Args, in the classic way of ArgParse and Sh"""

    options = list()
    seps = list()
    words = list()

    for (index, parm) in enumerate(parms):

        # Pick out the First Sep
        # and take the remaining Parms as Positional Args, not as Options

        if parm == "--":
            seps.append(parm)

        # Pick out each Option, before the First Sep

        elif (not seps) and (parm != "-") and parm.startswith("-"):
            options.append(parm)

        # Pick out each Arg, before the First Sep

        else:
            words.append(parm)

    return (options, seps, words)

    #   look deeper into when '---' is an option, like Grep votes '---' is an Arg
    #
    #       % qd |g -e +++ -e ---
    #       + git diff
    #       ('+ grep -i -e +++ -e ---',)
    #       --- a/bin/byotools.py
    #       +++ b/bin/byotools.py
    #       --- a/bin/git.py
    #       +++ b/bin/git.py
    #       --- a/bin/shpipes.py
    #       +++ b/bin/shpipes.py
    #       --- a/todo.txt
    #       +++ b/todo.txt
    #       %
    #


#
# Add some Def's that 'import shutil' forgot
#


def shutil_get_tty_height():  # from $LINES, else Stdout, else DevTty
    """Count Screen Rows from exported $LINES, else Stdout, else Dev Tty"""

    size = shutil_get_tty_size()

    return size.lines


def shutil_get_tty_width():  # from $COLUMNS, else Stdout, else DevTty
    """Count Screen Columns from exported $COLUMNS, else Stdout, else Dev Tty"""

    size = shutil_get_tty_size()

    return size.columns


def shutil_get_tty_size():
    """Count Screen Rows & Columns from $LINES & $COLUMNS, else Stdout, else Dev Tty"""

    if sys.__stdout__.isatty():  # show how to call simpler 'os.' in place of 'shutil.'
        _ = os.get_terminal_size(sys.__stdout__.fileno())

    with open("/dev/tty", "r") as tty:  # replace the cheap Fallback of (80, 24)
        fallback_size = os.get_terminal_size(tty.fileno())

    size = shutil.get_terminal_size(fallback=fallback_size)
    # from 'sys.__stdout__', else 'os.environ["LINES"], ["COLUMNS"]', else Fallback

    return size  # (.lines, .columns)


#
# Add some Def's that 'import subprocess' forgot
#


def subprocess_run_oneline(shline, *args, **kwargs):

    run = subprocess_run_stdio(shline, *args, stdout=subprocess.PIPE, **kwargs)

    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    assert len(lines) == 1, (shline, args, kwargs, lines)
    line = lines[0]

    return line


def subprocess_run_stdio(shline, *args, **kwargs):
    """Flush Stdout, flush Stderr, and then call without Stdin"""

    argv = shlex.split(shline)

    alt_kwargs = dict(kwargs)
    if "stdin" not in kwargs.keys():
        alt_kwargs["stdin"] = subprocess.PIPE

    sys.stdout.flush()
    sys.stderr.flush()

    run = subprocess.run(argv, *args, **kwargs)

    return run


#
# Add some Def's that 'import sys' forgot
#


def stderr_print(*args, **kwargs):
    """Work like Print, but write Stderr in place of Stdout"""

    sys.stdout.flush()
    print(*args, file=sys.stderr, **kwargs)  # todo: what if "file" in kwargs.keys() ?
    sys.stderr.flush()


class BrokenPipeSink:  # todo: add calls of it, don't just define it
    """
    Exit nonzero, but leave Stderr empty, at unhandled BrokenPipeError's

    Test with large Stdout cut sharply, such as:

        python3 -c 'for _ in range(54321): print(_)' |head -3

    as per:  https://docs.python.org/3/library/signal.html#note-on-sigpipe
    """

    RETURN_CODE_141 = 141  # Mac & Linux convention for Signal SigPipe
    assert RETURN_CODE_141 == (0x80 | signal.SIGPIPE), (0x80, signal.SIGPIPE)

    def __enter__(self, returncode=RETURN_CODE_141):
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

            sys.exit(self.returncode)  # Exit 141, or as chosen, after BrokenPipeError

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


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":

    # Run some Self-Test's

    _ = shutil_get_tty_size()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byotools.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
