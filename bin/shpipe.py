#!/usr/bin/env python3


r"""
usage: shpipe.py [--help] PIPE_VERB [ARG ...]

compose a graph of pipes of shverb's

positional arguments:
  PIPE_VERB  choice of ShVerb
  ARG        choice of Options and Arguments

options:
  --help     show this help message and exit

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

  source qb/env-path-append.source  &&: define 'c', 'cv', 'd', 'g', 'gi', and so on
  bash qb/env-path-append.source  &&: show how it works
  export PATH="${PATH:+$PATH:}~/Public/byobash/qb"  &&: get it done yourself

examples:

  shpipe.py  &&: show these examples and exit
  shpipe.py --h  &&: show this help message and exit
  shpipe.py --  &&: todo: run as you like it

  shpipe.py g --  &&: run Grep without options, not even our default '-i'

  shpipe.py c  &&: cat - >/dev/null
  shpipe.py cv  &&: pbpaste
  shpipe.py cv  &&: pbpaste ,...
  shpipe.py cv  &&: ... ,pbcopy
  shpipe.py cv  &&: ... ,tee >(pbcopy) ,...
  shpipe.py cv --  &&: pbpaste ,cat -ntv ,expand
  shpipe.py d  &&: diff -brpu A_FILE B_FILE |less -FIRX  &&: default 'diff -brpu a b'
  shpipe.py e  &&: emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipe.py em  &&: emacs -nw --no-splash --eval '(menu-bar-mode -1)'
  shpipe.py f  &&: find . -not -type d -not -path './.git/*' |less -FIRX  &&: Mac needs .
  shpipe.py g  &&: grep  &&: default 'grep -i'
  shpipe.py h  &&: head -16  &&: or whatever a third of a screen is
  shpipe.py hi  &&: history  &&: but include the files at the '~/.bash_histories/' dir
  shpipe.py ht  &&: sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'  &&: Head and also Tail
  shpipe.py m  &&: make --
  shpipe.py mo  &&: less -FIRX
  shpipe.py n  &&: cat -ntv -, expand
  shpipe.py p  &&: popd
  shpipe.py q  &&: git checkout
  shpipe.py s  &&: sort -
  shpipe.py sp  &&: sponge.py --
  shpipe.py t  &&: tail -16  &&: or whatever a third of a screen is
  shpipe.py u  &&: uniq -c -, expand
  shpipe.py v  &&: vim -
  shpipe.py w  &&: wc -l
  shpipe.py x  &&: hexdump -C
  shpipe.py xp  &&: expand
"""


import os
import pdb
import shlex
import subprocess
import sys

import byotools as byo

_ = pdb


def main():
    """Run from the Sh Command Line"""

    parms = sys.argv[1:]
    func_by_verb = form_func_by_verb()

    # Define some forms of 'shpipe.py'

    byo.exit_via_testdoc()  # shpipe.py
    byo.exit_via_argdoc()  # shpipe.py --help

    # Define many brutally cryptic abbreviations of ShVerb's

    shverb = parms[0] if parms else None
    main.prompter = None
    if shverb in func_by_verb.keys():
        func = func_by_verb[shverb]

        if hasattr(func, "prompter"):
            main.prompter = func.prompter

        func()  # these Func's mostly now exit here

    # Default to forward the Parms into a Git Subprocess

    byo.exit_via_shcommand()


#
# Wrap many many Shim's around Bash Pipe Filters
#


