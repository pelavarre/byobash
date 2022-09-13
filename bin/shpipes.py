#!/usr/bin/env python3

r"""
usage: shpipes.py [--help] [--ext=[EXT]] VERB [WORD ...]

compose and run a Pipe on the Os Copy/Paste Buffer, or inside a Pipe

positional arguments:
  VERB         choice of Alias to expand
  WORD         choice of Options and Positional Args to run in place of defaults

options:
  --help       show this help message and exit
  --ext=[EXT]  autocomplete & print, don't run the Code (default None, else '--ext=""')

quirks:

  frames dumps of 'pbpaste' to Stdout with one empty Stderr Line before, and one after,
    especially for the case of an Os Copy/Paste Buffer leaving its last Line unclosed
  calls on 'pbpaste' and 'pbcopy' to dump/ load the Os Copy/Paste Buffer
    even though many Linuxes & Windows' ship without defining 'pbpaste' and 'pbcopy'

  defaults to Diff from a file named 'a'
  limits Diff and Find like Sh should, by way of the 'less -FIRX' Paginator
  dumps larger numbers of Lines into taller Screens, as defaults of:  head/tail -...
  calls 'make --' even for Make's that can't distinguish 'make --' from 'make'
  lets Linux Terminal Stdin echo ⌃D TTY EOF as '', vs macOS as '^D', all without '\n'

slang:

  sends Cat '--show-tabs --show-nonprinting' as '-tv', not so much '--show-ends' as '-e'
  sends Diff '--ignore-space-change --recursive --show-c-function -unified' as '-brpu'
  sends Emacs '--no-window-system' as '-nw'
  sends HexDump '-C', as such, to show "Canonical" Hex+Char, not just Hex
  sends Less '--quit-if-one-screen' as '-F', & '--ignore-case' as '-I' till you type -I
  sends Less '--RAW-CONTROL-CHARS' as '-R', & '--no-init' as '-X'
  sends Uniq '--count' as '-c'
  sends Wc '--lines' as '-l'

Bash Install:

  source qb/env-path-append.source  # defines 'c', 'cv', 'd', 'g', 'gi', and so on
  bash qb/env-path-append.source  # shows how to patch it into your Sh Path
  export PATH="${PATH:+$PATH:}~/Public/byobash/qb"  # does patch it into your Sh Path

call Python to filter Lines of the Os Copy/Paste Buffer

  python3 -c 'import this' |tail -n +3 |shpipes.py cv
  pbpaste  # shows those nineteen lines built here

  shpipes.py pbc 'ssh localhost' 'cd /usr/bin/' "export PS1='\\$ '"
  pbpaste  # shows those three lines built here (such that pressing ⌘V will run them)

  shpipes.py upper
  shpipes.py split

  shpipes.py join |cat -
  echo '  abc  ' |shpipes.py lstrip |cat -etv
  find . |shpipes.py 're.sub(r"/.*$", "/..."'

  shpipes.py --ext=.py lstrip  # prints how it works, doesn't do it

call Python to filter whole Copies of the Os Copy/Paste Buffer

  shpipes.py join
  shpipes.py enumerate  # kin to:  |shpipes.py c, |cat -n -tv - |expand
  shpipes.py readlines  # aka:  |shpipes.py sh sponge
  shpipes.py textwrap.dedent

call Sh to filter Lines of the Os Copy/Paste Buffer

  shpipes.py cv cut -d/ -f4-  # drops 'http://.../' suffix
  shpipes.py cv a '?' 1  # pbpaste |awk -F'?' '{print $1}' |pbcopy  # drops trackers
  shpipes.py cv awk -F'?' '{print $1}'  # same work, but not so abbreviated
  shpipes.py cv sponge  # works even while "bash -c 'sponge'" is missing

  shpipes.py --ext=.sh lstrip  # prints how it works, doesn't do it

examples:

  shpipes.py a  # awk '{print $NF}'  # usage: a, a SEP, a INDEX, a SEP INDEX, etc
  shpipes.py a 0  # awk '{print $0}'  # closes every Line, same as:  shpipes.py xa
  shpipes.py a /  # awk -F/ '{print $NF}'  # picks Basename out of Path
  shpipes.py a / 1 # awk '{print $1}'  # prints Top DirName out of Path
  shpipes.py a / -1 # awk '{print $(NF - 1)}'  # picks Dir of Basename out of Path

  shpipes.py c  # cat - >/dev/null
  shpipes.py c --  # ... |cat -n -tv - |expand  # shows PbPaste endswith unclosed Line
  shpipes.py c |sort  # cat - |sort
  shpipes.py echo abc |c  # cat -n -tv - |expand

  shpipes.py cv -etv  # pbpaste |cat -etv |expand  # but framed
  echo -n abcde |shpipes.py cv  # ... |pbcopy
  echo abcdef |shpipes.py cv |cat -  # ... |tee >(pbcopy) |...

  shpipes.py d  # diff -brpu A_FILE B_FILE |less -FIRX  # default A_FILE='a', B_FILE='b'
  shpipes.py e  # emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipes.py em  # emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipes.py f  # find . -not -type d -not -path './.git/*' |less -FIRX  # Mac needs .
  # 'g' often means 'git'
  shpipes.py g  # grep -i .
  shpipes.py gi  # grep .  # without '-i'
  shpipes.py gl  # grep -ilR
  shpipes.py gli  # grep -lR  # without '-i'
  shpipes.py gv  # grep -v -i .
  shpipes.py gvi  # grep -v .  # without '-i'
  shpipes.py h  # head -16  # or whatever a third of the screen is
  shpipes.py hi  # history  # but include the '~/.bash_histories/' dir
  shpipes.py ht  # sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'  # Head and also Tail
  # 'l' often means 'ls -CF' or 'less -FIRX'
  shpipes.py m  # make --
  shpipes.py mo  # less -FIRX
  shpipes.py n  # cat -n -tv - |expand  # mostly redundant with 'shpipes.c'
  # 'pb' often doesn't mean Paste Buffer of macOS Copy/Paste
  shpipes.py pbc ...  # (echo "$1"; echo "$2"; ...) |pbcopy
  shpipes.py q  # git checkout
  shpipes.py s  # sort -
  shpipes.py sp  # sponge.py --
  shpipes.py t  # tail -16  # or whatever a third of the screen is
  shpipes.py u  # uniq -c - |expand
  shpipes.py v  # vim -
  # 'w' often means '/usr/bin/w'
  shpipes.py wcl  # wc -l
  shpipes.py x  # hexdump -C  # od -A x -t x1 -v
  shpipes.py xa  # xargs -n 1
  shpipes.py xp  # expand

examples:

  shpipes.py  # shows these examples and exits
  shpipes.py --h  # shows this help message and exits
  shpipes.py --  # calls on Vi to edit the Os Copy/Paste Buffer

  shpipes.py pbedit vi +$  # calls on 'vi +$' to edit the Os Copy/Paste Buffer
  shpipes.py pbedit emacs -nw  # calls on 'emacs -nw' to edit the Os Copy/Paste Buffer

  shpipes.py cv  # pbpaste  # but framed by 1 Blank Stderr Line above, & 1 below
  shpipes.py cv --  # pbpaste |cat -n -tv - |expand  # framed and numbered
  shpipes.py cv dent  # as if:  cv sed 's,^,    ,'
  shpipes.py cv dedent  # as if:  cv sed 's,^    ,,'
"""
# todo:  solve my Sh Rc Aliases:  black flake8 2to3 futurize
# todo:  solve my Sh Rc Funcs:  :: ? cp dir-p-tac jqd mv o p py pylint pys while_ssh
# todo:  shpipes.py x  -->  inline hexdump.py


