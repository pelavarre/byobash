#!/usr/bin/env python3

# todo:  link to https://git-scm.com/docs
r"""
usage: git.py [--help] VERB [ARG ...]
usage: git.py [--help] --for-shproc SHVERB [ARG ...]
usage: git.py [--help] --for-chdir CDVERB [ARG ...]

work quickly and concisely, over clones of source dirs of dirs of files

positional arguments:
  VERB                 choice of SubCommand
  ARG                  choice of Options and Arguments

options:
  --help               show this help message and exit
  --for-shproc SHVERB  unabbreviate the ShVerb and call on Git to do its work
  --for-chdir CDVERB   print the $(git rev-parse --show-toplevel) to tell Cd where to go

quirks:
  trace the expansion of each ShVerb as it runs, to help people learn by watching
  dumps larger numbers of Lines into taller Screens, as defaults of:  git log -...
  interlocks the most destructive moves by hanging till ⌃D Tty Eof
  classic Git rudely dumps Help & exits via a Code 1 Usage Error, when given no Parms
  Zsh and Bash take '(dirs -p |head -1)', but only Bash takes 'dirs +0'

advanced Bash install:

  source qbin/env-path-append.source  # define 'q', 'qd', 'qlf', 'qs', etc

  function git.py () {
    : : 'Show Git Status, else change the Sh Working Dir, else do other Git Work' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command git.py --for-shproc --
    elif [ "$#" = 1 ] && [ "$1" = "cd" ]; then
      'cd' "$(command git.py --for-chdir $@)" && (dirs -p |head -1)
    else
      command git.py --for-shproc "$@"
    fi
  }

  function qcd () {
    'cd' "$(command git.py --for-chdir cd $@)" && (dirs -p |head -1)
  }

  function --- () {
    command git.py -- --for-shproc --- "$@"
  }

  function +++ () {
    command git.py -- --for-shproc +++ "$@"
  }

  function File () {
    command git.py -- --for-shproc File "$@"
  }

examples:

  git.py  # show these examples and exit
  git.py --h  # show this help message and exit
  git.py --  # git checkout
  command git.py --  # show the Advanced Bash Install of Git Py and exit

  ls ~/.gitconfig
  ls .git/config
  git log -3 --pretty=$'%h "%an" %ae "%ad" "%cn" %ce "%cd" "%s"\n'
  git log -3 --oneline 'HEAD@{45 days ago}'  # Git Time Machine

  # Navigation (~20 aliases)

  git.py cd  # cd $(git rev-parse --show-toplevel)
  git.py co  # git checkout  # the calmest kind of 'git status'
  git.py d  # git diff
  git.py dh  # git diff HEAD~...  # default HEAD~1, without '-b'
  git.py dhno  # git diff --name-only HEAD~..., default HEAD~1
  git.py dno  # git diff --name-only
  git.py em  # qno ... && em $(qno ...)
  git.py g  # grep -i .
  git.py gi  # git grep .  # without '-i'
  git.py gli  # git grep -l .  # without '-i'
  git.py gl  # git grep -il .
  git.py gv  # git grep -v -i .
  git.py gvi  # git grep -v .  # without '-i'
  git.py lf  # git ls-files
  git.py no  # usage: git.py no [EXT | DEPTH|HEAD~...|HASH [EXT]]  # for dno, dhno, spno
  git.py s  # git show
  git.py sp  # git show --pretty=''
  git.py spno  # git show --pretty='' --name-only  # takes HEAD~..., defaults to  HEAD
  git.py sis  # git status --ignored --short  # calmer than 'git status'
  git.py st  # git status
  git.py sun  # git status --untracked-files=no
  git.py vi  # qno ... && vi $(qno ...)

  # Branch and Log Work (~27 aliases)

  git.py b  # git branch  # and see also:  git rev-parse --abbrev-ref
  git.py ba  # git branch --all
  git.py fcorb  # git fetch && git checkout ... && git rebase  # auth w/out ⌃D
  git.py cp  # git cherry-pick
  git.py dad  # git describe --always --dirty
  git.py f  # git fetch
  git.py frb  # git fetch && git rebase  # auth w/out ⌃D
  git.py l  # git log
  git.py l1  # git log --decorate -1
  git.py lg  # git log --oneline --no-decorate --grep ...
  git.py lgg  # git log --oneline --no-decorate -G ...  # grep for touches
  git.py lgs  # git log --oneline --no-decorate -S ...  # grep for adds/ deletes
  git.py lols  # git log --oneline --numstat  # list Files per Commit
  git.py lq  # git log --oneline --no-decorate -...  # default lots, -0 for no limit
  git.py lq0  # git log --oneline --no-decorate
  git.py lq1  # git log --oneline --no-decorate -1
  git.py lq2  # git log --oneline --no-decorate -2
  git.py lq3  # git log --oneline --no-decorate -3
  git.py lqa  # git log --oneline --no-decorate --author=$USER -...
  git.py ls  # git log --numstat  # but see also:  git show --name-only
  git.py lv  # git log --oneline --decorate -...  # default lots, -0 for no limit
  git.py lv0  # git log --oneline --decorate
  git.py lv1  # git log --oneline --decorate -1
  git.py lva  # git log --oneline --decorate --author=$USER -...
  git.py rb  # git rebase
  git.py ri  # git rebase --interactive --autosquash HEAD~...  # else {@upstream}
  git.py rl  # git reflog  # show Commits of Clone, no matter the Branch
  git.py rlv  # git reflog --format=fuller  # show more detail for Commits of Clone
  git.py rpar  # git rev-parse --abbrev-ref  # show the key line of:  git branch
  git.py rpsfn  # git rev-parse --symbolic-full-name  # like show @{-1..N} of 'co -'
  git.py rv  # git remote -v
  git.py ssn  # git shortlog --summary --numbered

  # Commit and Conflict Work (~17 aliases)

  git.py a  # git add
  git.py ap  # git add --patch
  git.py c  # git commit
  git.py ca  # git commit --amend
  git.py caa  # git commit --all --amend
  git.py caf  # git commit --all --fixup
  git.py cam  # git commit --all -m wip
  git.py cf  # git commit --fixup
  git.py cl  # take ⌃D to mean:  git clean -ffxdq  # destroy files outside Git Add
  git.py cls  # take ⌃D to mean:  sudo true && sudo git clean -ffxdq
  git.py cm  # git commit -m wip
  git.py pfwl  # take ⌃D to mean:  git push --force-with-lease
  git.py rh  # take ⌃D to mean:  git reset --hard ...  # hide local Commits
  git.py rhu  # take ⌃D to mean:  git reset --hard @{upstream}  # hide to restart
  git.py s1  # git show :1:...  # common base
  git.py s2  # git show :2:...  # just theirs
  git.py s3  # git show :3:...  # just ours

  # Reroll/Roll your own Repo

  rm -fr g.git git && git init --bare g.git && git clone g.git && cd g
  git rev-list $HASH..$HASH  # exit 0 only if $HASH found in in this Clone

  git push origin HEAD:guests/jqdoe/clients
"""