def form_func_by_verb():
    """Declare the Pipe Filter Abbreviations"""

    func_by_verb = dict(
        c=do_c,
        cv=do_cv,
        d=do_d,
        e=do_e,
        em=do_em,
        f=do_f,
        g=do_g,
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

    do_c.prompter = True
    do_h.prompter = True
    do_mo.prompter = True
    do_n.prompter = True
    do_s.prompter = True
    do_sp.prompter = True
    do_t.prompter = True
    do_u.prompter = True
    do_w.prompter = True
    do_x.prompter = True
    do_xp.prompter = True

    return func_by_verb


def do_c():
    """cat - >/dev/null"""

    parms = sys.argv[2:]
    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    if parms:
        exit_via_shpipe_shproc("cat")
    else:
        if stdin_isatty and stdout_isatty:
            exit_via_shpipe_shproc("cat - >/dev/null")
        else:
            exit_via_shpipe_shproc("cat -")


def do_cv():
    """pbpaste from tty, pbcopy to tty, else tee to pbcopy"""

    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()

    if stdin_isatty and stdout_isatty:
        do_cv_tty()  # pbpaste, except 'cv --' => pbpaste |cat -ntv |expand
    elif stdin_isatty:
        exit_via_shpipe_shproc("pbpaste")  # pbpaste |...
    elif stdout_isatty:
        exit_via_shpipe_shproc("pbcopy")  # ... |pbcopy
    else:
        exit_via_shpipe_shproc("tee >(pbcopy)")  # ... |tee >(pbcopy) |...


def do_cv_tty():
    """pbpaste, except 'cv --' => pbpaste |cat -ntv |expand"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if seps and not options:
        options = ["-ntv"]
        seps = []

    argv = ["cat"] + options + seps + args
    if not (options or seps or args):

        exit_via_shline(shline="pbpaste")

    else:

        shline = " ".join(byo.shlex_dquote(_) for _ in argv)
        shline = "pbpaste |{} |expand".format(shline)
        shshline = "bash -c '{}'".format(shline)

        exit_via_shline(shline=shshline)


# FIXME: code as exit_via_shline.shell=True, for better traces


def do_d():
    """diff -brpu a b |less -FIRX"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if not (options or seps):
        options.append("-brpu")
    if len(args) < 2:
        args.insert(0, "a")
    if len(args) < 2:
        args.append("b")

    argv = ["diff"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    shshline = "bash -c '{} |less -FIRX'".format(shline)
    if sys.stdout.isatty():
        shshline = "bash -c '{} |less -FIRX'".format(shline)

    exit_via_shline(shline=shshline)


def do_e():
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    exit_via_shpipe_shproc("emacs -nw --no-splash --eval '(menu-bar-mode -1)'")


def do_em():
    """emacs -nw --no-splash --eval '(menu-bar-mode -1)'"""

    exit_via_shpipe_shproc("emacs -nw --no-splash --eval '(menu-bar-mode -1)'")


def do_f():
    """find . -not -type d -not -path './.git/*' |less -FIRX"""  # Mac Find needs '.'

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if not args:
        args.append(".")  # Mac Find needs an explicit '.'
    if not (options or seps):
        options = ["-not", "-type", "d", "-not", "-path", "./.git/*"]

    argv = ["find"] + args + options + seps  # classic Find takes Args before Options
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)
    shshline = 'bash -c "{} |less -FIRX"'.format(shline)

    if sys.stdout.isatty():
        exit_via_shline(shline=shshline)
    else:
        exit_via_shline(shline)


def do_g():
    """grep -i"""

    parms = sys.argv[2:]
    stdout_isatty = sys.stdout.isatty()

    (options, seps, args) = byo.shlex_split_options(parms)
    if not (options or seps):
        options = "-i".split()
        if stdout_isatty:
            options.append("--color=yes")
    if not args:
        args = ["."]

    argv = ["grep"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_h():
    """head -16"""

    thirdrows = 16  # FIXME

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["head"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_hi():
    """history  &&: but include the files at the '~/.bash_histories/' dir"""

    raise NotImplementedError()


def do_ht():
    r"""sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'"""

    shline = r"sed -n -e '1,2p;3,3s/.*/&\n.../p;$p'"

    exit_via_shline(shline)


def do_m():
    """make --"""

    parms = sys.argv[2:]
    if not parms:
        exit_via_shpipe_shproc("make --")
    else:
        exit_via_shpipe_shproc("make")


def do_mo():
    """less -FIRX"""

    exit_via_shpipe_shproc("less -FIRX")


def do_n():
    """cat -ntv |expand"""

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if not (options or seps):
        options.append("-ntv")

    argv = ["cat"] + options + seps + args

    shline = " ".join(byo.shlex_dquote(_) for _ in argv)
    shline = "{} |expand".format(shline)

    shshline = "bash -c '{}'".format(shline)

    exit_via_shline(shline=shshline)


def do_p():
    """popd"""

    exit_via_shpipe_shproc("popd")


def do_q():
    """git checkout"""

    exit_via_shpipe_shproc("git checkout")


def do_s():
    """sort"""

    exit_via_shpipe_shproc("sort")


def do_sp():
    """sponge.py --"""

    exit_via_shpipe_shproc("sponge.py --")


def do_t():
    """tail -16"""

    thirdrows = 16  # FIXME

    parms = sys.argv[2:]

    (options, seps, args) = byo.shlex_split_options(parms)
    if not (options or seps):
        options.append("-{}".format(thirdrows))

    argv = ["tail"] + options + seps + args
    shline = " ".join(byo.shlex_dquote(_) for _ in argv)

    exit_via_shline(shline)


def do_u():
    """uniq -c - |expand"""

    exit_via_shpipe_shproc("uniq -c - |expand")


def do_v():
    """vim"""

    exit_via_shpipe_shproc("vim")


def do_w():
    """wc -l"""

    exit_via_shpipe_shproc("wc -l")


def do_x():
    """hexdump -C"""

    exit_via_shpipe_shproc("hexdump -C")


def do_xp():
    """expand"""

    exit_via_shpipe_shproc("expand")


#
# In the same-same old way, wrap many many Shim's around Bash Pipe Filters
#


def exit_via_shpipe_shproc(shline):
    """Forward Augmented Parms into a Bash Subprocess and exit, else return"""

    parms = sys.argv[2:]
    shparms = " ".join(byo.shlex_dquote(_) for _ in parms)

    # Pick a RIndex of the ShLine to forward Parms into

    marks = ["", " |", " >", " >("]

    rindices = list()
    for mark in marks:
        find = shline.find(mark)
        if find >= 0:
            rindex = shline.rindex(mark)
            rindices.append(rindex)

    rindex = min(rindices)  # Place the Parms inside the ShLine, else at its End

    shell = rindex != len(shline)

    # Forward the Parms

    parmed_shline = shline
    if parms:
        if rindex < len(shline):
            parmed_shline = shline[:rindex] + " " + shparms + shline[rindex:]
        else:
            parmed_shline = shline + " " + shparms

    # Call another layer of Bash for an 'a |c' Pipe, or for 'a |tee >(b) |c' Pipe of Tee

    shshline = "bash -c '{}'".format(parmed_shline)
    alt_shline = shshline if shell else parmed_shline

    # Run a line of Sh and then exit

    exit_via_shline(shline=alt_shline)


def exit_via_shline(shline):
    """Run a line of Sh and then exit"""

    argv = shlex.split(shline)

    sys.stderr.write("+ {}\n".format(shline))

    isatty = sys.stdin.isatty()
    if main.prompter:
        if isatty:
            sys.stderr.write("shpipe.py: Press ⌃D TTY EOF to quit\n")

    sys.stderr = open(os.devnull, "w")
    run = subprocess.run(argv)
    if run.returncode:  # Exit early, at the first NonZero Exit Status ReturnCode
        sys.stderr.write("+ exit {}\n".format(run.returncode))

        sys.exit(run.returncode)

    sys.exit()


#
# Track an example Terminal Qb ShPipe Transcript
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


# FIXME: code '  # ' and ' |' for Bash, convert for Zsh, such as &&: '...'

# FIXME: more concise Traceback at:  shpipe.py --

# FIXME: shpipe bash lstrip  # per line, translate Py Label to Sed
# FIXME: shpipe bash rstrip  # per line, translate Py Label to Sed
# FIXME: shpipe bash strip  # per line, translate Py Label to Sed

# FIXME: shpipe py ...  &&: edit the Os Copy/Paste Clipboard, else Stdio, never Tty
# FIXME: shpipe py lstrip  # per line
# FIXME: shpipe py "\n".join  # sponges
# FIXME: shpipe py textwrap.dedent  # joins and splits
# FIXME: shpipe py enumerate  # numbers
# FIXME: shpipe py splitlines "-".join  # joins chars of lines


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://.com/pelavarre/byobash/blob/main/bin/shpipe.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