import argparse
import io
import os
import pdb
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap

import byotools as byo

_ = pdb


# Calc the process exit status returncode for Keyboard Interrupt

SIGINT_RETURNCODE_130 = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE_130 == 130, (SIGINT_RETURNCODE_130, 0x80, signal.SIGINT)


# Mark the ShVerb's that wrongly fall back to hang for input at Tty Stdin,
# when given only Options and Seps, but not Words, in the absence of PbPaste Stdin

EMACS_SHVERBS = "e em emacs".split()
VI_SHVERBS = "v vi vim".split()
NEED_FILE_SHVERBS = EMACS_SHVERBS + VI_SHVERBS  # todo: weakly accurate

STR_PBPASTE_SHVERBS = """
    awk cat expand grep head hexdump less sed sort sponge sponge.py tail uniq wc
"""  # todo: weakly accurate  # FIXME: 'sponge.py' in the STR_PBPASTE_SHVERBS
PBPASTE_SHVERBS = set(STR_PBPASTE_SHVERBS.split())


def main():
    """Run from the Sh Command Line"""

    # Parse the Sh Command Line of a call of ShPipes Py

    args = parse_shpipes_args()
    parms = args.parms

    main.ext = args.alt_ext

    # Take 'shpipes.py', 'shpipes.py --h', 'shpipes.py --he', ... 'shpipes.py --help'

    byo.exit_if_testdoc()  # shpipes.py
    byo.exit_if_argdoc()  # shpipes.py --help

    # Else pick apart how to take the Verb and its Words

    exit_via_main_parms(parms)


def exit_via_main_parms(parms):
    """Run the Usage VERB [WORD ...]"""

    shfunc_by_verb = form_shfunc_by_verb()

    # Take 'shpipes.py --' or 'shpipes.py --'
    # or 'shpipes.py --ext' or 'shpipes.py --ext=...'

    alt_parms = parms if parms else ["--"]
    if alt_parms[:1] == ["--"]:

        main.shverb = "--"
        exit_after_shfunc(shfunc=pbedit, parms=parms)
        # F=$(mktemp) && pbpaste >$F && vi $F && cat $F |pbcopy && rm $F

    # Take stunningly cryptic abbreviations of ShPipe's

    assert parms

    shverb = parms.pop(0)
    if shverb in shfunc_by_verb.keys():
        shfunc = shfunc_by_verb[shverb]

        main.shverb = shverb
        exit_after_shfunc(shfunc, parms=parms)

    # Take any verb of the Sh Path

    exit_if_shverb([shverb] + parms)

    # Autocomplete & run (or just print) the Code

    exit_if_rare_autocomplete(shverb, parms=parms)

    main.shverb = shverb
    exit_after_autocomplete(parms)


def parse_shpipes_args():
    """Parse the Usage [--ext [EXT]]"""

    parms = sys.argv[1:]

    # Pop the usage '[--ext [EXT]]' out of the Parms

    ext = byo.shlex_parms_pop_option_value(
        parms, option="--ext", enough="--e", const=""
    )

    alt_ext = ext
    if ext and not ext.startswith("."):
        alt_ext = "." + ext

    # Publish results

    args = argparse.Namespace()

    args.alt_ext = alt_ext
    args.parms = parms

    # Succeed

    return args


#
# Map stunningly cryptic abbreviations to our ShFunc's who run them as ShPipe's
#


def exit_after_shfunc(shfunc, parms):
    """Forward Parms into a Cryptically Abbreviated ShFunc and exit"""

    # Agree to run if Sh Source required, but refuse to run if other Source required

    if main.ext is not None:
        if main.ext not in ("", ".bash", ".sh", ".zsh"):
            byo.stderr_print(
                "shpipes.py: ERROR: --ext={!r} missing for shfunc:  {}".format(
                    main.ext, byo.shlex_djoin(parms) if parms else "--"
                )
            )

            sys.exit(2)  # exits 2 for rare usage

    # Trace and call and exit

    shfunc(parms)

    sys.exit()  # exits None after a Cryptically Abbreviated ShFunc