# FIXME:  these are Aliases of 'git.py --for-shproc', not Aliases of 'git.py'

# todo:  Occasionally Needed Extras: making branches, deleting branches
# todo:  Upkeep of the Slow Clone:  git fetch --tags --force
# todo:  Upkeep of the Slow Clone:  git fetch --prune --prune-tags


import __main__
import collections
import getpass
import glob
import os
import pathlib
import pdb
import re
import shlex
import signal
import subprocess
import sys

import byotools as byo

_ = pdb


DEFAULT_NONE = None

SIGINT_RETURNCODE_130 = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE_130 == 130, (SIGINT_RETURNCODE_130, 0x80, signal.SIGINT)

GitLikeAlias = collections.namedtuple("GitLikeAlias", "shlines authed".split())


#
# Run from the Sh Command Line
#


def main():
    """Run from the Sh Command Line"""

    # Emulate running as a Sh Alias that doesn't write PyC Files

    rm_fr_import_byotools_pyc()

    # Track how to patch a 'git.py cd' into the Memory of the Sh Process

    patchdoc = """

  function git.py () {
    : : 'Show Git Status, else change the Sh Working Dir, else do other Git Work' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command git.py --for-shproc --
    elif [ "$#" = 1 ] && [ "$1" = "cd" ]; then
      'cd' "$(command git.py --for-chdir $@)" && (dirs -p |head -1)
    else
      command git.py --for-shproc "$@"
    fi
  }

  function qcd () {
    'cd' "$(command git.py --for-chdir cd $@)" && (dirs -p |head -1)
  }

  function --- () {
    command git.py -- --for-shproc --- "$@"
  }

  function +++ () {
    command git.py -- --for-shproc +++ "$@"
  }

  function File () {
    command git.py -- --for-shproc File "$@"
  }

    """

    # Take out "--for-shproc" and "--for-chdir" early, and skip over "--"

    sys_parms = sys.argv[1:]
    options = ("--for-chdir", "--for-shproc")

    parms = None
    if sys_parms:
        if sys_parms[0] in options:

            parms = sys_parms[1:]

        elif sys_parms[0] == "--":
            if sys_parms[1:]:
                if sys_parms[1] in options:

                    parms = sys_parms[2:]

        # Define the 'git.py' that isn't 'command git.py'

        if parms is not None:
            if not parms:

                byo.exit_after_testdoc()

            # Define the 'git.py --' that isn't 'command git.py --'

            if parms == ["--"]:

                parms = ["co"]  # "git checkout"
                # FIXME: print counts of 'gsis' as reminders for:  git add

    # Define the most conventional forms of 'git.py'

    byo.exit_if_patchdoc(patchdoc)  # command git.py --
    byo.exit_if_testdoc()  # command git.py
    byo.exit_if_argdoc()  # git.py --help

    # Expand any of many intensely cryptic calls of "--for-chdir" and "--for-shproc"

    if parms:
        shverb = parms[0]

        exit_if_by_shverb(shverb, parms=parms[1:])

    # Default to forward the Parms into a Git Subprocess

    byo.exit_after_shverb()


def exit_if_by_shverb(shverb, parms):
    """Expand any of many intensely cryptic calls of Git Aliases"""

    main.shverb = shverb

    exit_if_funcs_by_shverb = form_exit_if_funcs_by_shverb()
    aliases_by_shverb = form_aliases_by_shverb()

    # For a few ShVerb's, take more context into account

    exit_if_func = exit_if_funcs_by_shverb.get(shverb, DEFAULT_NONE)
    if exit_if_func:

        exit_if_func(parms)

    # Commonly, instantiate a fixed-length template of ShLine's

    alias = aliases_by_shverb.get(shverb, DEFAULT_NONE)
    if alias:
        authed = alias.authed

        shlines = alias.shlines
        if shverb == "cd":
            shlines = ["git rev-parse --show-toplevel"]

            git_cd_shlines = ["cd $(git rev-parse --show-toplevel)"]
            assert alias.shlines == git_cd_shlines, alias.shlines

        exit_if_shproc(shverb, parms=parms, authed=authed, shlines=shlines)

    # Else return to try something else

    return


