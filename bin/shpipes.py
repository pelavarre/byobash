#!/usr/bin/env python3

r"""
usage: shpipes.py [--help] VERB [ARG ...]

compose a graph of pipes of shverb's

positional arguments:
  VERB    choice of Alias to expand
  ARG     choice of Options and Positional Args to run in place of defaults

options:
  --help  show this help message and exit

quirks:
  dumps larger numbers of Lines into taller Screens, as defaults of:  head/tail -...
  limits Diff and Find like Sh should, by way of the 'less -FIRX' Paginator
  calls 'make --' even for Make's that can't distinguish 'make --' from 'make'
  lets Linux Terminal Stdin echo ⌃D TTY EOF as '', vs macOS as '^D', all without '\n'

slang:
  sends Cat '--show-tabs --show-nonprinting' as '-tv'
  sends Diff '--ignore-space-change --recursive --show-c-function -unified' as '-brpu'
  sends HexDump '-C', as such, to show "Canonical" Hex+Char, not just Hex
  sends Emacs ' --no-window-system ' as ' -nw '
  sends Uniq '--count' as '-c'
  sends Wc '--lines' as '-l'

advanced bash install:

  source qb/env-path-append.source  # define 'c', 'cv', 'd', 'g', 'gi', and so on
  bash qb/env-path-append.source  # show how it works
  export PATH="${PATH:+$PATH:}~/Public/byobash/qb"  # get it done yourself

  shpipes.py cv  # pbpaste |...
  shpipes.py cv  # ... |pbcopy
  shpipes.py cv  # ... |tee >(pbcopy) |...

examples:

  shpipes.py  # show these examples and exit
  shpipes.py --h  # show this help message and exit
  shpipes.py --  # todo: run as you like it

  shpipes.py cv --  # pbpaste |cat -ntv |expand
  shpipes.py cv -etv  # pbpaste |cat -etv |expand

  shpipes.py c |  # cat - |
  shpipes.py |c  # |cat -ntv |expand
  shpipes.py |cv  # pbcopy
  shpipes.py |cv |  # |tee >(pbcopy) |

  shpipes.py a  # awk -F' ' '{print $NF}'  # a, a SEP, a INDEX, a SEP INDEX, etc
  shpipes.py c  # cat - >/dev/null
  shpipes.py cv  # pbpaste
  shpipes.py d  # diff -brpu A_FILE B_FILE |less -FIRX  # default A_FILE='a', B_FILE='b'
  shpipes.py e  # emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipes.py em  # emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipes.py f  # find . -not -type d -not -path './.git/*' |less -FIRX  # Mac needs .
  shpipes.py g  # grep -i .
  shpipes.py gi  # shpipes.py g --  # grep .  # without '-i'
  shpipes.py gl  # grep -ilR
  shpipes.py gli  # shpipes.py gl --  # grep -lR  # without '-il'
  shpipes.py h  # head -16  # or whatever a third of the screen is
  shpipes.py hi  # history  # but include the '~/.bash_histories/' dir
  shpipes.py ht  # sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'  # Head and also Tail
  shpipes.py m  # make --
  shpipes.py mo  # less -FIRX
  shpipes.py n  # cat -ntv -| expand
  shpipes.py p  # popd
  shpipes.py q  # git checkout
  shpipes.py s  # sort -
  shpipes.py sp  # sponge.py --
  shpipes.py t  # tail -16  # or whatever a third of the screen is
  shpipes.py u  # uniq -c -| expand
  shpipes.py v  # vim -
  shpipes.py w  # wc -l
  shpipes.py x  # hexdump -C
  shpipes.py xp  # expand
"""


import __main__
import pdb
import re
import shlex
import subprocess
import sys

import byotools as byo

_ = pdb


