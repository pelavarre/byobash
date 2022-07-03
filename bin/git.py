#!/usr/bin/env python3

r"""
usage: git.py [--h] [--pwd] VERB [ARG ...]

copy each line of input bytes (or chars) to output (as if "cat"enating them slowly)

positional arguments:
  VERB          choice of subcommand
  ARG           choice of options and arguments

options:
  --help        show this help message and exit
  --for-chdir   print to Stdout what the in-memory Sh Cd needs to hear

quirks:
  taller Screens come with larger default limits on lines
  Zsh and Bash take '(dirs -p |head -1)', but only Bash takes 'dirs +0'

advanced bash install:

  function 'git.py' () {
    : : 'Show Git Status, else change the Sh Working Dir, else do other Git Work' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command git.py status "$@"
    elif [ "$#" = 1 ] && [ "$1" = "cd" ]; then
      'cd' "$(command git.py --for-chdir $@)" && (dirs -p |head -1)
    else
      command git.py "$@"
    fi
  }

examples:

  git.py cd  &&: cd $(git rev-parse --show-toplevel)
  git.py d  &&: git diff
  git.py g  &&: git grep
  git.py gl  &&: git grep -l
  git.py dh  &&: git diff HEAD~..., default HEAD~1
  git.py dhno  &&: git diff --name-only HEAD~..., default HEAD~1
  git.py dno  &&: git diff --name-only
  git.py lf  &&: git ls-files
  git.py s  &&: git show
  git.py sp  &&: git show --pretty=''
  git.py sno  &&: git show --name-only
  git.py ssi  &&: git status --short --ignored
  git.py sun  &&: git status --untracked-files=no

  git.py b  &&: git branch
  git.py ba  &&: git branch --all
  git.py co  &&: git checkout
  git.py cofrb  &&: git checkout ... && git fetch && git rebase
  git.py dad  &&: git describe --always --dirty
  git.py f  &&: git fetch
  git.py frb  &&: git fetch && git rebase
  git.py l  &&: git log
  git.py l1  &&: git log --decorate -1
  git.py lg  &&: git log --oneline --no-decorate --grep
  git.py lG  &&: git log --oneline --no-decorate -G ...  &&: search for touches
  git.py lS  &&: git log --oneline --no-decorate -S ...  &&: search for adds/ deletes
  git.py lq  &&: git log --oneline --no-decorate -19  &&: -0 for no limit
  git.py ls  &&: git log --stat
  git.py lv  &&: git log --oneline --decorate -19  &&: -0 for no limit
  git.py rb  &&: git rebase
  git.py ri  &&: git rebase --interactive --autosquash @{upstream}  &&: or HEAD~...
  git.py rl  &&: git reflog  &&: show Commits
  git.py rpar  &&: git rev-parse --abbrev-ref  &&: show the key line of:  git.py b
  git.py rpsfn  &&: git rev-parse --symbolic-full-name @{-1}  &&: show:  git.py co -
  git.py rv  &&: git remote -v
  git.py ssn  &&: git shortlog --summary --numbered

  git.py a  &&: git add
  git.py ap  &&: git add --patch
  git.py c  &&: git commit
  git.py ca  &&: git commit --amend
  git.py caa  &&: git commit --all --amend
  git.py caf  &&: git commit --all --fixup
  git.py cf  &&: git commit --fixup
  git.py cm  &&: git commit -m wip
  git.py cl  &&: take ⌃D to mean:  git clean -ffxdq  &&: destroy files outside Git Add
  git.py cls  &&: take ⌃D to mean:  sudo git clean -ffxdq  &&: not kidding around
  git.py pfwl  &&: take ⌃D to mean:  git push --force-with-lease
  git.py rhu  &&: take ⌃D to mean:  git reset --hard @{upstream}  &&: hide Commits
  git.py s1 ...  &&: git show :1:...  &&: common base
  git.py s2 ...  &&: git show :2:...  &&: just theirs
  git.py s3 ...  &&: git show :3:...  &&: juts ours

  git.py  &&: show these examples and exit
  git.py --h  &&: show this help message and exit
  git.py --  &&: 'git status' and then counts of:   git status --short --ignored
  command git.py --  &&: show the Advanced Bash Install of Git Py and exit
"""


import sys


import byotools as byo


#
# Radically abbreviate common Sh Git Lines
# thus emulate '~/.gitconfig' '[alias]'es,
# except don't hide the work of unabbreviation,
# away from our newer people trying to learn over your shoulder, by watching you work
#

GIT_ALIASES = dict()

GIT_ALIASES["cl"] = "git clean -ffxdq"
GIT_ALIASES["cls"] = "sudo git clean -ffxdq"
GIT_ALIASES["pfwl"] = "git push --force-with-lease"
GIT_ALIASES["rhu"] = "git reset --hard @{upstream}"
GIT_ALIASES["status"] = ["git status", "git status --short --ignored"]


# Block the more disruptive Sh Git Lines, unless authorized by ⌃D Tty Eof

GIT_INTERLOCKS = set()
GIT_INTERLOCKS.add("cl")
GIT_INTERLOCKS.add("cls")
GIT_INTERLOCKS.add("pfwl")
GIT_INTERLOCKS.add("rhu")


def main():
    """Run from the Sh Command Line"""

    parms = sys.argv[1:]

    patchdoc = """

  function 'git.py' () {
    : : 'Show Git Status, else change the Sh Working Dir, else do other Git Work' : :
    if [ "$#" = 1 ] && [ "$1" = "--" ]; then
      command git.py status "$@"
    elif [ "$#" = 1 ] && [ "$1" = "cd" ]; then
      'cd' "$(command git.py --for-chdir $@)" && (dirs -p |head -1)
    else
      command git.py "$@"
    fi
  }

    """

    # Define some forms of 'git.py'

    byo.exit_via_patchdoc(patchdoc)  # command git.py --
    byo.exit_via_testdoc()  # git.py
    byo.exit_via_argdoc()  # git.py --help

    # Default to forward the Parms into a Git Subprocess

    key = parms[0] if parms else None
    if key not in GIT_ALIASES.keys():

        byo.exit()

    # Define 'git.py VERB'

    value = GIT_ALIASES[key]

    shlines = value
    if isinstance(value, str):
        shlines = [value]

    for shline in shlines:
        print(shline)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# -gla could be -gl --author=$USER
#
# define a pile of functions: -grhu, -gcl, etc
# trace what they mean - with inverse globs for concision, like at:  -ga bin/*.py
# keep a history of what they said
#
# tune for Screen Height at default chop of -glqv, etc
# -glq, -glv in place of -glq, -glqv
#
# gg, ggl, gglq, gglv and so on, for the mouse click to pick up the leading letter
#
# pick a -glf focus for -gg
# capture:  -gc $(-gdno), compare to '--all'
#
# 'grep -h' => grep -h def.shlex_quote $(-ggl def.shlex_quote):
#
# attach notes to -gco, for display by -gbq and -gb
#
# git log --oneline --decorate --decorate-refs-exclude '*/origin/users/??/*' -15
#
# compare
# git show --name-only
# git diff-tree --no-commit-id --name-only -r
#
# git grep default to $(-gsno)
# git emacs
# git vi

# git log -S regex file.ext # grep the changes for an odd number (PickAxe)

# -gd origin

# git diff --name-only HEAD~1

# git add -p
# git describe --always --dirty


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/git.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
