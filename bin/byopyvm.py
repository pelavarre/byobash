#!/usr/bin/env python3

r"""
usage: byopyvm.py [--help] [WORD ...]

work quickly and concisely, over Dirs of Dirs of Files

positional arguments:
  WORD   the name of the next Func to run, a la the Forth Programming Language

options:
  --help               show this help message and exit

advanced bash install

  function = {
    : : 'Show Stack, else else do other Stack Work' : :
    if [ "$#" = 0 ]; then
        ~/Public/byobash/bin/byopyvm.py ls
    else
        ~/Public/byobash/bin/byopyvm.py "$@"
    fi
  }

quick start:

  git clone https://github.com/pelavarre/byobash.git
  cd byobash/

  source dotfiles/dot.byo.bashrc
  alias byopyvm.py=bin/byopyvm.py

  byopyvm.py

examples:

  byopyvm.py  # show these examples and exit
  byopyvm.py --h  # show this help message and exit
  command bin/byopyvm.py --  # show the Advanced Bash Install of ByoPyVM Py and exit

  # Files and Dirs

  = ls  # ls -1Frt |tail -4
  = cp  # cp -ip ... ...~$(date +%m%dpl%H%M%S)~  # FIXME
  = cp  # cp -ipR .../ ...~$(date +%m%dpl%H%M%S)~  # FIXME
  = mv  # mv -i ... ...~$(date +%m%dpl%H%M%S)~  # FIXME

  # Maths

  = math.pi  # echo 3.141592653589793 >3.142~
  = 2 *  # echo 2 >2~ && rm -f 3.142~ 2~ && echo 6.283185307179586 >6.283~
  = .  # cat 6.283~ && rm -f 6.283~

  = math.pi 2 * .  # all at once
"""


import json
import math
import pathlib
import pdb
import re
import shlex
import subprocess
import sys

import byotools as byo

_ = math
_ = pdb


def main():
    """Run from the Sh Command Line"""

    # Start up

    parms = sys.argv[1:]
    main.parms = parms

    collapse_star_parms(parms)

    func_by_verb = form_func_by_verb()

    patchdoc = """

      function = {
        : : 'Show Stack, else else do other Stack Work' : :
        if [ "$#" = 0 ]; then
            ~/Public/byobash/bin/byopyvm.py ls
        else
            ~/Public/byobash/bin/byopyvm.py "$@"
        fi
      }

    """

    # Quit conventionally

    byo.exit_if_patchdoc(patchdoc)  # command byopyvm.py --
    byo.exit_if_testdoc()  # byopyvm.py
    byo.exit_if_argdoc()  # byopyvm.py --help

    # Take each word, one at a time

    while parms:

        func = None

        shverb = parms[0]
        if shverb not in func_by_verb:
            shverb = taker_from_word(word=shverb)

        func = func_by_verb[shverb]
        func(parms)

        parms[::] = parms[1:]