def main():
    """Run from the Sh Command Line"""

    parms = sys.argv[1:]
    func_by_verb = form_func_by_verb()

    # Take 'shpipes.py', 'shpipes.py --h', 'shpipes.py --he', ... 'shpipes.py --help'

    byo.exit_via_testdoc()  # shpipes.py
    byo.exit_via_argdoc()  # shpipes.py --help

    assert parms

    # Take 'shpipes.py --'

    if parms == ["--"]:
        sys.stderr.write("NotImplementedError: 'cv --' to mean:  cv |wc\n")
        sys.stderr.write("NotImplementedError: 'cv --' to mean:  cv |vi.py - |cv\n")

        sys.exit(2)  # Exit 2 for wrong usage

    # Take many brutally cryptic abbreviations of ShVerb's

    shverb = parms[0]
    if shverb in func_by_verb.keys():
        func = func_by_verb[shverb]

        __main__.main.sponge_shverb = None
        if hasattr(func, "tty_sponge"):
            __main__.main.sponge_shverb = shverb

        func()  # these Func's mostly now exit here

    # Default to forward the Parms into a Git Subprocess

    byo.exit_via_shcommand()


#
# Wrap many many Shim's around Sh Pipe's
#


def form_func_by_verb():
    """Declare the Pipe Filter Abbreviations"""

    func_by_verb = dict(
        a=do_a,
        c=do_c,
        cv=do_cv,
        d=do_d,
        e=do_e,
        em=do_em,
        f=do_f,
        g=do_g,
        gi=do_gi,
        gli=do_gli,
        gl=do_gl,
        h=do_h,
        hi=do_hi,
        ht=do_ht,
        m=do_m,
        mo=do_mo,
        n=do_n,
        p=do_p,
        q=do_q,
        s=do_s,
        sp=do_sp,
        t=do_t,
        u=do_u,
        v=do_v,
        w=do_w,
        x=do_x,
        xp=do_xp,
    )

    do_a.tty_sponge = True
    do_c.tty_sponge = True
    do_g.tty_sponge = True
    do_gi.tty_sponge = True
    do_h.tty_sponge = True
    do_mo.tty_sponge = True
    do_n.tty_sponge = True
    do_s.tty_sponge = True
    do_sp.tty_sponge = True
    do_t.tty_sponge = True
    do_u.tty_sponge = True
    do_w.tty_sponge = True
    do_x.tty_sponge = True
    do_xp.tty_sponge = True

    return func_by_verb


def do_a():
    """awk -F' ' '{print $NF}'  # a, a SEP, a INDEX, a SEP INDEX, etc"""

    parms = sys.argv[2:]

    # Pick out a Sep, or an Index, both, or neither, from the Parms, if Parms

    if not parms:

        exit_via_shline("awk '{print $NF}'")

    elif len(parms) == 1:

        if re.match(r"^[-+]?[0-9]+$", string=parms[0]):
            (sep, index) = (None, parms[0])
        else:
            (sep, index) = (parms[0], "NF")

    elif len(parms) == 2:

        (sep, index) = parms

    else:

        exit_via_shparms("awk '{print $NF}'")

    # Forward just an Index, else a Sep and an Index

    if sep is None:
        exit_via_shline("awk '{{print {}}}'".format(index))
    else:
        shsep = byo.shlex_dquote(sep)
        exit_via_shline("awk -F{} '{{print ${}}}'".format(shsep, index))


def do_c():
    """cat - >/dev/null"""

    parms = sys.argv[2:]
    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    if parms:
        exit_via_shparms("cat")
    else:
        if stdin_isatty and stdout_isatty:
            exit_via_shparms("cat - >/dev/null")
        elif not stdin_isatty:
            exit_via_shpipe("cat -ntv |expand")
        else:
            exit_via_shparms("cat -")


def do_cv():
    """pbpaste inside tty, pbpaste from tty, pbcopy to tty, else tee to pbcopy"""

    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    if stdin_isatty and stdout_isatty:
        do_cv_tty()  # pbpaste, except 'cv --' => pbpaste |cat -ntv |expand
    elif stdin_isatty:
        exit_via_shparms("pbpaste")  # pbpaste |...
    elif stdout_isatty:
        exit_via_shparms("pbcopy")  # ... |pbcopy
    else:
        exit_via_shparms("tee >(pbcopy)")  # ... |tee >(pbcopy) |...


