#!/usr/bin/env python3

r"""
usage: git.py [--help] VERB [ARG ...]
usage: git.py [--help] --for-shproc SHVERB [ARG ...]
usage: git.py [--help] --for-chdir CDVERB [ARG ...]

work over clones of source dirs of dirs of files

positional arguments:
  VERB                 choice of SubCommand
  ARG                  choice of Options and Arguments

options:
  --help               show this help message and exit
  --for-shproc SHVERB  unabbreviate the ShVerb and call on Git to do its work
  --for-chdir CDVERB   print the $(git rev-parse --show-toplevel) to tell Cd where to go

quirks:
  dumps larger numbers of Lines into taller Screens, as defaults of:  git log -...
  classic Git rudely dumps Help & exits via a Code 1 Usage Error, when given no Parms
  Zsh and Bash take '(dirs -p |head -1)', but only Bash takes 'dirs +0'

advanced bash install:

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

examples:

  git.py  &&: show these examples and exit
  git.py --h  &&: show this help message and exit
  git.py --  &&: git checkout
  command git.py --  &&: show the Advanced Bash Install of Git Py and exit

  ls ~/.gitconfig
  ls .git/config

  &&: Navigation

  git.py cd  &&: cd $(git rev-parse --show-toplevel)
  git.py d  &&: git diff
  git.py g  &&: git grep  &&: FIXME: g to grep -i, gi to grep
  git.py co  &&: git checkout  &&: the calmest kind of 'git status'
  git.py gl  &&: git grep -l
  git.py dh  &&: git diff HEAD~...  &&: default HEAD~1, without '-b'
  git.py dhno  &&: git diff --name-only HEAD~..., default HEAD~1
  git.py dno  &&: git diff --name-only
  git.py em  &&: bash -c 'em $(qdhno |tee /dev/stderr)'
  git.py lf  &&: git ls-files
  git.py s  &&: git show
  git.py sp  &&: git show --pretty=''
  git.py spno  &&: git show --pretty='' --name-only
  git.py ssi  &&: git status --short --ignored  &&: calmer than 'git status'
  git.py st  &&: git status
  git.py sun  &&: git status --untracked-files=no
  git.py vi  &&: bash -c 'vi $(qdhno |tee /dev/stderr)'

  &&: Branch and Log Work

  git.py b  &&: git branch  &&: and see also:  git rev-parse --abbrev-ref
  git.py ba  &&: git branch --all
  git.py cofrb  &&: git checkout ... && git fetch && git rebase
  git.py cp  &&: git cherry-pick
  git.py dad  &&: git describe --always --dirty
  git.py f  &&: git fetch
  git.py frb  &&: git fetch && git rebase
  git.py l  &&: git log
  git.py l1  &&: git log --decorate -1
  git.py lg  &&: git log --oneline --no-decorate --grep ...
  git.py lgg  &&: git log --oneline --no-decorate -G ...  &&: search for touches
  git.py lgs  &&: git log --oneline --no-decorate -S ...  &&: search for adds/ deletes
  git.py lq  &&: git log --oneline --no-decorate -...  &&: default lots, -0 for no limit
  git.py lq1  &&: git log --oneline --no-decorate -1
  git.py lqa  &&: git log --oneline --no-decorate --author=$USER -...
  git.py ls  &&: git log --numstat  &&: but see also:  git show --name-only
  git.py lv  &&: git log --oneline --decorate -...  &&: default lots, -0 for no limit
  git.py lv1  &&: git log --oneline --decorate -1
  git.py rb  &&: git rebase
  git.py ri  &&: git rebase --interactive --autosquash HEAD~...  &&: default {@upstream}
  git.py rl  &&: git reflog  &&: show Commits
  git.py rpar  &&: git rev-parse --abbrev-ref  &&: show the key line of:  git.py b
  git.py rpsfn  &&: git rev-parse --symbolic-full-name @{-...}  &&: show:  git.py co -
  git.py rv  &&: git remote -v
  git.py ssn  &&: git shortlog --summary --numbered

  &&: Commit and Conflict Work

  git.py a  &&: git add
  git.py ap  &&: git add --patch
  git.py c  &&: git commit
  git.py ca  &&: git commit --amend
  git.py caa  &&: git commit --all --amend
  git.py caf  &&: git commit --all --fixup
  git.py cam  &&: git commit --all -m wip
  git.py cf  &&: git commit --fixup
  git.py cm  &&: git commit -m wip
  git.py cl  &&: take ⌃D to mean:  git clean -ffxdq  &&: destroy files outside Git Add
  git.py cls  &&: take ⌃D to mean:  sudo true && sudo git clean -ffxdq
  git.py pfwl  &&: take ⌃D to mean:  git push --force-with-lease
  git.py rh  &&: take ⌃D to mean:  git reset --hard ...  &&: hide local Commits
  git.py rhu  &&: take ⌃D to mean:  git reset --hard @{upstream}  &&: hide to start over
  git.py s1  &&: git show :1:...  &&: common base
  git.py s2  &&: git show :2:...  &&: just theirs
  git.py s3  &&: git show :3:...  &&: just ours

  &&: Reroll/Roll your own Repo

  rm -fr g.git git && git init --bare g.git && git clone g.git && cd g
"""
# todo:  Occasionally Needed Extras: making branches, deleting branches


