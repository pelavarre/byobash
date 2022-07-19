#!/usr/bin/env python3

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
  trace the expansion of each Alias as it runs, to help people learn by watching
  dumps larger numbers of Lines into taller Screens, as defaults of:  git log -...
  interlocks the most destructive moves by hanging till ⌃D Tty Eof
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

  git.py  # show these examples and exit
  git.py --h  # show this help message and exit
  git.py --  # git checkout
  command bin/git.py --  # show the Advanced Bash Install of Git Py and exit

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
  git.py em  # bash -c 'em $(qdhno |tee /dev/stderr)'
  git.py g  # git grep -i
  git.py gi  # git grep
  git.py gl  # git grep -ilR
  git.py gli  # git grep -lR
  git.py lf  # git ls-files
  git.py no  # git show --pretty='' --name-only ..., else git diff --name-only HEAD~1
  git.py s  # git show
  git.py sp  # git show --pretty=''
  git.py spno  # git show --pretty='' --name-only
  git.py ssi  # git status --short --ignored  # calmer than 'git status'
  git.py st  # git status
  git.py sun  # git status --untracked-files=no
  git.py vi  # bash -c 'vi $(qdhno |tee /dev/stderr)'

  # Branch and Log Work (~27 aliases)

  git.py b  # git branch  # and see also:  git rev-parse --abbrev-ref
  git.py ba  # git branch --all
  git.py cofrb  # git checkout ... && git fetch && git rebase  # auth w/out ⌃D
  git.py cp  # git cherry-pick
  git.py dad  # git describe --always --dirty
  git.py f  # git fetch
  git.py frb  # git fetch && git rebase  # auth w/out ⌃D
  git.py l  # git log
  git.py l1  # git log --decorate -1
  git.py lg  # git log --oneline --no-decorate --grep ...
  git.py lgg  # git log --oneline --no-decorate -G ...  # search for touches
  git.py lgs  # git log --oneline --no-decorate -S ...  # search for adds/ deletes
  git.py lols  # git log --oneline --numstat  # list Files per Commit
  git.py lq  # git log --oneline --no-decorate -...  # default lots, -0 for no limit
  git.py lq1  # git log --oneline --no-decorate -1
  git.py lqa  # git log --oneline --no-decorate --author=$USER -...
  git.py ls  # git log --numstat  # but see also:  git show --name-only
  git.py lv  # git log --oneline --decorate -...  # default lots, -0 for no limit
  git.py lv1  # git log --oneline --decorate -1
  git.py rb  # git rebase
  git.py ri  # git rebase --interactive --autosquash HEAD~...  # else {@upstream}
  git.py rl  # git reflog  # show Commits of Clone, no matter the Branch
  git.py rlv  # git reflog --format=fuller  # show more detail for Commits of Clone
  git.py rpar  # git rev-parse --abbrev-ref  # show the key line of:  git.py b
  git.py rpsfn  # git rev-parse --symbolic-full-name @{-...}  # show:  git.py co -
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


SIGINT_RETURNCODE = 0x80 | signal.SIGINT
assert SIGINT_RETURNCODE == 130, (SIGINT_RETURNCODE, 0x80, signal.SIGINT)

GitLikeAlias = collections.namedtuple("GitLikeAlias", "shlines authed".split())


#
# Run from the Sh Command Line
#