def collapse_star_parms(parms):
    """Reconstruct the Sh Input Line despite the presence of '*' as a word"""

    shline = "ls"
    shshline = "bash -c {!r}".format(shline)
    argv = shlex.split(shshline)

    run = subprocess.run(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    length = len(lines)
    if length:

        index = 0
        while index < len(parms):
            stop = index + length

            if parms[index:][:length] == lines:
                parms[::] = parms[:index] + ["*"] + parms[stop:]

                # the Sh Input Line might, or might Not, have had a ' * ' here

            index += 1


#
# Parse input sourcelines
#


def taker_from_word(word):
    """Pick out what kind of Input Word this is"""

    if re.match(r"^[-+]?[0-9]+$", string=word):

        return "int"

    if re.match(r"^[-+]?[0-9]+[.][0-9]*$", string=word):  # todo: 1e-2

        return "float"

    if re.match(r"^([A-Z_a-z][0-9A-Z_a-z]*)?[.][.0-9A-Z_a-z]+$", string=word):

        return "dotted_name"

    if re.match(r"^[0-9A-Z_a-z]+$", string=word):

        return "name"

    if word in NAME_BY_CHAR.keys():
        name = NAME_BY_CHAR[word]

        return name

    return "SyntaxError"


def form_name_by_char():
    """Choose Names for Chars that Python Names reject"""

    d = dict()

    d[" "] = "space"
    d["!"] = "bang"
    d['"'] = "quote"
    d["#"] = "hash"
    # d["$"]
    # d["%"]
    d["&"] = "amp"
    d["'"] = "tick"
    # d["("]
    # d[")"]
    d["*"] = "star"
    d["+"] = "plus"
    d[","] = "comma"
    d["-"] = "dash"
    d["."] = "dot"
    d["/"] = "slash"

    d[":"] = "colon"
    d[";"] = "semi"
    # d["<"]
    d["="] = "equals"
    # d[">"]
    d["?"] = "query"

    d["@"] = "at"

    # d["["]
    d["\\"] = "backslant"
    # d["]"]
    d["^"] = "hat"
    d["_"] = "skid"  # underscore

    d["`"] = "backtick"

    # d["{"]
    d["|"] = "bar"
    # d["}"]
    d["~"] = "tilde"

    return d

    # https://unicode.org/charts/PDF/U0000.pdf
    # http://www.catb.org/jargon/html/A/ASCII.html
    # https://www.dourish.com/goodies/jargon.html

    # http://www.forth.org/svfig/Win32Forth/DPANS94.txt
    # https://aplwiki.com/wiki/Unicode


NAME_BY_CHAR = form_name_by_char()


#
# Wrap Shim's around Sh Commands
#


def form_func_by_verb():
    """Declare the Pipe Filter Abbreviations"""

    func_by_verb = dict(
        dot=do_dot,
        dotted_name=do_dotted_name,
        int=do_int,
        ls=do_ls,
        slash=do_slash,
        star=do_star,
    )

    return func_by_verb


def do_dot(parms):
    """Pop X but print its Value"""

    x = stack_pop(promise="cat {} && ")

    print(x)


def do_dotted_name(parms):
    """Push the Value of a Dotted Name"""

    evalled = eval(parms[0])
    stack_push(evalled)


def do_int(parms):
    """Push the Value of an Int"""

    x = int(parms[0])
    stack_push(x)


def do_ls(parms):
    """Show the Keys of the T Z Y X Stack, not its Values"""

    shline = "ls -1Frt |tail -4"
    sys.stderr.write("+ {}\n".format(shline))

    shshline = "bash -c {!r}".format(shline)
    argv = shlex.split(shshline)
    subprocess.run(argv, stdin=subprocess.PIPE, check=True)


def do_slash(parms):
    """Push Y / X"""

    (_x, _y) = stack_pop(2)
    x = _x / _y
    stack_push(x)


def do_star(parms):
    """Push Y * X"""

    (_x, _y) = stack_pop(2)
    x = _x * _y
    stack_push(x)


#
# Build a Stack out of Recently Touched Files in Cwd
#


def stack_pop(depth=1, promise=""):
    """Peek and remove some of the Values most recently pushed"""

    pairs = stack_pop_pairs(depth, promise=promise)
    values = list(_[-1] for _ in pairs)

    pops = list()
    for value in values:
        pop = json.loads(value)
        pops.append(pop)

    if len(pops) == 1:
        one_pop = pops[-1]

        return one_pop

    return pops


def stack_pop_pairs(depth=1, promise=""):
    """Peek and remove some of the Key-Value Pairs most recently pushed"""

    pairs = stack_peek_pairs(depth)

    paths = list(_[0] for _ in pairs)
    shpaths = " ".join(byo.shlex_dquote(_) for _ in paths)
    shline = "rm -f {}".format(shpaths)

    sys.stderr.write("+ {}{}\n".format(promise.format(shpaths), shline))

    argv = shlex.split(shline)
    subprocess.run(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True)

    return pairs


def stack_peek_pairs(depth=1):
    """Peek at some of the Key-Value Pairs most recently pushed"""

    #

    shline = "ls -1rt"

    argv = shlex.split(shline)
    run = subprocess.run(
        argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True
    )
    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    #

    pairs = list()

    filenames = lines[-depth:]
    for filename in filenames:
        path = pathlib.Path(filename)
        chars = path.read_text()

        pair = (str(path), chars)
        pairs.append(pair)

    #

    return pairs


def stack_push(value):
    """Push the Json Chars of a Value, into a new Autonamed File"""

    key = "{}~".format(round(value, 3))
    stack_push_key_value(key, value=value)


def stack_push_key_value(key, value):
    """Push the Json Chars of a Value, into a fresh File"""

    sys.stderr.write("+ echo {} >{}\n".format(value, key))

    chars = json.dumps(value)
    with open(key, "w") as writing:
        writing.write(chars)


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byopyvm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