def form_shfunc_by_verb():
    """Declare the Pipe Filter Abbreviations"""

    shfunc_by_verb = dict(
        a=do_a,  # awk -F' ' '{print $NF}'  # a, a SEP, a INDEX, a SEP INDEX, etc
        c=do_c,  # cat - >/dev/null
        cv=do_cv,  # pbpaste |...  # ... |pbcopy
        d=do_d,  # diff -brpu A_FILE B_FILE |less -FIRX  # default '-brpu a b'
        e=do_e,  # (same as 'do_em')
        em=do_em,  # emacs -nw --no-splash --eval '(menu-bar-mode -1)'
        f=do_f,  # find . -not -type d -not -path './.git/*' |less -FIRX  # Mac needs .
        g=do_g,  # grep -i .
        gi=do_gi,  # grep .  # without '-i'
        gli=do_gli,  # grep -lR  # without '-i'
        gl=do_gl,  # grep -ilR
        gv=do_gv,  # grep -v -i .
        gvi=do_gvi,  # grep -v .  # without '-i'
        h=do_h,  # head -16  # or whatever a third of the screen is
        hi=do_hi,  # history  # but include the '~/.bash_histories/' dir
        ht=do_ht,  # sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'  # Head and also Tail
        m=do_m,  # make --
        mo=do_mo,  # less -FIRX
        n=do_n,  # cat -n -tv - - |expand
        pbc=do_pbc,  # (echo "$1"; echo "$2"; ...) |pbcopy
        pbedit=pbedit,  # Call on Vi to edit a Pipe Byte Stream, or on a chosen Editor
        q=do_q,  # git checkout
        s=do_s,  # sort -
        sp=do_sp,  # sponge.py --
        t=do_t,  # tail -16  # or whatever a third of the screen is
        u=do_u,  # uniq -c - |expand
        v=do_v,  # vim -
        wcl=do_wcl,  # wc -l
        x=do_x,  # hexdump -C
        xp=do_xp,  # expand
    )

    return shfunc_by_verb


#
# Define:  a, c
#


def do_a(parms):  # "qb/a"  # "a"
    """awk -F' ' '{print $NF}'  # usage: a, a SEP, a AWK_INDEX, a SEP AWK_INDEX, etc"""

    # Forward Parms transparently, when not taken as meaningful here:

    (sep, repr_index) = awk_parms_to_sep_repr_index(parms)
    if (sep is None) and (repr_index is None):

        exit_after_shparms("awk", parms=parms)

    # Autocomplete an Awk Code Fragment that is Sep or Awk Index or both or neither

    if sep in (None, " "):
        shline = "awk '{{print {}}}'".format(repr_index)
    else:
        shsep = byo.shlex_dquote(sep)
        shline = "awk -F{} '{{print {}}}'".format(shsep, repr_index)

    # Run the autocompleted Awk Code

    exit_after_shline(shline)


def awk_parms_to_sep_repr_index(parms):
    """Take usage 'AWK_SEP (.|AWK_INDEX)' or usage '.|AWK_INDEX|AWK_SEP', else None's"""

    sep = None
    repr_index = None

    if parms[2:]:  # forwards Parms transparently, when there are many

        pass

    elif parms[1:]:  # takes usage: AWK_SEP (.|AWK_INDEX)

        if len(parms[0]) == 1:
            if re.match(r"^[-+]?[0-9]+$", string=parms[1]) or (parms[1] == "."):
                sep = parms[0]
                int_index = None if (parms[1] == ".") else int(parms[1])
                repr_index = awk_repr_index(int_index)

    elif parms:  # takes usage: .|AWK_INDEX|AWK_SEP

        if re.match(r"^[-+]?[0-9]+$", string=parms[0]) or (parms[0] == "."):
            int_index = None if (parms[0] == ".") else int(parms[0])
            repr_index = awk_repr_index(int_index)
        elif len(parms[0]) == 1:
            sep = parms[0]
            repr_index = awk_repr_index(int_index=None)

    elif not parms:

        sep = " "
        repr_index = awk_repr_index(int_index=None)

    return (sep, repr_index)


def awk_repr_index(int_index):
    """ "Convert to Awk Repr Index from Awk Int Index"""

    repr_index = "$NF"
    if int_index is not None:
        if int_index < 0:  # '$NF' for Last Word, else Rightmost Words '$(NF - 1)' etc.
            repr_index = "$(NF - {})".format(abs(int_index))
        else:  # '$0' for Whole Line, else Leftmost Words '$1', '$2', etc
            repr_index = "${}".format(int_index)

    return repr_index


def do_c(parms):  # "qb/c"  # "c"
    """cat - >/dev/null"""

    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    if parms == ["--"]:

        exit_after_shpipe("cat -n -tv - |expand")

    if not parms:

        if not stdin_isatty:

            exit_after_shpipe("cat -n -tv - |expand")

        if stdout_isatty:

            exit_after_shpipe("cat - >/dev/null")

        exit_after_shline("cat -")

    exit_after_shparms("cat", parms=parms)


#
# Define:  cv
#


def do_cv(parms):  # "qb/cv"  # "cv"
    """pbpaste inside tty, pbpaste from tty, pbcopy to tty, else tee to pbcopy"""

    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    # Work differently to drain Pb, else fill Pb, else stream through Pb
    # Forward or reject Parms, don't drop them

    if stdin_isatty:  # cv ...  # also:  cv ... |...

        exit_after_framing_cv_if(parms)  # drains Pb

    elif stdout_isatty:  # ... |cv ...
        byo.exit_if_rare_parms("shpipes.py ... cv", parms=parms)

        exit_after_shline("pbcopy")  # fills Pb

    else:  # ... |cv ... |...
        byo.exit_if_rare_parms("shpipes.py ... cv ...", parms=parms)

        exit_after_shpipe("tee >(pbcopy)")  # streams through Pb