import __main__
import collections
import getpass
import glob
import os
import pdb
import re
import shlex
import signal
import subprocess
import sys

import byotools as byo

_ = pdb


GitLikeAlias = collections.namedtuple("GitLikeAlias", "shlines authed".split())


def main():  # FIXME  # noqa C901 complex
    """Run from the Sh Command Line"""

    rm_fr_import_byotools_pyc()  # Give the Illusion of a Sh Alias without PyC

    aliases_by_verb = form_aliases_by_verb()

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

    """

    # Drop the "--for-shproc" Parm
    # if it's followed by no more Parms, or
    # if it's followed one of "--help", "--hel", "--he", "--h"

    parms = sys.argv[1:]

    if parms and (parms[0] == "--for-shproc"):
        if not parms[1:]:
            sys.argv[1:] = parms[1:]
        else:
            parm_1 = parms[1]
            if parm_1.startswith("--h") and "--help".startswith(parm_1):
                sys.argv[1:] = parms[1:]
            elif parm_1 == "--":  # here emulate Sh Function:  git.py --
                sys.argv[1:] = ["--for-shproc", "co"]
                # FIXME: but show counts of 'gssi', to discourage forgetting:  git add

        parms = sys.argv[1:]

    # Define some forms of 'git.py'

    byo.exit_via_patchdoc(patchdoc)  # command git.py --
    byo.exit_via_testdoc()  # git.py
    byo.exit_via_argdoc()  # git.py --help

    # Define many GitLikeAlias'es

    if parms[1:]:
        option = parms[0]
        if option.startswith("--for-"):
            unevalled_parms = parms[2:]

            # Define 'git.py --for-chdir cd ...'
            # to do only the 'git rev-parse --show-toplevel' work here,
            # while trusting the caller to the the 'cd $(...)' work

            if "--for-chdir".startswith(option):
                cdverb = parms[1]
                if cdverb == "cd":

                    alias = aliases_by_verb[cdverb]
                    authed = alias.authed
                    shlines = ["git rev-parse --show-toplevel"]

                    git_cd_shlines = ["cd $(git rev-parse --show-toplevel)"]
                    assert alias.shlines == git_cd_shlines, alias.shlines

                    exit_via_git_shproc(
                        shverb=cdverb,
                        parms=unevalled_parms,
                        authed=authed,
                        shlines=shlines,
                    )

            # Define 'git.py --for-shproc SHVERB ...'

            if "--for-shproc".startswith(option):
                shverb = parms[1]
                if shverb in aliases_by_verb.keys():

                    alias = aliases_by_verb[shverb]
                    authed = alias.authed
                    shlines = alias.shlines

                    exit_via_git_shproc(
                        shverb, parms=unevalled_parms, authed=authed, shlines=shlines
                    )

    # Default to forward the Parms into a Git Subprocess

    byo.exit_via_shcommand()


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


def exit_via_git_shproc(shverb, parms, authed, shlines):  # FIXME  # noqa: C901 complex
    """Forward Augmented Parms into a Git Subprocess and exit, else return"""

    thirdrows = 16  # FIXME

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
    shparms = " ".join(byo.shlex_dquote(_) for _ in alt_parms)
    shparms_minus = " ".join(byo.shlex_dquote(_) for _ in parms_minus)

    # Form each ShLine, and split each ShLine apart into an ArgV

    argvs = list()
    for shline in alt_shlines:

        # At most once, accept a request to forward Parms

        parmed_shline = None

        if "{}" not in shline:

            parmed_shline = shline.format()

        else:

            assert shparms is not None

            # Count off 0..N below HEAD, default 1, else take complex Parms

            if " HEAD~{}" in shline:

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

            # Default to take complex Parms

            else:
                parmed_shline = shline.format(shparms)

            # Reject subsequent requests to forward Parms, if any

            shparms = None

        # Fix it up some more and ship it out

        argv_shline = parmed_shline

        shguest = byo.shlex_dquote(getpass.getuser())
        guest_key = " --author=$USER"
        guest_repl = " --author={}".format(shguest)

        argv_shline = argv_shline.replace(guest_key, guest_repl)

        argv = shlex.split(argv_shline)
        argvs.append(argv)

    # Actually return, actually don't exit, if Parms present but not forwarded

    if shparms:

        return

    # Join the ShLines

    auth_shlines = list()
    for argv in argvs:
        shline = " ".join(byo.shlex_dquote(_) for _ in argv)

        overquoted = "git reset --hard '@{upstream}'"  # because of the {} Braces
        shline = shline.replace(overquoted, "git reset --hard @{upstream}")

        auth_shlines.append(shline)

    auth_shline = " && ".join(auth_shlines)

    # Demand authorization

    if not authed:
        if auth_shline == "git push --force-with-lease":
            rpar_shline = "git rev-parse --abbrev-ref HEAD"

            sys.stderr.write("+ {}\n".format(rpar_shline))
            rpar_argv = shlex.split(rpar_shline)
            _ = subprocess.run(rpar_argv)
            sys.stderr.write("+\n")

    if not authed:

        sys.stderr.write("did you mean:  {}\n".format(auth_shline))
        sys.stderr.write("press ⌃D to execute, or ⌃C to quit\n")
        try:
            _ = sys.stdin.read()
        except KeyboardInterrupt:
            sys.stderr.write("\n")
            sys.stderr.write("KeyboardInterrupt\n")

            returncode = 0x80 | signal.SIGINT
            assert returncode == 130, (returncode, signal.SIGINT)

            sys.exit(returncode)

    # Run each of the ArgV's and exit

    exit_via_argvs(argvs)


def exit_via_argvs(argvs):
    """Run each of the ArgV's and exit"""

    for argv in argvs:

        shline = " ".join(byo.shlex_dquote(_) for _ in argv)

        sys.stderr.write("+ {}\n".format(shline))
        run = subprocess.run(argv)
        if run.returncode:  # Exit early, at the first NonZero Exit Status ReturnCode
            sys.stderr.write("+ exit {}\n".format(run.returncode))

            sys.exit(run.returncode)

    sys.exit()