def rm_fr_import_byotools_pyc():
    """Cancel the Dirt apparently tossed into this Git Clone by Import ByoTools"""

    cwd = os.getcwd()

    bin_dirname = os.path.dirname(byo.__file__)

    byobash_dirname = os.path.join(bin_dirname, os.pardir)
    pyc_dirname = os.path.join(bin_dirname, "__pycache__")
    pyc_glob = os.path.join(pyc_dirname, "byotools.cpython-*.pyc")

    real_cwd = os.path.realpath(cwd)
    real_byobash_dirname = os.path.realpath(byobash_dirname)

    eq = real_cwd == real_byobash_dirname
    startswith = real_cwd.startswith(real_byobash_dirname + os.sep)
    if eq or startswith:

        hits = list(glob.glob(pyc_glob))
        if len(hits) == 1:
            hit = hits[-1]

            os.remove(hit)
            if not os.listdir(pyc_dirname):
                os.rmdir(pyc_dirname)


def exit_if_shproc(shverb, parms, authed, shlines):  # todo  # noqa: C901 complex
    """Copy/edit Parms into Git and exit, else return"""

    rows = byo.shutil_get_tty_height()
    thirdrows = max(3, rows // 3)

    alt_shlines = list(_ for _ in shlines if _ != "cat -")
    alt_parms = parms
    if not parms:

        if alt_shlines == ["git commit --all --fixup {}"]:
            alt_parms = ["HEAD"]
        elif alt_shlines == ["git commit --fixup {}"]:
            alt_parms = ["HEAD"]
        elif alt_shlines == ["git rev-parse --abbrev-ref {}"]:
            alt_parms = ["HEAD"]

    # Distinguish a leading Int parm, without requiring it

    intparm = None
    if alt_parms:

        chars = alt_parms[0]
        if re.match(r"^[-+]?[0-9]+$", string=chars):
            intparm = int(chars)

    if alt_shlines == ["git rebase --interactive --autosquash HEAD~{}"]:
        if not alt_parms:
            alt_shlines = ["git rebase --interactive --autosquash @{{upstream}}"]
        elif intparm is None:
            alt_shlines = ["git rebase --interactive --autosquash {}"]

    #

    parms_minus = alt_parms[1:]
    shparms = byo.shlex_djoin(alt_parms)
    shparms_minus = byo.shlex_djoin(parms_minus)

    # Form each ShLine, and split each ShLine apart into an ArgV

    argvs = list()
    for shline in alt_shlines:

        # At most once, accept a request to forward Parms

        parmed_shline = None

        if "{}" not in shline:

            parmed_shline = shline.format()

        else:

            parmed_shline = shline.format(shparms)

            # Count off 0..N below HEAD, default 1, else take complex Parms

            if shline == "git show --pretty='' --name-only {}":
                if intparm is not None:
                    alt_shline = shline.replace(" {}", " HEAD~{}")
                    parmed_shline = alt_shline.format(intparm, shparms_minus)

            elif " HEAD~{}" in shline:

                if not shparms:
                    parmed_shline = shline.format(1)
                elif intparm is None:
                    alt_shline = shline.replace(" HEAD~{}", " HEAD~{} {}")
                    parmed_shline = alt_shline.format(1, shparms)
                else:
                    absparm = abs(intparm)
                    alt_shline = shline.replace(" HEAD~{}", " HEAD~{} {}")
                    parmed_shline = alt_shline.format(absparm, shparms_minus)

            # Count off 1..N of "git checkout -", default 1, else take complex Parms

            elif " @{{-{}}}" in shline:

                if not shparms:
                    parmed_shline = shline.format(1)
                elif intparm is None:
                    alt_shline = shline.replace(" @{{-{}}}", " @{{-{}}} {}")
                    parmed_shline = alt_shline.format(1, shparms)
                else:
                    absparm = abs(intparm)
                    alt_shline = shline.replace(" @{{-{}}}", " @{{-{}}} {}")
                    parmed_shline = alt_shline.format(absparm, shparms_minus)

            # Count off Lines of Output, default Third Screen, else take complex Parms
            # but take any of '-0', '0', '+0' to mean No Limit Parm

            elif " -{}" in shline:

                if not shparms:
                    parmed_shline = shline.format(thirdrows)
                elif intparm is None:
                    alt_shline = shline.replace(" -{}", " -{} {}")
                    parmed_shline = alt_shline.format(thirdrows, shparms)
                elif intparm == 0:
                    alt_shline = shline.replace(" -{}", " {}")
                    parmed_shline = alt_shline.format(shparms_minus)
                else:
                    absparm = abs(intparm)
                    alt_shline = shline.replace(" -{}", " -{} {}")
                    parmed_shline = alt_shline.format(absparm, shparms_minus)

            # Reject subsequent requests to forward Parms, if any

            shparms = None

        # Fix it up some more and ship it out

        argv_shline = parmed_shline.rstrip()
        if " --author=$USER" in parmed_shline:

            shguest = byo.shlex_dquote(getpass.getuser())
            guest_key = " --author=$USER"
            guest_repl = " --author={}".format(shguest)

            argv_shline = parmed_shline.rstrip().replace(guest_key, guest_repl)

        argv = shlex.split(argv_shline)
        argvs.append(argv)

    # Actually return, actually don't exit, if Parms present but not forwarded

    if shparms:

        return

    # Join the ShLines

    auth_shlines = list()
    for argv in argvs:
        shline = byo.shlex_djoin(argv)

        overquoted = "git reset --hard '@{upstream}'"  # because of the {} Braces
        shline = shline.replace(overquoted, "git reset --hard @{upstream}")

        auth_shlines.append(shline)

    auth_shline = " && ".join(auth_shlines)

    # Demand authorization

    if not authed:
        if auth_shline == "git push --force-with-lease":

            gcue_shline = "git config user.email"
            byo.stderr_print("+ {}".format(gcue_shline))
            gcue_line = byo.subprocess_run_oneline(gcue_shline)
            byo.stderr_print(gcue_line)

            rpar_shline = "git rev-parse --abbrev-ref HEAD"
            byo.stderr_print("+ {}".format(rpar_shline))
            rpar_line = byo.subprocess_run_oneline(rpar_shline)
            byo.stderr_print(rpar_line)
            byo.stderr_print("+")

            guest = gcue_line.split("@")[0]
            if "/{}/".format(guest) not in rpar_line:
                byo.stderr_print(
                    "git.py: {!r} not authorized for Qpfwl at Branch {!r}".format(
                        guest, rpar_line
                    )
                )

                byo.stderr_print("git.py:")
                byo.stderr_print("git.py: did you mean:  {}".format(auth_shline))
                byo.stderr_print("git.py:")

                sys.exit(2)

    if not authed:

        byo.stderr_print("did you mean:  {}".format(auth_shline))
        byo.stderr_print("press ⌃D to execute, or ⌃C to quit")
        try:
            _ = sys.stdin.read()
        except KeyboardInterrupt:
            byo.stderr_print()
            byo.stderr_print("KeyboardInterrupt")

            assert SIGINT_RETURNCODE_130 == 130, SIGINT_RETURNCODE_130

            sys.exit(SIGINT_RETURNCODE_130)  # Exit 130 to say KeyboardInterrupt SIGINT

    # Run each of the ArgV's and exit

    require_cwd_in_clone_if_git_diff(argv=argvs[0])  # duck around 125+ Lines of Error

    byo.exit_after_some_loud_argv(argvs)


def require_cwd_in_clone_if_git_diff(argv):
    """Guard the call, if it's Git Diff, with a check for Cwd is in Clone"""

    if argv[:2] != "git diff".split():

        return

    # Don't risk the guard complexifying results, in the normal case of Git Dir present

    path = pathlib.Path(".git")
    if path.is_dir():

        return

    # Call the guard

    qdno_shline = byo.shlex_djoin(argv)  # such as:  git diff --name-only
    qdno_argv = shlex.split(qdno_shline)

    sys.stdout.flush()
    sys.stderr.flush()

    run = subprocess.run(
        qdno_argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout = run.stdout.decode() if run.stdout else None
    stderr = run.stderr.decode() if run.stderr else None

    # Silence this call and return now, when the guard doesn't fire,
    # such as in the case of running in a Dir beneath the Top Dir of the Clone

    if not run.returncode:

        return

    # Trace the guard firing, but compress the trace

    assert run.returncode, run.returncode  # often 129 of Git Diff, not 128 of Git Log
    assert not stdout, repr(stdout)
    assert stderr, stderr

    byo.stderr_print("+ {}".format(qdno_shline))
    if stdout:
        sys.stdout.write(stdout)
    if stderr:
        errlines = stderr.splitlines()
        len_errlines = len(errlines)
        if len_errlines < 3:
            sys.stderr.write(stderr)
        else:
            byo.stderr_print("\n".join(errlines[:2]))
            byo.stderr_print("... {} more lines ...".format(len_errlines - 2))
            byo.stderr_print("+ exit {}".format(run.returncode))

    sys.stdout.flush()
    sys.stderr.flush()

    sys.exit(run.returncode)


#
# Define Git Alias'es that trace their own meaning, so i still learn over your shoulder
#


def form_aliases_by_shverb():
    """Declare the GitLikeAlias'es, indexed by ShVerb"""

    doc = __main__.__doc__

    # Visit each GitLike Alias

    aliases_by_shverb = dict()
    for (k, v) in ALIASES.items():
        verb = k

        # Declare this GitLike Alias

        shlines = v.split(" && ")
        docline = "git.py {k}  # {v}".format(k=k, v=v)

        alias = GitLikeAlias(shlines, authed=True)
        if "  # cat - && " in docline:
            alias = GitLikeAlias(shlines, authed=None)

        assert verb not in aliases_by_shverb.keys(), repr(verb)

        aliases_by_shverb[verb] = alias

        # Require Alias found, close enough, in Doc
        # todo: Require the DocLine found in full, with only zero or more Comments added

        if docline in doc:

            continue

        docline_twice = docline.format("...", "...")  # no Exception when just 1 "{}"
        if docline_twice in doc:

            continue

        docline_once = docline.format("...")
        if docline_once in doc:

            continue

        parmless_docline = byo.str_removesuffix(docline, " {}")
        if parmless_docline in doc:

            continue

        authed_docline = docline.replace("  # cat - && ", "  # take ⌃D to mean:  ")
        if authed_docline in doc:

            continue

        authed_docline_once = authed_docline.format("...")
        if authed_docline_once in doc:

            continue

        assert False, (k, docline, shlines)

    return aliases_by_shverb


ALIASES = {
    "a": "git add {}",
    "ap": "git add --patch {}",
    "b": "git branch",
    "ba": "git branch --all",
    "c": "git commit {}",
    "ca": "git commit --amend {}",
    "caa": "git commit --all --amend {}",
    "caf": "git commit --all --fixup {}",
    "cam": "git commit --all -m wip",
    "cd": "cd $(git rev-parse --show-toplevel)",
    "cf": "git commit --fixup {}",
    "cl": "cat - && git clean -ffxdq",
    "cls": "cat - && sudo true && sudo git clean -ffxdq",
    "cm": "git commit -m wip",
    "co": "git checkout {}",
    "cp": "git cherry-pick {}",
    "d": "git diff {}",
    "dad": "git describe --always --dirty",
    "dh": "git diff HEAD~{}",  # default HEAD~1, without '-b'
    "dhno": "git diff --name-only HEAD~{}",
    "dno": "git diff --name-only {}",
    "em": "qno {} && em $(qno {})",
    "f": "git fetch",
    "fcorb": "git fetch && git checkout {} && git rebase",  # auth w/out ⌃D
    "frb": "git fetch && git rebase",
    "l": "git log {}",
    "l1": "git log --decorate -1 {}",
    "lf": "git ls-files {}",
    "lg": "git log --oneline --no-decorate --grep {}",
    "lgg": "git log --oneline --no-decorate -G {}",  # touches, aka Grep Source
    "lgs": "git log --oneline --no-decorate -S {}",  # adds/deletes, aka Pickaxe
    "lols": "git log --oneline --numstat {}",
    "lq": "git log --oneline --no-decorate -{}",
    "lq0": "git log --oneline --no-decorate {}",
    "lq1": "git log --oneline --no-decorate -1 {}",
    "lq2": "git log --oneline --no-decorate -2 {}",
    "lq3": "git log --oneline --no-decorate -3 {}",
    "lqa": "git log --oneline --no-decorate --author=$USER -{}",
    "ls": "git log --numstat {}",
    "lv": "git log --oneline --decorate -{}",
    "lv0": "git log --oneline --decorate {}",
    "lv1": "git log --oneline --decorate -1 {}",
    "lva": "git log --oneline --decorate --author=$USER -{}",
    "no": "usage: git.py no [EXT | DEPTH|HEAD~...|HASH [EXT]]",  # for dno, dhno, spno
    "pfwl": "cat - && git push --force-with-lease",
    "rb": "git rebase {}",  # auth w/out ⌃D
    "rh": "cat - && git reset --hard {}",
    "rhu": "cat - && git reset --hard @{{upstream}}",
    "ri": "git rebase --interactive --autosquash HEAD~{}",
    "rl": "git reflog",
    "rlv": "git reflog --format=fuller",
    "rpar": "git rev-parse --abbrev-ref {}",
    "rpsfn": "git rev-parse --symbolic-full-name {}",  # like show @{-1..N} of 'co -'
    "rv": "git remote -v",
    "s": "git show {}",
    "s1": "git show :1:{}",
    "s2": "git show :2:{}",
    "s3": "git show :3:{}",
    "sp": "git show --pretty='' {}",
    "spno": "git show --pretty='' --name-only {}",
    "sis": "git status --ignored --short",
    "ssn": "git shortlog --summary --numbered",
    "st": "git status {}",
    "sun": "git status --untracked-files=no",
    "vi": "qno {} && vi $(qno {})",
}

#
# Git Grep defaults to --color=yes and '-R', and often matches too many lines at '-v'
# 'qlgg' can't be 'qlG' in a Mac HFS FileSystem that has a 'qlg' already
# 'qlgs' can't be 'qlS' in a Mac HFS FileSystem that has a 'qls' already
#


#
# Define some Git Alias'es to take meaning out of Parm's, not just forward Parm's
#


def form_exit_if_funcs_by_shverb():
    """Declare the Exit_If Func's, indexed by ShVerb"""

    exit_if_funcs = dict(
        em=exit_if_em,  # "em"
        g=exit_if_g,  # "g"
        gi=exit_if_gi,  # "gi"
        gl=exit_if_gl,  # "gl"
        gli=exit_if_gli,  # "gli"
        gv=exit_if_gv,  # "gv"
        gvi=exit_if_gvi,  # "gvi"
        no=exit_if_git_no,  # "no"
        rpsfn=exit_if_git_rpsfn,  # "rpsfn"
        vi=exit_if_vi,  # "vi"
    )

    exit_if_funcs["+++"] = exit_if_by_git_stdout_line
    exit_if_funcs["---"] = exit_if_by_git_stdout_line
    exit_if_funcs["File"] = exit_if_by_py_stderr_line
    # todo: coin a ShVerb to take "+++", "---", "File" etc as its first Parm

    return exit_if_funcs


#
# Define some Git Alias'es to take looped-back Std/out/err Lines as Next Steps
#


def exit_if_by_py_stderr_line(parms):  # for ShVerb "File"
    """Take or suggest next action after being fed back a Line of Py Stderr"""

    shverb = main.shverb

    # Receive two Parms from such as:  File "bin/git.py", line 1091, in main

    if (shverb == "File") and (len(parms) >= 1):
        assert parms[0].endswith(","), parms
        assert parms[1] == "line", parms
        assert parms[2].endswith(","), parms
        assert parms[3] == "in", parms
        assert parms[4:], parms

        path = byo.str_removesuffix(parms[0], suffix=",")
        str_lineno = byo.str_removesuffix(parms[2], suffix=",")
        lineno = int(str_lineno)

        _ = lineno  # todo: jump to Line of File

        exit_after_git_edit_path(path)

    # todo: factor out 'def exit_if_by_py_stderr_line' into some other file?


def exit_if_by_git_stdout_line(parms):  # for ShVerbs "+++", "---"
    """Take or suggest next action after being fed back a Line of Git Stdout"""

    shverb = main.shverb

    # Receive one Parm from such as:  --- a/bin/git.py
    # or from such as:  +++ b/bin/git.py

    if (shverb in ("---", "+++")) and (len(parms) == 1):
        prefix = parms[0][:2]
        if prefix in ("a/", "b/"):

            path = parms[0]
            path = byo.str_removeprefix(path, prefix=prefix)

            exit_after_git_edit_path(path)

            # todo: jump to Line of File when given 2 Lines of Paste


def exit_after_git_edit_path(path):  # common to ShVerb's "+++", "---", "File"
    """Forward one Parm into the local Editor"""

    # Form a ShLine to forward the one Parm into the local Editor

    git_config_shline = "git config core.editor"
    byo.stderr_print("+ {}".format(git_config_shline))

    vi_shline = byo.subprocess_run_oneline("git config core.editor")
    vi_shline = vi_shline + " " + byo.shlex_dquote(path)
    vi_argv = shlex.split(vi_shline)

    # Run the Shline

    vi_argv = shlex.split(vi_shline)
    byo.subprocess_run_loud(vi_argv, stdin=None)

    sys.exit()  # Exit None after an ArgV exits Falsey

    # todo: jump to Line of File
    # vi bin/git.py +785
    # emacs -nw --eval '(menu-bar-mode -1)' bin/git.py --eval '(goto-line 785)'


#
# usage: git.py no [EXT | DEPTH|HEAD~...|HASH [EXT]]"  # for dno, dhno, spno
#
# show the tracked files in flight
#
# examples:
#   qno  # 'qdno' else 'qdhno'
#   qno .py  # same as 'qno', but cut back by:  |grep -e '[.]py$'
#   qno py  # short for:  qno .py
#   qno 3  # short for:  qdhno 3
#   qno 3 .txt  # same as 'qno 3', but cut back by:  |grep -e '[.]txt$'
#   qno HEAD  # short for:  qspno HEAD
#   qno HEAD~3  # short for 'qspno HEAD~3', not for 'qdhno HEAD~3'
#   qno abcdef0  # short for 'qspno abcdef0', not for 'qdhno abcdef0'
#   qno abcdef0 .bash  # same as 'qno abcdef0' but cut back by:  |grep -e '[.]bash$'
#


def exit_if_git_no(parms):  # "qno"
    """List the Files of the Git Diff, else of Git Diff HEAD~1, else the EXT there"""

    aliases_by_shverb = form_aliases_by_shverb()

    # Require some synch of 'qno' with 'qdno', 'qdhno', and 'qspno'

    dno_alias = aliases_by_shverb["dno"]
    assert dno_alias.shlines == ["git diff --name-only {}"], dno_alias.shlines
    dhno_alias = aliases_by_shverb["dhno"]
    assert dhno_alias.shlines == ["git diff --name-only HEAD~{}"], dhno_alias.shlines
    spno_alias = aliases_by_shverb["spno"]
    assert spno_alias.shlines == ["git show --pretty='' --name-only {}"]

    # Secretly sample the 'git diff --name-only'

    qd_shline = "git diff --name-only"
    qd_argv = shlex.split(qd_shline)
    require_cwd_in_clone_if_git_diff(argv=qd_argv)
    qd_run = subprocess.run(qd_argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert not qd_run.returncode, qd_run.returncode

    qd_stdout = qd_run.stdout.decode()
    qd_chars = qd_stdout.rstrip()

    # If no Parms, then list the Files of the Git Diff, else of Git Diff HEAD~1

    if not parms:
        if qd_chars:

            exit_if_by_shverb(shverb="dno", parms=list())

        else:

            exit_if_by_shverb(shverb="dhno", parms=list())

    # Take a File Ext as 1 Parm, or as the 2nd of 2 Parms

    parms_0 = parms[0]

    uint_parm = re.match(r"^[0-9]+$", string=parms_0)
    hash_parm = re.match(r"^[0-9A-Fa-f]+$", string=parms_0)
    head_parm = parms_0.startswith("HEAD")

    depth_parm = uint_parm or hash_parm or head_parm

    ext_parm = None
    if len(parms) == 2:
        if depth_parm:
            ext_parm = parms[1]
    elif len(parms) == 1:
        if not depth_parm:
            ext_parm = parms[0]

    # Expand a leading Unsigned Int Parm as a depth below HEAD

    alt_parms = list(parms)
    if uint_parm:
        alt_parms[0] = "HEAD~{}".format(parms_0)

    # Call on "dhno" or "spno" to take Parms given without a chosen Ext

    if not ext_parm:
        if uint_parm:

            exit_if_by_shverb(shverb="dhno", parms=parms)

        else:

            exit_if_by_shverb(shverb="spno", parms=alt_parms)

    # Call on "dno" else ("dhno" or "spno") to take Parms given with a chosen Ext

    exit_if_git_no_ext(
        ext_parm,
        qd_chars=qd_chars,
        depth_parm=depth_parm,
        uint_parm=uint_parm,
        alt_parms=alt_parms,
    )


def exit_if_git_no_ext(ext_parm, qd_chars, depth_parm, uint_parm, alt_parms):
    """List only the Files of EXT found in a Git Diff"""

    # List the Files of the Git Diff, else of Git Diff HEAD~1, else of Chosen Depth

    shline = "git diff --name-only"
    if not qd_chars:
        shline = "git diff --name-only HEAD~1"
    if depth_parm:
        shline = "git diff --name-only {}".format(alt_parms[0])
        if not uint_parm:
            shline = "git show --pretty='' --name-only {}".format(alt_parms[0])

    # Form a Reg Ex to pick out only the Files of the Ext

    ext = ext_parm if ext_parm.startswith(".") else ".{}".format(ext_parm)

    re_ext = re.escape(ext[1:])
    alt_re_ext = r"[.]" + re_ext + r"$"  # simplify to r"[.]" down from "r\."
    sh_alt_re_ext = byo.shlex_dquote(alt_re_ext)

    # List only the Files of the Ext, else exit nonzero

    shpipe = "{} |grep -e {}".format(shline, sh_alt_re_ext)
    shshline = "bash -c {!r}".format(shpipe)
    argv = shlex.split(shshline)

    byo.subprocess_run_loud(argv, shpipe)  # implicit 'stdin=subprocess.PIPE'

    sys.exit()  # Exit None after an ArgV exits Falsey


#
# usage: git.py rpsfn [-DEPTH]
#
# show Branch history below or thru '--abbrev-ref HEAD'
#
# examples:
#   qrpsfn  # git rev-parse --symbolic-full-name @{-1}
#   qrpsfn -1  # git rev-parse --symbolic-full-name HEAD |sed 's,^refs/heads/,,'
#   qrpsfn -3  # git rev-parse --symbolic-full-name ... @{-2} |sed 's,^refs/heads/,,'
#


def exit_if_git_rpsfn(parms):  # "rpsfn"  # distinct from "rpar"
    """List the last Symbolic Full Names through to an Int, else forward Parms"""

    # Require the Alias "rpsfn" defined, same as here, across the ArgDoc and such

    shverb = "rpsfn"

    aliases_by_shverb = form_aliases_by_shverb()

    alias = aliases_by_shverb[shverb]
    authed = alias.authed
    shlines = alias.shlines

    assert authed
    assert shlines == ["git rev-parse --symbolic-full-name {}"], shlines

    # Take an Int as the Last to show, but ignore the Sign on the Int

    alt_shlines = list()
    alt_shlines.append("git rev-parse --symbolic-full-name HEAD")

    alt_parms = parms
    if not parms:

        alt_parms = ["@{-1}"]  # Define 'rpsfn' as 'rpsfn @{-1}'

    elif len(parms) == 1:

        parms_0 = parms[0]
        if parms == ["--"]:
            parms_0 = "-4"  # Define 'rpsfn --' as 'rpsfn -4'

        if re.match(r"^[-+]?[0-9]+$", string=parms_0):
            absintparm = abs(int(parms_0))

            for index in range(1, absintparm):
                alt_shlines.append(
                    "git rev-parse --symbolic-full-name @{{-{}}}".format(index)
                )

            exit_after_rpsfn_shlines(shlines=alt_shlines)

    assert alt_parms

    exit_if_shproc(shverb="rpsfn", parms=alt_parms, authed=True, shlines=shlines)

    assert False, alt_parms


def exit_after_rpsfn_shlines(shlines):
    """Trace all the ShLines before any of the Outputs, and drop the 'refs/heads/'"""

    for shline in shlines:
        byo.stderr_print("+ {} |sed 's,^refs/heads/,,'".format(shline))

    expansions = list()
    for shline in shlines:
        expansion = byo.subprocess_run_oneline(shline)
        expansions.append(expansion)

    for expansion in expansions:
        print(byo.str_removeprefix(expansion, "refs/heads/"))

    sys.exit(0)  # Exit 0 after printing Help Lines


#
# Amp up 'g', 'gi', 'gl', 'gli', 'gv', 'gvi'
# todo: merge with 'shpipes.py' near 'def do_g'
#


def exit_if_g(parms):  # "g"
    """grep -i ."""

    exit_if_g_parms_shoptions_shwords(parms, shoptions="-i", shwords=".")


# todo: merge with 'grep.py' and 'shpipes.do_g_parms_shoptions_shwords'
def exit_if_g_parms_shoptions_shwords(parms, shoptions, shwords=None):
    """Forward ShLine of Options or Seps, else default to Options and Words"""

    stdout_isatty = sys.stdout.isatty()

    # Forward ShLine w Parms of Options or Seps

    (options, seps, words) = byo.shlex_parms_partition(parms, mark="-e")
    if options or seps:
        shline = "git grep {}".format(shoptions).rstrip()

        marked_alt_parms = options + seps + words
        if set(marked_alt_parms) - set(parms):

            exit_after_weak_shparms(shline, parms=marked_alt_parms)

        else:

            exit_after_weak_shparms(shline, parms=parms)

    # Else default to Options and Words, except also add Color into a Tty Stdout

    options = shlex.split(shoptions)
    if stdout_isatty:
        if shwords:
            options.append("--color=auto")

    if not words:
        if shwords:
            words = shlex.split(shwords)

    # Trace and call and exit

    shline = "git grep"
    alt_parms = options + seps + words

    exit_after_weak_shparms(shline, parms=alt_parms)


# todo: merge with 'shpipe.exit_after_shparms'
def exit_after_weak_shparms(shline, parms):
    """Forward Parms into a Sh Subprocess - trace, call,and exit"""

    argv = shlex.split(shline) + parms

    byo.exit_after_one_loud_argv(argv)


def exit_if_gi(parms):  # "qbin/gi"  # "gi"
    """grep ."""

    exit_if_g_parms_shoptions_shwords(parms, shoptions="", shwords=".")


def exit_if_gl(parms):  # "qbin/gl"  # "gl"
    """grep -il"""  # better No ShWords, than r"." to match too many Lines

    exit_if_g_parms_shoptions_shwords(parms, shoptions="-il", shwords="")


def exit_if_gli(parms):  # "qbin/gli"  # "gli"
    """grep -l"""  # better No ShWords, than r"." to match too many Lines

    exit_if_g_parms_shoptions_shwords(parms, shoptions="-l", shwords="")


def exit_if_gv(parms):  # "qbin/gv"  # "gv"
    """grep -v -i ."""

    exit_if_g_parms_shoptions_shwords(parms, shoptions="-v -i", shwords=".")


def exit_if_gvi(parms):  # "qbin/gvi"  # "gvi"
    """grep -v"""

    exit_if_g_parms_shoptions_shwords(parms, shoptions="-v", shwords=".")


#
# Layer over 'qno' synthesis of 'qdno', 'qdhno', 'qspno'
#


def exit_if_em(parms):  # "em"
    exit_if_shverb_qno("em", parms)


def exit_if_vi(parms):  # "vi"
    exit_if_shverb_qno("vi", parms)


def exit_if_shverb_qno(shverb, parms):

    # Fetch the ShLine Templates

    aliases_by_shverb = form_aliases_by_shverb()

    assert shverb in aliases_by_shverb.keys()

    em_alias = aliases_by_shverb["em"]
    assert em_alias.shlines == ["qno {}", "em $(qno {})"], em_alias.shlines
    vi_alias = aliases_by_shverb["vi"]
    assert vi_alias.shlines == ["qno {}", "vi $(qno {})"], vi_alias.shlines

    alias = aliases_by_shverb[shverb]
    shlines = alias.shlines

    # Fill out the ShLine Templates

    shparms = byo.shlex_djoin(parms)

    shpipe = " && ".join(_.format(shparms).rstrip() for _ in shlines)
    if not shparms:
        shpipe = shpipe.replace("$(qno )", "$(qno)")

    shshline = "bash -c {!r}".format(shpipe)

    argv = shlex.split(shshline)
    byo.subprocess_run_loud(argv, stdin=None, shpipe=shpipe)

    sys.exit()  # Exit None after an ArgV exits Falsey


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


#
# ToDo Txt for Git Py
#


# for X in 3.2.1^{{tag,commit,tree}}; do (set -xe; git rev-parse $X); done


# todo: Git Py could decline to lose Stdin, such as refuse:  echo abc |git.py grep bc


# todo: test:  qno qa  # it should mean:  git add $(git diff --name-only)

# todo: echo qbin/qg{v,}{l,}{w,}{i,}
# todo: echo qb/g{v,}{l,}{w,}{i,}
# todo: auto-correct'ing the 'qg' [FILE ...] Parm to be:  $(qno)

# todo: define qg algorithmically
# todo: fan out as full 32 inside:  echo qbin/qg{v,}{l,}{w,}{i,}{n,}
# todo: ditto via 'shpipes.py' as full 32 inside:  echo qb/g{v,}{l,}{w,}{i,}{n,}

#
# todo: add '-h' into 'git log grep' => grep -h def.shlex_quote $(-ggl def.shlex_quote)
#

# compaction for qsis = git status --ignored --short
# todo:  $(qsis) without its first column, wow like we could stderr its first column

# q ..., could mean ... $(qno)  # so should it?

#
# expand unambiguous abbreviations
#   such as 'git log --no-mer --one --deco' for '--no-merges --oneline --decorate'
#

# _ = """
# % git checkout -b guests/jqdoe/sandbox1
# Switched to a new branch 'guests/jqdoe/sandbox1'
# % qrpar
# + git rev-parse --abbrev-ref HEAD
# guests/jqdoe/sandbox1
# % git push
# fatal: The current branch guests/jqdoe/sandbox1 has no upstream branch.
# To push the current branch and set the remote as upstream, use
#
#     git push --set-upstream origin guests/jqdoe/sandbox1
#
# zsh: exit 128   git push
# """

#
# trace what they mean - with inverse globs for concision, like at:  -ga bin/*.py
#

#
# --pretty=format:'%h %aE %s'  |cat - <(echo) |sed "s,@$DOMAIN,,"
# git blame/log --abbrev=3
#

#
# git push origin HEAD:people/jqdoe/project/1234
# git checkout -b people/jqdoe/project/1234 origin/people/jqdoe/project/1234
# git push origin --delete people/jqdoe/project/12345
# git branch -D people/jqdoe/project/12345
#

#
# git log --oneline --decorate --decorate-refs-exclude '*/origin/guests/??/*' -15
#
# -gd origin  # that's not precisely it, but abbreviate Diff's vs the Pushed Code
#

#
# persist a focus larger than $(qno) for 'qg', maybe
# persist a history of what qb, qlq, qlv did say
# persist notes onto each -gco, for display by -gbq and -gb
#
# compare
# git commit $(qno)
# git commit --all
#
# compare
# git show --name-only
# git diff-tree --no-commit-id --name-only -r
#


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/git.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