def exit_after_framing_cv_if(parms):
    """Exit after PbPaste into PbCopy, or after PbPaste"""

    (_, _, words) = byo.shlex_parms_partition(parms)
    if words:
        if main.ext is None:  # such as:  cv dent

            exit_after_cv_edit(parms)

        else:  # such as:  cv --e dent

            exit_after_cv_edit(["--ext={}".format(main.ext)] + parms)

    exit_after_framing_pbpaste_if(parms)  # such as:  cv |n


def exit_after_framing_pbpaste_if(parms):
    """Exit after PbPaste unmarked, or with Opts, or '|cat -n -tv - |expand' for Sep"""

    stdout_isatty = sys.stdout.isatty()
    plus = "\n" if stdout_isatty else ""  # todo: framing for Stdout Pipes

    try:

        if not parms:
            shpipe_plus = "pbpaste" + plus

            exit_after_shpipe(shpipe=shpipe_plus)

        (options, seps, words) = byo.shlex_parms_partition(parms)
        if seps and not (options or words):
            shpipe_plus = "pbpaste |cat -n -tv - |expand" + plus

            exit_after_shpipe(shpipe=shpipe_plus)

        shparms = byo.shlex_djoin(parms)
        shpipe_plus = "pbpaste |cat {} |expand".format(shparms) + plus

        exit_after_shpipe(shpipe=shpipe_plus)

    finally:

        if plus:
            byo.stderr_print()


def exit_after_cv_edit(parms):
    """Exit after running the Parms to edit the Os Copy/Paste Buffer"""

    shverb = parms[0]
    if shverb in NEED_FILE_SHVERBS:

        exit_after_cv_mktemp_pipe(parms)

    else:

        exit_after_cv_cv_pipe(parms)


def exit_after_cv_mktemp_pipe(parms):
    """Exit after running the Parms to edit a File of the Os Copy/Paste Buffer"""

    # Copy the Os Copy/Paste Buffer into a File

    with tempfile.NamedTemporaryFile() as sponge:
        path = sponge.name

        enter_run = subprocess.run(
            "pbpaste".split(), stdin=subprocess.PIPE, stdout=sponge
        )
        assert not enter_run.returncode

        # Call Self with Parms and Filename

        argv_0 = os.path.abspath(sys.argv[0])
        argv = [argv_0] + parms + [path]

        wrapped_run = subprocess.run(argv)
        if wrapped_run.returncode:
            byo.stderr_print("+ exit {}".format(wrapped_run.returncode))

            sys.exit(wrapped_run.returncode)

        # Copy the File into the Os Copy/Paste Buffer

        with open(path, "rb") as stdin:
            exit_run = subprocess.run("pbcopy".split(), stdin=stdin)

        assert not exit_run.returncode

    sys.exit()


def exit_after_cv_cv_pipe(parms):
    """Exit after running the Parms to edit a Pipe of the Os Copy/Paste Buffer"""

    # Sponge up the Paste Buffer to serve as Stdin

    ibytes = stdin_load()

    stdin = io.BytesIO(ibytes)
    with_stdin = sys.stdin
    sys.stdin = stdin

    # Add a 2nd Sponge to serve as Stdout

    stdout = io.BytesIO()
    with_stdout = sys.stdout
    sys.stdout = stdout

    # Run the Parms

    try:
        # exit_via_main_parms(parms)  # dies by 'io.UnsupportedOperation: fileno'
        subprocess_pipe_self(parms)
    finally:
        sys.stdin = with_stdin
        sys.stdout = with_stdout

    # Replace the Paste Buffer, if the Run of the Parms succeeded

    stdout.seek(0)
    obytes = stdout.read()

    stdout_dump(obytes)

    sys.exit()  # exits None after running Code


def subprocess_pipe_self(parms):
    """Call Self as a Pipe Filter between two Files"""

    with tempfile.TemporaryFile() as left_sponge:
        with tempfile.TemporaryFile() as right_sponge:

            ibytes = sys.stdin.read()
            left_sponge.write(ibytes)
            left_sponge.flush()  # unneeded?
            left_sponge.seek(0)

            #

            argv_0 = os.path.abspath(sys.argv[0])
            argv = [argv_0] + parms

            run = subprocess.run(argv, stdin=left_sponge, stdout=right_sponge)

            if run.returncode:
                byo.stderr_print("+ exit {}".format(run.returncode))

                sys.exit(run.returncode)  # passes back a NonZero Exit Status ReturnCode

            #

            right_sponge.flush()  # unneeded?
            right_sponge.seek(0)

            obytes = right_sponge.read()
            sys.stdout.write(obytes)
            sys.stdout.flush()  # unneeded?


#
# Define:  d, e, f
#


def do_d(parms):  # "qb/d"  # "d"
    """diff -brpu a b |less -FIRX"""

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-brpu")
    if len(words) < 2:
        words.insert(0, "a")
    if len(words) < 2:
        words.append("b")

    argv = ["diff"] + options + seps + words
    shline = byo.shlex_djoin(argv)

    exit_after_shline_to_tty(shline)


def do_e(parms):  # "qb/e"  # "e"
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    do_em(parms)


def do_em(parms):  # "qb/em"  # "em"
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    if not parms:  # a la 'byo.exit_if_testdoc'

        print()
        print("emacs -nw --no-splash --eval '(menu-bar-mode -1)'")
        print()

        sys.exit(0)  # exits 0 after printing Help Lines

    exit_after_shverb_shparms(
        "emacs -nw --no-splash --eval '(menu-bar-mode -1)'", parms=parms
    )


def do_f(parms):  # "qb/f"  # "f"
    """find . -not -type d -not -path './.git/*' |less -FIRX"""  # Mac Find needs '.'

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options = ["-not", "-type", "d", "-not", "-path", "./.git/*"]
    if not words:
        words.append(".")  # Mac Find needs an explicit '.'

    argv = ["find"] + words + options + seps  # classic Find takes Words before Options
    shline = byo.shlex_djoin(argv)

    exit_after_shline_to_tty(shline)


#
# Define:  g, gi, gl, gli, gv, gvi
# todo: merge with 'git.py' near 'def exit_if_g'
#