def do_cv_tty():
    """pbpaste, except 'cv --' => pbpaste |cat -ntv |expand"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if seps and not options:
        options = ["-ntv"]
        seps = []

    argv = ["cat"] + options + seps + args
    if not (options or seps or args):

        exit_via_shline(shline="pbpaste")

    else:

        shpipe = " ".join(byo.shlex_dquote(_) for _ in argv)
        shpipe = "pbpaste |{} |expand".format(shpipe)
        exit_via_shpipe(shpipe)


def do_d():
    """diff -brpu a b |less -FIRX"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-brpu")
    if len(args) < 2:
        args.insert(0, "a")
    if len(args) < 2:
        args.append("b")

    argv = ["diff"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline_shpipe_to_tty(shline)


def do_e():
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    sys.stderr.write("shpipes.py e: Press Esc X revert Tab Return, and ⌃X⌃C, to quit\n")

    exit_via_shparms("emacs -nw --no-splash --eval '(menu-bar-mode -1)'")


def do_em():
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    sys.stderr.write("shpipes.py e: Press Esc X revert Tab Return, and ⌃X⌃C, to quit\n")

    exit_via_shparms("emacs -nw --no-splash --eval '(menu-bar-mode -1)'")


def do_f():
    """find . -not -type d -not -path './.git/*' |less -FIRX"""  # Mac Find needs '.'

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not args:
        args.append(".")  # Mac Find needs an explicit '.'
    if not (options or seps):
        options = ["-not", "-type", "d", "-not", "-path", "./.git/*"]

    argv = ["find"] + args + options + seps  # classic Find takes Args before Options
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline_shpipe_to_tty(shline)


# todo: compact 'def do_g', 'def do_gi', 'def do_gl', 'def do_gli' into 1 Def, not 4
def do_g():
    """grep -i ."""

    parms = sys.argv[2:]
    stdout_isatty = sys.stdout.isatty()

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options = "-i".split()
        if stdout_isatty:
            options.append("--color=yes")
    if not args:
        args = ["."]

    argv = ["grep"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_gi():
    """grep ."""

    parms = sys.argv[2:]
    stdout_isatty = sys.stdout.isatty()

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        # options = "-i".split()  # no
        if stdout_isatty:
            options.append("--color=yes")
    if not args:
        args = ["."]

    argv = ["grep"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_gl():
    """grep -ilR"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options = "-ilR".split()

    argv = ["grep"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_gli():
    """grep -lR"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options = "-lR".split()

    argv = ["grep"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_h():
    """head -16  # or whatever a third of the screen is"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["head"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_hi():
    """history  # but include the files at the '~/.bash_histories/' dir"""

    raise NotImplementedError()


def do_ht():
    r"""sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'"""

    shline = r"sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'"

    exit_via_shline(shline)


def do_m():
    """make --"""

    parms = sys.argv[2:]
    if not parms:
        exit_via_shparms("make --")
    else:
        exit_via_shparms("make")


def do_mo():
    """less -FIRX"""

    exit_via_shparms("less -FIRX")


def do_n():
    """cat -ntv |expand"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-ntv")

    argv = ["cat"] + options + seps + args

    shline = " ".join(byo.shlex_dquote(_) for _ in argv)
    shline = "{} |expand".format(shline)

    exit_via_shpipe(shpipe=shline)


def do_p():
    """popd"""

    exit_via_shparms("popd")


def do_q():
    """git checkout"""

    exit_via_shparms("git checkout")


def do_s():
    """sort"""

    exit_via_shparms("sort")


def do_sp():
    """sponge.py --"""

    exit_via_shparms("sponge.py --")


def do_t():
    """tail -16  # or whatever a third of the screen is"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_parms_partition(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["tail"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_u():
    """uniq -c - |expand"""

    exit_via_shparms("uniq -c - |expand")


def do_v():
    """vim"""

    sys.stderr.write("shpipes.py e: Press ⇧Z ⇧Q to quit\n")

    exit_via_shparms("vim")


def do_w():
    """wc -l"""

    exit_via_shparms("wc -l")


def do_x():
    """hexdump -C"""

    exit_via_shparms("hexdump -C")


def do_xp():
    """expand"""

    exit_via_shparms("expand")


#
# Forward Parms into a Bash Subprocess and exit
#


def exit_via_shparms(shline):
    """Forward Parms into a Bash Subprocess and exit"""

    parms = sys.argv[2:]
    shparms = " ".join(byo.shlex_dquote(_) for _ in parms)

    # Pick a RIndex of the ShLine to forward Parms into

    marks = ["", " |", " <", " >"]

    rindices = list()
    for mark in marks:
        find = shline.find(mark)
        if find >= 0:
            rindex = shline.rindex(mark)
            rindices.append(rindex)

    rindex = min(rindices)  # Place the Parms inside the ShLine, else at its End

    # Forward the Parms

    parmed = shline
    if parms:
        if rindex < len(shline):
            parmed = shline[:rindex] + " " + shparms + shline[rindex:]
        else:
            parmed = shline + " " + shparms

    if rindex != len(shline):
        exit_via_shpipe(shpipe=parmed)
    else:
        exit_via_shline(shline=parmed)


def exit_via_shline_shpipe_to_tty(shline):
    """Exit after running inside a Paginator if Stdout Tty, else exit after running"""

    shpipe = "{} |less -FIRX".format(shline)
    if sys.stdout.isatty():

        exit_via_shpipe(shpipe)

    else:

        exit_via_shline(shline)


def exit_via_shpipe(shpipe):
    """Exit after running a line of Sh marked up with r"[|<>$!]" etc"""

    exit_via_shline(shline=shpipe, shell=True)


def exit_via_shline(shline, shell=False):
    """Exit after running a line of Sh"""

    sys.stderr.write("+ {}\n".format(shline))

    isatty = sys.stdin.isatty()
    if __main__.main.sponge_shverb:
        if isatty:
            sys.stderr.write(
                "shpipes.py {!r}: Press ⌃D TTY EOF to quit\n".format(main.sponge_shverb)
            )

    if not shell:
        argv = shlex.split(shline)
    else:
        shshline = "bash -c {}".format(shlex.quote(shline))
        argv = shlex.split(shshline)

    run = subprocess.run(argv)
    if run.returncode:  # Exit early, at the first NonZero Exit Status ReturnCode
        sys.stderr.write("+ exit {}\n".format(run.returncode))

        sys.exit(run.returncode)

    sys.exit()


#
# Track an example Terminal Qb ShPipes Transcript
#


_ = """

%
%
% python3 -c 'import this' |h -5 |cv
+ pbcopy
+ head -5
%
% cv |sed -n -e '3,$p' |sed 's,[.]$,,' |cv
+ pbpaste
+ pbcopy
%
% cv --
+ bash -c 'pbpaste |cat -ntv |expand'
     1  Beautiful is better than ugly
     2  Explicit is better than implicit
     3  Simple is better than complex
%
%
% cv |t -2
+ pbpaste
+ tail -2
Explicit is better than implicit
Simple is better than complex
%

"""


# FIXME: shpipes.py bash lstrip  # per line, translate Py Label to Sed
# FIXME: shpipes.py bash rstrip  # per line, translate Py Label to Sed
# FIXME: shpipes.py bash strip  # per line, translate Py Label to Sed

# FIXME: shpipes.py ...  # edit the Os Copy/Paste Clipboard, else Stdio, never Tty
# FIXME: shpipes.py lstrip  # per line
# FIXME: shpipes.py "\n".join  # sponges
# FIXME: shpipes.py textwrap.dedent  # joins and splits
# FIXME: shpipes.py enumerate  # numbers
# FIXME: shpipes.py splitlines "-".join  # joins chars of lines


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://.com/pelavarre/byobash/blob/main/bin/shpipes.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