#
# Wrap many many Shim's around Git
#


#
# FIXME put these Comments somewhere good
#
# Radically abbreviate common Sh Git Lines
# thus emulate '~/.gitconfig' '[alias]'es,
# except don't hide the work of unabbreviation,
# away from our newer people trying to learn over your shoulder, by watching you work
#
# Block the more disruptive Sh Git Lines, unless authorized by ⌃D Tty Eof
#


def form_aliases_by_verb():
    """Declare the GitLikeAlias'es"""

    doc = __main__.__doc__

    # Visit each GitLike Alias

    aliases_by_verb = dict()
    for (k, v) in ALIASES.items():
        verb = k

        shline = "git.py {k}  &&: {v}".format(k=k, v=v)
        shlines = v.split(" && ")

        # Compile-time option for a breakpoint on a ShVerb or CdVerb

        if False:
            if verb == "cd":
                pdb.set_trace()

        # Separate kinds of Alias'es
        # todo: Require the DocLine found in full, with only zero or more Comments added

        docline_0 = shline
        docline_0 = byo.str_removesuffix(docline_0, " {}")
        docline_1 = docline_0.replace("  &&: cat - && ", "  &&: take ⌃D to mean:  ")
        docline_2 = docline_0.format("...")
        docline_3 = docline_1.format("...")

        alias = GitLikeAlias(shlines, authed=True)
        if "  &&: cat - && " in shline:
            alias = GitLikeAlias(shlines, authed=None)

        if docline_3 in doc:  # add interlock before, and place Parms explicitly
            pass
        elif docline_2 in doc:  # place Parms explicitly, in the middle or at the end
            pass
        elif docline_1 in doc:  # add interlock before, but no Parms
            pass
        elif docline_0 in doc:  # add optional Parms past the end
            pass
        else:
            assert False, (shlines, docline_0, docline_1)

        # Declare this GitLike Alias

        assert verb not in aliases_by_verb.keys(), repr(verb)

        aliases_by_verb[verb] = alias

    return aliases_by_verb


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
    "cofrb": "git checkout {} && git fetch && git rebase",  # auth'ed!
    "cp": "git cherry-pick {}",
    "d": "git diff {}",
    "dad": "git describe --always --dirty",
    "dh": "git diff HEAD~{}",  # default HEAD~1, without '-b'
    "dhno": "git diff --name-only HEAD~{}",
    "dno": "git diff --name-only {}",
    "em": "bash -c 'em $(qdhno |tee /dev/stderr)'",
    "f": "git fetch",
    "frb": "git fetch && git rebase",
    "g": "git grep {}",  # todo: default Grep of $(-gdhno)
    "gl": "git grep -l {}",  # todo: default Grep of $(-gdhno)
    "l": "git log {}",
    "l1": "git log --decorate -1 {}",
    "lf": "git ls-files {}",
    "lg": "git log --oneline --no-decorate --grep {}",
    "lgg": "git log --oneline --no-decorate -G {}",  # touches, aka Grep Source
    "lgs": "git log --oneline --no-decorate -S {}",  # adds/deletes, aka Pickaxe
    "lq": "git log --oneline --no-decorate -{}",
    "lq1": "git log --oneline --no-decorate -1 {}",
    "lqa": "git log --oneline --no-decorate --author=$USER -{}",
    "ls": "git log --numstat {}",
    "lv": "git log --oneline --decorate -{}",
    "lv1": "git log --oneline --decorate -1 {}",
    "pfwl": "cat - && git push --force-with-lease",
    "rb": "git rebase {}",  # auth'ed!
    "rh": "cat - && git reset --hard {}",
    "rhu": "cat - && git reset --hard @{{upstream}}",
    "ri": "git rebase --interactive --autosquash HEAD~{}",
    "rl": "git reflog",
    "rpar": "git rev-parse --abbrev-ref {}",
    "rpsfn": "git rev-parse --symbolic-full-name @{{-{}}}",
    "rv": "git remote -v",
    "s": "git show {}",
    "s1": "git show :1:{}",
    "s2": "git show :2:{}",
    "s3": "git show :3:{}",
    "sp": "git show --pretty='' {}",
    "spno": "git show --pretty='' --name-only {}",
    "ssi": "git status --short --ignored",
    "ssn": "git shortlog --summary --numbered",
    "st": "git status {}",
    "sun": "git status --untracked-files=no",
    "vi": "bash -c 'vi $(qdhno |tee /dev/stderr)'",
}