def do_g(parms):  # "qb/g"  # "g"
    """grep -i ."""

    do_g_parms_shoptions_shwords(parms, shoptions="-i", shwords=".")


# todo: merge with 'grep.py' and 'git.exit_if_g_parms_shoptions_shwords'
def do_g_parms_shoptions_shwords(parms, shoptions, shwords=None):
    """Forward ShLine of Options or Seps, else default to Options and Words"""

    stdout_isatty = sys.stdout.isatty()

    # Forward ShLine w Parms of Options or Seps

    (options, seps, words) = byo.shlex_parms_partition(parms, mark="-e")
    if options or seps:
        shline = "grep {}".format(shoptions).rstrip()

        marked_alt_parms = options + seps + words
        if set(marked_alt_parms) - set(parms):

            exit_after_shparms(shline, parms=marked_alt_parms)

        else:

            exit_after_shparms(shline, parms=parms)

    # Else default to Options and Words, except also add Color into a Tty Stdout

    options = shlex.split(shoptions)
    if stdout_isatty:
        if shwords:
            options.append("--color=auto")

    if not words:
        if shwords:
            words = shlex.split(shwords)

    # Trace and call and exit

    shline = "grep"
    alt_parms = options + seps + words

    exit_after_shparms(shline, parms=alt_parms)


def do_gi(parms):  # "qb/gi"  # "gi"
    """grep ."""

    do_g_parms_shoptions_shwords(parms, shoptions="", shwords=".")


def do_gl(parms):  # "qb/gl"  # "gl"
    """grep -ilR"""  # better No ShWords, than r"." to match too many Lines

    do_g_parms_shoptions_shwords(parms, shoptions="-ilR", shwords="")


def do_gli(parms):  # "qb/gli"  # "gli"
    """grep -lR"""  # better No ShWords, than r"." to match too many Lines

    do_g_parms_shoptions_shwords(parms, shoptions="-lR", shwords="")


def do_gv(parms):  # "qb/gv"  # "gv"
    """grep -v -i ."""

    do_g_parms_shoptions_shwords(parms, shoptions="-v -i", shwords=".")


def do_gvi(parms):  # "qb/gvi"  # "gvi"
    """grep -v"""

    do_g_parms_shoptions_shwords(parms, shoptions="-v", shwords=".")


#
#  Define:  h, hi, ht, m, mo, n, pbc, q, s, sp, t, u, v, wcl, x, xa, xp
#


def do_h(parms):  # "qb/h"  # "h"
    """head -16  # or whatever a third of the screen is"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["head"] + options + seps + words
    shline = byo.shlex_djoin(argv)

    exit_after_shline(shline)


def do_hi(parms):  # "qb/hi"  # "hi"
    """history  # but include the files at the '~/.bash_histories/' dir"""

    raise NotImplementedError()


def do_ht(parms):  # "qb/ht"  # "ht"  # FIXME: show 2/9th of screen at head, 1/9th tail
    r"""sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    shline = r"sed -n -e '1,{}p;{},{}s/.*/&\n.../p;$p'".format(
        thirdrows - 1, thirdrows, thirdrows
    )

    byo.exit_if_rare_parms("ht", parms=parms)

    exit_after_shline(shline)


def do_m(parms):  # "qb/m"  # "m"
    """make --"""

    exit_after_shverb_shparms("make --", parms=parms)


def do_mo(parms):  # "qb/mo"  # "mo"
    """less -FIRX"""

    exit_after_shverb_shparms("less -FIRX", parms=parms)


def do_n(parms):  # "qb/n"  # "n"
    """cat -n -tv - |expand"""

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-n")
        options.append("-tv")
    if not words:
        words.append("-")

    argv = ["cat"] + options + seps + words

    shline = byo.shlex_djoin(argv)
    shpipe = "{} |expand".format(shline)

    exit_after_shpipe(shpipe)


def do_pbc(parms):  # "qb/pbc"  # "pbc"
    """(echo "$1"; echo "$2"; ...) |pbcopy"""

    for parm in parms:
        qparm = byo.shlex_dquote(parm)
        if parm == r"export PS1='\$ '":  # todo: generalise how to quote such well
            qparm = '"' + r"export PS1='\\$ '" + '"'
        byo.stderr_print("+ echo {}".format(qparm))

    ichars = ""  # no lines
    if parms:
        ichars = "\n".join(parms) + "\n"  # one or more closed lines
    ibytes = ichars.encode()

    subprocess.run("pbcopy".split(), input=ibytes, check=True)

    # macOS says "pb" means Os Copy/Paste Buffer, but sadly many people disagree
    # so we can work "pbp" and "pbc" as abbreviations of "pbpaste" and "pbcopy"


def do_q(parms):  # "qb/q"  # "q"
    """git checkout"""

    exit_after_shparms("git checkout", parms=parms)


def do_s(parms):  # "qb/s"  # "s"
    """sort -"""

    exit_after_shparms("sort -", parms=parms)


def do_sp(parms):  # "qb/sp"  # "sp"  # FIXME: expand 'sponge.py' inline here
    """sponge.py --"""

    exit_after_shparms("sponge.py --", parms=parms)


def do_t(parms):  # "qb/t"  # "t"
    """tail -16  # or whatever a third of the screen is"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["tail"] + options + seps + words
    shline = byo.shlex_djoin(argv)

    exit_after_shline(shline)


def do_u(parms):  # "qb/u"  # "u"
    """uniq -c - |expand"""

    exit_after_shverb_shparms("uniq -c - |expand", parms=parms)


def do_v(parms):  # "qb/v"  # "v"
    """vim"""

    if not parms:  # a la 'byo.exit_if_testdoc'

        print()
        print("ls |vi -  # fills Vi with Pipe")
        print()

        sys.exit(0)  # exits 0 after printing Help Lines

    exit_after_shparms("vim", parms=parms)