def main():  # todo  # noqa C901 complex
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

    """

    # Take "--for-cdproc" and "--for-shproc" out early

    parms = None

    sys_parms = sys.argv[1:]
    options = ("--for-cdproc", "--for-shproc")
    if sys_parms and (sys_parms[0] in options):
        parms = sys.argv[2:]

        # Define the 'git.py' that isn't 'command git.py'

        if not parms:

            byo.exit_after_testdoc()

        # Define the 'git.py --' that isn't 'command git.py --'

        if parms == ["--"]:

            parms = ["co"]  # "git checkout"
            # FIXME: print counts of 'gssi' as reminders for:  git add

    # Define the most conventional forms of 'git.py'

    byo.exit_if_patchdoc(patchdoc)  # command git.py --
    byo.exit_if_testdoc()  # command git.py
    byo.exit_if_argdoc()  # git.py --help

    # Expand any of many intensely cryptic calls of "--for-cdproc" and "--for-shproc"

    if parms:
        shverb = parms[0]

        exit_if_by_shverb(shverb, parms=parms[1:])

    # Default to forward the Parms into a Git Subprocess

    byo.exit_after_shverb()


def exit_if_by_shverb(shverb, parms):
    """Expand any of many intensely cryptic calls of Git Aliases"""

    exit_if_funcs_by_shverb = form_exit_if_funcs_by_shverb()
    aliases_by_shverb = form_aliases_by_shverb()

    # For a few ShVerb's, take more context into account

    exit_if_func = exit_if_funcs_by_shverb.get(shverb)
    if exit_if_func:

        exit_if_func(parms)

    # Commonly, instantiate a fixed-length template of ShLine's

    alias = aliases_by_shverb.get(shverb)
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
        # elif alt_shlines == ["git grep {}"]:  # no, because Git Grep defaults to -R
        #     alt_parms = ["."]
        # elif alt_shlines == ["git grep -i {}"]:
        #     alt_parms = ["."]
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
        shline = byo.shlex_djoin(argv)

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
            _ = subprocess.run(rpar_argv, stdin=subprocess.PIPE)
            sys.stderr.write("+\n")

    if not authed:

        sys.stderr.write("did you mean:  {}\n".format(auth_shline))
        sys.stderr.write("press ⌃D to execute, or ⌃C to quit\n")
        try:
            _ = sys.stdin.read()
        except KeyboardInterrupt:
            sys.stderr.write("\n")
            sys.stderr.write("KeyboardInterrupt\n")

            assert SIGINT_RETURNCODE == 130, SIGINT_RETURNCODE

            sys.exit(SIGINT_RETURNCODE)  # Exit 130 to say KeyboardInterrupt SIGINT

    # Run each of the ArgV's and exit

    byo.exit_after_some_argv(argvs)


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

        shline = None
        shlines = v
        if not isinstance(v, list):
            shline = "git.py {k}  # {v}".format(k=k, v=v)
            shlines = v.split(" && ")

        # Compile-time option for a breakpoint on a ShVerb or CdVerb

        _ = """  # duck Flake8 C901 is too complex (11)  # todo

            if False:
                if verb == "cd":
                    pdb.set_trace()

        """

        # Separate kinds of Alias'es
        # todo: Require the DocLine found in full, with only zero or more Comments added

        if shline is None:

            alias = GitLikeAlias(shlines, authed=True)

        else:

            docline_0 = shline
            docline_0 = byo.str_removesuffix(docline_0, " {}")
            docline_1 = docline_0.replace("  # cat - && ", "  # take ⌃D to mean:  ")
            docline_2 = docline_0.format("...")
            docline_3 = docline_1.format("...")

            alias = GitLikeAlias(shlines, authed=True)
            if "  # cat - && " in shline:
                alias = GitLikeAlias(shlines, authed=None)

            if docline_3 in doc:  # add interlock before, and place Parms explicitly
                pass
            elif (
                docline_2 in doc
            ):  # place Parms explicitly, in the middle or at the end
                pass
            elif docline_1 in doc:  # add interlock before, but no Parms
                pass
            elif docline_0 in doc:  # add optional Parms past the end
                pass
            else:
                assert False, (shlines, docline_0, docline_1)

        # Declare this GitLike Alias

        assert verb not in aliases_by_shverb.keys(), repr(verb)

        aliases_by_shverb[verb] = alias

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
    "cofrb": "git checkout {} && git fetch && git rebase",  # auth w/out ⌃D
    "cp": "git cherry-pick {}",
    "d": "git diff {}",
    "dad": "git describe --always --dirty",
    "dh": "git diff HEAD~{}",  # default HEAD~1, without '-b'
    "dhno": "git diff --name-only HEAD~{}",
    "dno": "git diff --name-only {}",
    "em": "bash -c 'em $(qdhno |tee /dev/stderr)'",
    "f": "git fetch",
    "frb": "git fetch && git rebase",
    "g": "git grep -i {}",  # todo: default Grep of $(-gdhno)
    "gi": "git grep {}",  # todo: default Grep of $(-gdhno)
    "gl": "git grep -il {}",  # todo: default Grep of $(-gdhno)
    "gli": "git grep -l {}",  # todo: default Grep of $(-gdhno)
    "l": "git log {}",
    "l1": "git log --decorate -1 {}",
    "lf": "git ls-files {}",
    "lg": "git log --oneline --no-decorate --grep {}",
    "lgg": "git log --oneline --no-decorate -G {}",  # touches, aka Grep Source
    "lgs": "git log --oneline --no-decorate -S {}",  # adds/deletes, aka Pickaxe
    "lols": "git log --oneline --numstat {}",
    "lq": "git log --oneline --no-decorate -{}",
    "lq1": "git log --oneline --no-decorate -1 {}",
    "lqa": "git log --oneline --no-decorate --author=$USER -{}",
    "ls": "git log --numstat {}",
    "lv": "git log --oneline --decorate -{}",
    "lv1": "git log --oneline --decorate -1 {}",
    "no": "git show --pretty='' --name-only ..., else git diff --name-only HEAD~1",
    "pfwl": "cat - && git push --force-with-lease",
    "rb": "git rebase {}",  # auth w/out ⌃D
    "rh": "cat - && git reset --hard {}",
    "rhu": "cat - && git reset --hard @{{upstream}}",
    "ri": "git rebase --interactive --autosquash HEAD~{}",
    "rl": "git reflog",
    "rlv": "git reflog --format=fuller",
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
        no=exit_if_git_no,
        rpsfn=exit_if_git_rpsfn,
    )

    return exit_if_funcs


def exit_if_git_no(parms):
    """List the Files of the Git Diff HEAD~1, else the Files of a chosen Hash"""

    aliases_by_shverb = form_aliases_by_shverb()

    dhno_alias = aliases_by_shverb["dhno"]
    assert dhno_alias.shlines == ["git diff --name-only HEAD~{}"]

    # Collapse back down to 'git diff --name-only HEAD~1', if no Parms

    if not parms:

        exit_if_by_shverb(shverb="dhno", parms=parms)

    # Pick out an Ext, if 1 Parm that isn't an Int nor a Hash

    if len(parms) == 1:
        parms_0 = parms[0]
        if not re.match(r"^[0-9A-Fa-f+]$", string=parms_0):

            ext = parms_0 if parms_0.startswith(".") else ".{}".format(parms_0)
            re_ext = re.escape(ext[1:])
            alt_re_ext = r"[.]" + re_ext + r"$"  # simplify to r"[.]" down from "r\."

            shline = "git diff --name-only HEAD~1 |grep -e {}".format(
                byo.shlex_dquote(alt_re_ext)
            )
            shshline = "bash -c {!r}".format(shline)
            argv = shlex.split(shshline)

            byo.subprocess_run_else_exit(argv, shline)

            sys.exit()  # Exit None after an ArgV exits Falsey

    # Else fall back to list the Files of a chosen Hash

    exit_if_by_shverb(shverb="spno", parms=parms)


def exit_if_git_rpsfn(parms):
    """List the last Symbolic Full Names through to an Int, else forward Parms"""

    # Require the Alias "rpsfn" defined, same as here, across the ArgDoc and such

    shverb = "rpsfn"

    aliases_by_shverb = form_aliases_by_shverb()

    alias = aliases_by_shverb[shverb]
    authed = alias.authed
    shlines = alias.shlines

    assert authed
    assert shlines == ["git rev-parse --symbolic-full-name @{{-{}}}"], shlines

    # Take an Int as the Last to show, but ignore the Sign on the Int

    alt_shlines = list()
    alt_shlines.append("git rev-parse --abbrev-ref HEAD")

    alt_parms = parms
    if parms:
        parms_0 = parms[0]
        if re.match(r"^[-+]?[0-9]+$", string=parms_0):

            absintparm = abs(int(parms_0))
            alt_parms = parms[1:]

            for index in range(1, absintparm + 1):
                alt_shlines.append(
                    "git rev-parse --symbolic-full-name @{{{{-{}}}}}".format(index)
                )

    exit_if_shproc(shverb="rpsfn", parms=alt_parms, authed=True, shlines=alt_shlines)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# 'todo.txt' for 'git.py' =>

#
# FIXME: add '-h' into 'git log grep' => grep -h def.shlex_quote $(-ggl def.shlex_quote)
#
# FIXME: dial back the over-aggressive quoting at qrpsfn => git rev-parse ... '@{-1}'
#
# FIXME: solve:  qrpsfn --
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

_ = """
% git checkout -b guests/jqdoe/sandbox1
Switched to a new branch 'guests/jqdoe/sandbox1'
% qrpar
+ git rev-parse --abbrev-ref HEAD
guests/jqdoe/sandbox1
% git push
fatal: The current branch guests/jqdoe/sandbox1 has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin guests/jqdoe/sandbox1

zsh: exit 128   git push
"""

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