# Mac HFS FileSystem's don't accept 'qlG' and 'qlg' existing inside one Dir
# Mac HFS FileSystem's don't accept 'qlS' and 'qls' existing inside one Dir


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# 'todo.txt' for 'git.py' =>

#
# FIXME
#
# add '-h' into 'git log grep' => grep -h def.shlex_quote $(-ggl def.shlex_quote)
#
# drop the doubled -19 -1 from such as:  qlq -1
#
# qbin/qlsq  =>  git.py ls --  =>  interleave of qlq and each qspno
# for N in $(seq 3); do
#     echo
#     git log --oneline --no-decorate -$N |tail -1
#     git show --pretty= --name-only HEAD~$N
# done
#

#
# todo
#

# compaction for qssi = git status --short --ignored

# q ..., could mean ... $(qdhno)  # so should it?

#
# expand unambiguous abbreviations
#   such as 'git log --no-mer --one --deco' for '--no-merges --oneline --decorate'
#

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
# persist a focus larger than $(qdhno) for 'qg', maybe
# persist a history of what qb, qlq, qlv did say
# persist notes onto each -gco, for display by -gbq and -gb
#
# compare
# git commit $(qdhno)
# git commit --all
#
# compare
# git show --name-only
# git diff-tree --no-commit-id --name-only -r
#


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/git.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