def do_wcl(parms):  # "qb/wcl"  # "wcl"
    """wc -l"""

    exit_after_shverb_shparms("wc -l", parms=parms)


def do_x(parms):  # "qb/x"  # "x"
    """hexdump -C"""

    exit_after_shverb_shparms("hexdump -C", parms=parms)


def do_xa(parms):  # "qb/xa"  # "xa"
    """xargs -n 1"""

    exit_after_shverb_shparms("xargs -n 1", parms=parms)


def do_xp(parms):  # "qb/xp"  # "xp"
    """expand"""

    exit_after_shparms("expand", parms=parms)


#
# Edit the Os Copy/Paste Buffer
#


def pbedit(parms):
    """Call on Vi to edit a Pipe Byte Stream, or on a chosen Editor"""

    # Take 'usage: shpipes.py -- VERB [WORD ...]' as the Editor, else fallback to 'vi'

    vi_argv_minus = parms
    if parms in ([], ["--"]):
        vi_argv_minus = shlex.split("vi")

    # Authorize the leak of one Temporary File (commonly left in "/tmp" till Os Restart)

    byo.stderr_print("+ F=$(mktemp)")

    run = subprocess.run(
        shlex.split("mktemp"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True
    )

    stdout = run.stdout.decode()
    lines = stdout.splitlines()
    assert len(lines) == 1, lines

    mktemp_path = lines[-1]

    # Sponge up Stdin for a Pipe, else sponge up the Os Copy/Paste Buffer

    ibytes = stdin_load("pbpaste >$F")
    with open(mktemp_path, "ab") as writing:
        writing.write(ibytes)

    # Edit the File

    vi_argv = vi_argv_minus + [mktemp_path]

    vi_shline_minus = byo.shlex_djoin(vi_argv_minus)
    byo.stderr_print("+ {} $F".format(vi_shline_minus))

    subprocess.run(vi_argv, check=True)

    # Dump into Stdout for a Pipe, else into the Os Copy/Paste Buffer

    with open(mktemp_path, "rb") as reading:
        obytes = reading.read()

    obytelines = obytes.splitlines()
    byo.stderr_print(
        "... {} bytes of {} lines ...".format(len(obytes), len(obytelines))
    )

    stdout_dump(obytes, shline="cat $F |pbcopy")

    # Race to destroy the Edited File, rather than leaking it

    byo.stderr_print("+ rm $F")

    os.remove(mktemp_path)


def stdin_load(shline="pbpaste"):
    """Sponge up Stdin for a Pipe, else sponge up the Os Copy/Paste Buffer"""

    if not sys.stdin.isatty():
        with open("/dev/stdin", "rb") as reading:
            ibytes = reading.read()
    else:
        byo.stderr_print("+ {}".format(shline))
        run = subprocess.run(
            "pbpaste", stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True
        )
        ibytes = run.stdout

    return ibytes


def stdout_dump(obytes, shline="pbcopy"):
    """Dump into Stdout for a Pipe, else into the Os Copy/Paste Buffer"""

    if not sys.stdout.isatty():
        with open("/dev/stdout", "wb") as writing:
            writing.write(obytes)
    else:
        byo.stderr_print("+ {}".format(shline))
        subprocess.run("pbcopy", input=obytes, check=True)


#
# Forward Parms into a Sh Subprocess and exit
#


def exit_after_shverb_shparms(shline, parms):
    """Drop default Parms when given Options or Seps"""

    shverb = shline.split()[0]

    # Forward the Parms unless Options or Seps given

    (options, seps, words) = byo.shlex_parms_partition(parms)
    if not (options or seps):

        exit_after_shparms(shline, parms=parms)

    # Forward no Parms, in particular not the Seps, when no Options and no Words given

    if (not options) and (not words):

        exit_after_shline(shline=shverb)

    # Else forward all the Parms but onto the ShVerb, without the rest of the ShLine

    exit_after_shparms(shline=shverb, parms=parms)


# todo: merge with 'shpipe.exit_after_weak_shparms'
def exit_after_shparms(shline, parms):
    """Forward Parms into a Sh Subprocess - trace, call,and exit"""

    shparms = byo.shlex_djoin(parms)

    # Pick a RIndex of the ShLine to forward Parms into

    marks = ["", " |", " <", " >"]

    rindices = list()
    for mark in marks:
        find = shline.find(mark)
        if find >= 0:
            rindex = shline.rindex(mark)
            rindices.append(rindex)

    rindex = min(rindices)  # places the Parms inside the ShLine, else past its End

    # Forward the Parms

    parmed = shline
    if parms:
        if rindex < len(shline):
            parmed = shline[:rindex] + " " + shparms + shline[rindex:]
        else:
            parmed = shline + " " + shparms

    if rindex != len(shline):
        exit_after_shpipe(shpipe=parmed)
    else:
        exit_after_shline(shline=parmed)


def exit_after_shline_to_tty(shline):
    """Paginate the output, when it's dumping to Tty"""

    shpipe = "{} |less -FIRX".format(shline)
    if sys.stdout.isatty():

        exit_after_shpipe(shpipe)

    else:

        exit_after_shline(shline)


def exit_after_shpipe(shpipe):
    """Trace and run one ShPipe, then exit"""

    shline = shpipe.rstrip()  # such as a ShPipe ending in "\n"
    shshline = "bash -c {}".format(shlex.quote(shline))
    argv = shlex.split(shshline)

    exit_after_shline_as_argv(shline=shpipe, argv=argv)  # not '(shshline,'


def exit_after_shline(shline):
    """Trace and run one ShLine, then exit"""

    argv = shlex.split(shline)

    exit_after_shline_as_argv(shline, argv=argv)


def exit_after_shline_as_argv(shline, argv):
    """Trace as ShLine but run as ArgV, then exit"""

    # Collect context  # todo: weakly focuses on first command before '|'

    alt_argv = shlex.split(shline)
    alt_argv = list(_ for _ in alt_argv if not re.match("^[0-9]*[<>]", string=_))

    shverb = alt_argv[0]

    stdin_ispipe = not sys.stdin.isatty()
    tty_prompt_pair = form_tty_prompt_pair(stdin_ispipe, shline=shline, shverb=shverb)
    stdin_ispb = judge_stdin_ispb(
        shline, alt_argv=alt_argv, tty_prompt_pair=tty_prompt_pair
    )
    shverb = alt_argv[0]

    # Choose Stdin and print the Code

    index = shline.find(" |")
    index = index if (index >= 0) else len(shline)

    no_stdin_shpipe = shline[:index] + " </dev/null" + shline[index:]
    if shverb == "pbpaste":
        no_stdin_shpipe = shline

    pbpaste_shpipe = "pbpaste |{}".format(shline)

    if stdin_ispipe or tty_prompt_pair:
        byo.stderr_print("+ {}".format(shline))
        stdin = None
    elif not stdin_ispb:
        byo.stderr_print("+ {}".format(no_stdin_shpipe))
        stdin = subprocess.PIPE
    else:
        byo.stderr_print("+ {}".format(pbpaste_shpipe))
        stdin = stdin_demand()

    # Exit zero, when Not authorized to run the Code

    if main.ext is not None:

        sys.exit(0)  # exits 0 after printing Help Lines

    # Run the Code

    if tty_prompt_pair:
        byo.stderr_print(tty_prompt_pair[0])

    try:

        try:
            run = subprocess.run(argv, stdin=stdin)
        except KeyboardInterrupt:
            byo.stderr_print()
            byo.stderr_print("KeyboardInterrupt")

            tty_prompt_pair = None  # mutate

            assert SIGINT_RETURNCODE_130 == 130, SIGINT_RETURNCODE_130

            sys.exit(SIGINT_RETURNCODE_130)  # exits 130 to say KeyboardInterrupt SIGINT

    finally:

        if tty_prompt_pair:
            byo.stderr_print(tty_prompt_pair[-1])

    if run.returncode:  # exits early, at the first NonZero Exit Status ReturnCode
        byo.stderr_print("+ exit {}".format(run.returncode))

        sys.exit(run.returncode)  # passes back a NonZero Exit Status ReturnCode

    sys.exit()  # exits None after this Subprocess


def form_tty_prompt_pair(stdin_ispipe, shline, shverb):
    """Default to run without Tty, but make exceptions"""  # todo: weakly accurate

    entry_prompt = None
    if not stdin_ispipe:
        if shline in ("cat -", "cat - >/dev/null"):
            entry_prompt = "shpipes.py {}: Press ⌃D TTY EOF to quit"
        if shverb in EMACS_SHVERBS:
            entry_prompt = (
                "shpipes.py {}: "
                "Press Esc X revert Tab Return, and ⌃X⌃C, to quit".format(shverb)
            )
        if shverb in VI_SHVERBS:
            entry_prompt = "shpipes.py {}: Press ⇧Z ⇧Q to quit".format(shverb)

    prompt_pair = None
    if entry_prompt:
        exit_prompt = "shpipes.py {}: Congrats, you did escape".format(shverb)
        prompt_pair = (entry_prompt, exit_prompt)

    return prompt_pair


def judge_stdin_ispb(shline, alt_argv, tty_prompt_pair):
    """Choose when to take Stdin from PbPaste"""

    shverb = alt_argv[0]

    (_, _, words) = byo.shlex_parms_partition(alt_argv[1:])

    file_words = words
    file_words = list(_ for _ in file_words if _ not in "- /dev/stdin /dev/tty".split())
    file_words = list(_ for _ in file_words if not (set("{|}") & set(_)))
    if shverb == "grep":  # todo: weakly picks out does Grep have File Parms
        if ("-l" not in shline) and ("-il" not in shline):
            if len(file_words) <= 1:
                file_words = list()
    if shverb == "sed":  # todo: weakly picks out does Sed have File Parms
        file_words = list()

    stdin_ispb = shverb in PBPASTE_SHVERBS
    if file_words or tty_prompt_pair:
        stdin_ispb = False
    if shverb == "grep":  # todo: weakly picks out does Grep have File Parms
        if ("-l" in shline) or ("-il" in shline):
            stdin_ispb = False

    return stdin_ispb


def stdin_demand():
    """Take fast large PbPaste as Stdin, when given slow small Tty people at Stdin"""

    stdin = sys.stdin
    if sys.stdin.isatty():
        pbpaste_argv = shlex.split("pbpaste")
        sub = subprocess.Popen(pbpaste_argv, stdout=subprocess.PIPE)

        stdin = sub.stdout

    return stdin


#
# Exit after calling Subprocess, if dropping the Py Ext Mark finds a Sh Verb
#


def exit_if_shverb(parms):
    """Exit after calling Subprocess, if dropping the Py Ext Mark finds a Sh Verb"""

    argv = parms

    # Find the Executable without Source, else return

    main_py_basename = os.path.basename(argv[0])
    shverb = byo.str_removesuffix(main_py_basename, suffix=".py")
    which = shutil.which(shverb)

    if not which:

        return

    # Refuse to run when found, if Source also required

    if main.ext is not None:
        byo.stderr_print(
            "shpipes.py: ERROR: --ext={!r} missing for shverb:  {}".format(
                main.ext, shverb
            )
        )

        sys.exit(2)  # exits 2 for rare usage

    # Else trace and call and exit

    byo.exit_if_shverb(argv)


#
# Autocomplete & trace, or run, rare fragments of Python
#


def exit_if_rare_autocomplete(shverb, parms):
    """Autocomplete & run the Code & exit, else return"""

    if main.ext is None:
        if not parms:
            if shverb == "dent":
                exit_after_dent()
            elif shverb == "dedent":
                exit_after_dedent()


def exit_after_dent():
    """Insert 4 Spaces to the left of each Line"""

    byo.stderr_print("+ py dent 4")

    with open("/dev/stdin", "rb") as reading:
        with open("/dev/stdout", "wb") as writing:

            for iline in reading.readlines():
                ibytes = iline.splitlines()[0]
                itail = iline[len(ibytes) :]
                ichars = ibytes.decode(errors="surrogateescape")

                ochars = "    " + ichars

                obytes = ochars.encode(errors="surrogateescape")
                writing.write(obytes + itail)

    sys.exit()  # exits None after running auto-complete'd Python


def exit_after_dedent():
    """Delete 4 Spaces at the left of each Line that begins with 4 Spaces"""

    byo.stderr_print("+ py dedent 4")

    with open("/dev/stdin", "rb") as reading:
        with open("/dev/stdout", "wb") as writing:

            for iline in reading.readlines():
                ibytes = iline.splitlines()[0]
                itail = iline[len(ibytes) :]
                ichars = ibytes.decode(errors="surrogateescape")

                ochars = byo.str_removeprefix(ichars, prefix="    ")

                obytes = ochars.encode(errors="surrogateescape")
                writing.write(obytes + itail)

    sys.exit()  # exits None after running auto-complete'd Python


#
# Autocomplete & trace, or run, common fragments of Python
#


def exit_after_autocomplete(parms):
    """Autocomplete & run (or just print) the Code"""

    argv = [main.shverb] + parms

    # Agree to run if Py Source required, but refuse to run if other Source required

    if main.ext is not None:
        if main.ext not in ("", ".py", ".py3"):
            byo.stderr_print(
                "shpipes.py: ERROR: --ext={!r} missing for py: {}".format(
                    main.ext, byo.shlex_djoin(argv) if argv else "--"
                )
            )

            sys.exit(2)  # exits 2 for rare usage

    # Compose Py Source

    pysource = '''
        #!/usr/bin/env python3

        r"""{doc}"""

        with open("/dev/stdin", "rb") as reading:
            with open("/dev/stdout", "wb") as writing:

                for iline in reading.readlines():
                    ibytes = iline.splitlines()[0]
                    itail = iline[len(ibytes): ]
                    ichars = ibytes.decode()

                    ochars = ichars

                    obytes = ochars.encode()
                    writing.write(obytes + itail)
    '''

    pysource = textwrap.dedent(pysource)

    doc = "Run Py Code autocompleted by:  {}".format(byo.shlex_djoin(sys.argv))
    pysource = pysource.format(doc=doc)
    # todo: abbreviate sys.argv[0] to home path
    # todo: expand '--ext=' to an explicit '--ext=.py'

    # Patch up Py Source, so as to autocomplete the argv

    byo.stderr_print("+ ... {} ...".format(byo.shlex_djoin(argv)))

    if True:
        if len(argv) == 1:
            parm = argv[-1]
            if (parm in dir(str)) and not parm.startswith("_"):
                pysource = pysource.replace(
                    """ochars = ichars""", """ochars = str.{}(ichars)""".format(parm)
                )

    # Print Help Lines and exit, if not authorized to run

    if main.ext is not None:
        byo.stderr_print("{}".format(pysource))

        raise NotImplementedError(
            "todo: trace unabbreviated Python", main.shverb, parms
        )

        sys.exit(0)  # exits 0 after printing Help Lines

    # Else run and exit

    if True:

        raise NotImplementedError("todo: run unabbreviated Python", main.shverb, parms)

        exec(pysource)

    else:

        with open("/dev/stdin", "rb") as reading:
            with open("/dev/stdout", "wb") as writing:

                for iline in reading.readlines():
                    ibytes = iline.splitlines()[0]
                    itail = iline[len(ibytes) :]
                    ichars = ibytes.decode()

                    ochars = str.upper(ichars)

                    obytes = ochars.encode()
                    writing.write(obytes + itail)

    sys.exit()  # exits None after running Code


#
# Track some example Terminal Sh input lines
#


_ = """

python3 -c 'import this' |tail -n +3 |cv
cv |wcl

cv |t -1
cv h -3
cv
cv --
cv upper

"""


# FIXME: stop 'cv split' from meaning empty-the-paste-buffer


#
# Track a resulting Sh Terminal Sh transcript
#


_ = """

% python3 -c 'import this' |tail -n +3 |cv
+ pbcopy
% cv |wcl
      19
%

% cv |t -1
+ pbpaste
+ tail -1

Namespaces are one honking great idea -- let's do more of those!

%

% cv h -3
+ pbpaste
+ head -3
+ pbcopy
% cv

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.

%

% cv --
+ pbpaste |cat -n tv |expand

     1  Beautiful is better than ugly.
     2  Explicit is better than implicit.
     3  Simple is better than complex.

%

% cv h -1
+ pbpaste
+ head -1
+ pbcopy
%

% cv tr -d '.'
+ pbpaste
+ tr -d '.'
+ pbcopy
%

% cv upper
+ pbpaste
+ python3 -c '... _ = upper(_) ...'
+ pbcopy
%

% cv
+ pbpaste

BEAUTIFUL IS BETTER THAN UGLY

%

"""


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


#
# ToDo Txt for ShPipes Py
#

# todo: capture of 'cv >...' should report 'wc -l'

# todo: whole word match wins over partial, such as across:  strip lstrip rstrip
# todo: part word match doesn't force left match, such as:  dent dedent exdent indent

# todo: cv spill
# to inject line-break's well
# such as http://api?k1=v1&k2=v2

# FIXME: take each Arg of 'g...' as list of '-e' REGEX to Logical-Or, up to '--'
# todo: define qg algorithmically
# todo: fan out as full 32 inside:  echo qbin/qg{v,}{l,}{w,}{i,}{n,}
# todo: ditto via 'git.py' as full 32 inside:  echo qb/g{v,}{l,}{w,}{i,}{n,}

#  make more dry runs work, some do work now
#
#       % c --ext
#       ('+ cat - >/dev/null',)
#       %
#


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/shpipes.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
