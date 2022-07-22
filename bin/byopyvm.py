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

  = math.pi  # echo 3.141592653589793 >3.142
  = 2 *  # echo 2 >2 && rm -f 3.142 2 && echo 6.283185307179586 >6.283
  = .  # cat 6.283 && rm -f 6.283

  = math.pi 2 * .  # all at once
"""


import collections
import json
import math
import os
import pathlib
import pdb
import re
import shlex
import subprocess
import sys
import traceback

import byotools as byo

_ = math
_ = pdb


FILENAME_PRECISION_3 = 3  # 3 digits means mention 'math.pi' as '3.142'


def main():
    """Run from the Sh Command Line"""

    # Start up

    parms = sys.argv[1:]
    main.parms = parms

    collapse_star_parms(parms)

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

    # Run well

    parms_run(parms)


def parms_run(parms):
    """Run the Parms = Read a Word, Evaluate the Word, Print the Result, Loop"""

    # Take each word, one at a time

    func_by_verb = form_func_by_verb()

    while parms:

        func = None

        shverb = parms[0]
        if shverb not in func_by_verb:
            shverb = taker_from_word(word=shverb)

        assert shverb in func_by_verb, (shverb, parms)

        func = func_by_verb[shverb]
        func(parms)

        parms[::] = parms[1:]


def collapse_star_parms(parms):
    """Reconstruct the Sh Input Line despite the presence of '*' as a word"""

    shline = "ls"
    shshline = "bash -c {!r}".format(shline)

    sys.stdout.flush()
    sys.stderr.flush()
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

    d["0"] = "zero"  # Python accepts Digital Digits in the Name, but not to start with
    d["1"] = "one"
    d["2"] = "two"
    d["3"] = "three"
    d["4"] = "four"
    d["5"] = "five"
    d["6"] = "six"
    d["7"] = "seven"
    d["8"] = "eight"
    d["9"] = "nine"

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
        buttonfile=do_buttonfile,
        dot=do_dot,
        dotted_name=do_dotted_name,
        int=do_int,
        ls=do_ls,
        dash=do_dash,  # Monosyllabic Folk speak of the '-' Dash
        minus=do_dash,  # Calculator Folk speak of the '-' Minus
        name=do_name,
        over=do_push_y,
        plus=do_plus,
        slash=do_slash,
        star=do_star,
    )

    return func_by_verb


def do_dot(parms):
    """Pop X but print its Value"""

    x = stack_pop(1, default=None, promise="cat {} && ")

    print(x)


def do_dotted_name(parms):
    """Call a Dotted Name, else push its Value"""

    do_name(parms)


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

    sys.stdout.flush()
    sys.stderr.flush()
    subprocess.run(argv, stdin=subprocess.PIPE, check=True)


def do_dash(parms):
    """Push Y - X in place of Y X"""

    if stack_depth() < 1:
        stack_push(0)
    elif stack_depth() < 2:
        stack_push(0)
        stack_swap()
    else:

        (_y, _x) = stack_pop(2, default=0)
        x = _y - _x
        stack_push(x)


def do_plus(parms):
    """Push Y + X in place of Y X"""

    if stack_depth() < 1:
        stack_push(0)
    elif stack_depth() < 2:
        stack_push(0)
    else:

        (_y, _x) = stack_pop(2, default=0)
        x = _y + _x
        stack_push(x)


def do_name(parms):
    """Call a Name, else push its Value"""

    evalled = eval(parms[0])

    if not isinstance(evalled, collections.abc.Callable):
        stack_push(evalled)
    else:
        do_x_func(parms, evalled)


def do_push_y(parms):
    """Push Y"""

    if stack_depth() < 1:
        stack_push(0)
    elif stack_depth() < 2:
        stack_push(0)
    else:

        (_y, _x) = stack_peek(2, default=None)
        stack_push(_y)


def do_slash(parms):
    """Push Y / X in place of Y X"""

    if stack_depth() < 1:
        stack_push(1)
    elif stack_depth() < 2:
        stack_push(1)
        stack_swap()
    else:

        (_, _x) = stack_peek(2, default=None)
        if _x == 0:
            stack_push(1)
        else:

            (_y, _x) = stack_pop(2, default=1)
            x = _y / _x  # todo:  1 5 / -> 0.2 -> 5 should end in Int, not Float
            stack_push(x)


def do_star(parms):
    """Push Y * X in place of Y X"""

    if stack_depth() < 1:
        stack_push(1)
    elif stack_depth() < 2:
        stack_push(1)
    else:

        (_y, _x) = stack_pop(2, default=1)
        x = _y * _x  # todo: -0.0 should be 0
        stack_push(x)


def do_x_func(parms, func):
    """Push Func(X) in place of X"""

    assert func is math.sqrt

    if stack_depth() < 1:
        stack_push(1)
    else:

        _x = stack_peek(1, default=0)
        if _x >= 0:
            _x = stack_pop(1, default=0)
            x = func(_x)  # todo: sqrt of int should still be int
            stack_push(x)
        else:
            x = _x * _x
            stack_push(x)


#
# Build a Stack out of Recently Touched Files in Cwd
#


def stack_depth():
    """Count the Values in the Stack"""

    pairs = stack_pairs_peek(0)  # todo:  stop evalling all the Values to count them
    depth = len(pairs)

    return depth


def stack_swap():
    """Drag the 2nd-to-Last Value to Top of Stack"""

    if stack_depth() < 1:
        stack_push(0)
    elif stack_depth() < 2:
        stack_push(0)
    else:

        pairs = stack_pairs_peek(2)
        pair = pairs[0]
        (basename, _) = pair

        shline = "touch {}".format(byo.shlex_dquote(basename))
        sys.stderr.write("+ {}\n".format(shline))

        sys.stdout.flush()
        sys.stderr.flush()
        subprocess.run(shlex.split(shline))


#
# Build a Stack out of Recently Touched Files in Cwd
#


def stack_pop(depth, default=None, promise=""):
    """Peek and eval and remove some of the Values most recently pushed"""

    peeks = stack_peek(depth, default=default)

    _ = stack_pairs_pop(depth, promise=promise)

    return peeks  # will be 'one_peek' in the corner of 'depth=1'


def stack_peek(depth, default):
    """Peek and eval some of the Values most recently pushed"""

    assert depth >= 1
    default_json = json.dumps(default)

    pairs = stack_pairs_peek(depth, default_json=default_json)  # peek, not pop
    values = list(_[-1] for _ in pairs)

    peeks = list()
    for value in values:
        peek = stack_loads(chars=value, default=default)
        peeks.append(peek)

    assert len(peeks) == depth, (len(peeks), depth)
    if depth == 1:
        one_peek = peeks[-1]

        return one_peek  # is 'one_peek' in the corner of 'depth=1'

    return peeks  # is zero, two, or more Peeks, in the corners of 'depth != 1'


def stack_dumps(value):
    """Format an Object as Chars"""

    try:
        poke = json.dumps(value)
    except TypeError:
        poke = str(value)

        assert isinstance(value, complex), (type(value), poke)

    return poke


def stack_loads(chars, default):
    """Unwrap the Object inside the Chars, else return the Default"""

    try:
        peek = json.loads(chars)
    except json.JSONDecodeError:
        try:
            peek = complex(chars)
        except ValueError:
            peek = default

    return peek


def stack_pairs_pop(depth, default_json=json.dumps(None), promise=""):
    """Peek and remove some of the Basename-Chars Pairs most recently pushed"""

    assert depth >= 0

    pairs = stack_pairs_peek(depth, default_json=default_json)

    paths = list(_[0] for _ in pairs)
    shpaths = " ".join(byo.shlex_dquote(_) for _ in paths if _ is not None)
    if shpaths:
        if any(_.startswith("-") for _ in paths):
            shline = "rm -f -- {}".format(shpaths)
        else:
            shline = "rm -f {}".format(shpaths)

        sys.stderr.write("+ {}{}\n".format(promise.format(shpaths), shline))

        sys.stdout.flush()
        sys.stderr.flush()
        argv = shlex.split(shline)
        subprocess.run(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True)

    return pairs


def stack_pairs_peek(depth=1, default_json=json.dumps(None)):
    """Peek at some of the Basename-Chars Pairs most recently pushed"""

    assert depth >= 0

    #

    shline = "ls -1rt"

    sys.stdout.flush()
    sys.stderr.flush()
    argv = shlex.split(shline)
    run = subprocess.run(
        argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, check=True
    )
    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    filenames = lines

    #

    pairs = list()

    for filename in filenames:
        path = pathlib.Path(filename)
        if path.is_file():

            chars = path.read_text()
            chars = chars.rstrip()

            peek = stack_loads(chars, default=None)
            if peek is None:  # such as json.JSONDecodeError

                continue

            pair = (str(path), chars)
            pairs.append(pair)

    if depth:
        pairs = pairs[-depth:]  # todo: stop evalling the discarded Depths of Stack

    #

    none_basename_pair = (None, default_json)
    while len(pairs) < depth:
        pairs.append(none_basename_pair)

    #

    return pairs


def stack_push(value):
    """Push the Json Chars of a Value, into a new Autonamed File"""

    if isinstance(value, float):
        basename = "{}".format(round(value, FILENAME_PRECISION_3))
    else:
        basename = str(value)

    stack_push_basename_value(basename, value=value)


def stack_push_basename_value(basename, value):
    """Push the Json Chars of a Value, into a fresh File"""

    path = pathlib.Path(basename)
    chars = stack_dumps(value)

    shvalue = byo.shlex_dquote(chars)

    # Choose the given Basename, else the next that doesn't already exist

    alt_path = path
    if path.exists():
        alt_path = find_alt_path(path)

    alt_shpath = byo.shlex_dquote(str(alt_path))

    # Trace and run

    echo_shline = "echo {} >{}".format(shvalue, alt_shpath)
    sys.stderr.write("+ {}\n".format(echo_shline))

    with open(alt_path, "w") as writing:
        writing.write("{}\n".format(chars))


def find_alt_path(path):
    """Find the next Basename that doesn't already exist in the Dir"""

    alt_path = pathlib.Path("{}~".format(path))  # the 0th Alt

    index = 1
    while alt_path.exists():
        alt_path = pathlib.Path("{}~{}~".format(path, index))

        index += 1

    return alt_path


#
# Take Double-Click's of Dot-Command ButtonFile's
#


def do_buttonfile(parms):
    """Take one Double-Click of a Dot-Command ButtonFile"""

    try:

        do_buttonfile_word(parms)

    except Exception:
        sys.stderr.write("\n")

        traceback.print_exc()

        sys.stderr.write("Press ⌃D TTY EOF to quit\n")
        sys.stdin.read()

        raise


def do_buttonfile_word(parms):  # FIXME  # noqa C901 too complex (11)
    """Run the Name of a Dot-Command ButtonFile, without its Ext, as a Word"""

    assert parms

    # Take the Name, without its Ext, as a Word

    main_file = parms.pop(1)

    basename = os.path.basename(main_file)
    (root, ext) = os.path.splitext(basename)
    _ = ext

    # Run the Word

    word = root
    if word in "0123456789":
        entry_write_char(parms=[word])
    elif word == "E":  # todo:  add "+:-" to toggle the Sign of Exp else of Mantissa
        entry_write_char(parms=["E".lower()])
    elif word == "clear":
        entries_clear()
    elif word == "dot":
        entry_write_char(parms=["."])
    else:
        entry = entry_close_if_open()
        if word == "comma":
            run_button_comma(entry)

        elif word == "e":
            do_dotted_name(parms=["math.e"])
        elif word == "i":
            do_name(parms=["1j"])
        elif word == "j":
            do_name(parms=["1j"])
        elif word == "\N{Greek Small Letter Pi}":  # π
            do_dotted_name(parms=["math.pi"])
        elif word == "\N{Square Root}":  # √
            do_dotted_name(parms=["math.sqrt"])

        else:

            run_button_word(parms, word=word)


def run_button_word(parms, word):
    """Run the Parms, but first close the last Entry, if needed"""

    entry_close_if_open()

    parms = [word]
    parms_run(parms)


def entries_clear():
    """Pop all the Number Files, else push out four Numbers Files named 3, 2, 1, 0"""

    pairs = stack_pairs_pop(depth=0)
    if not pairs:
        stack_push(3)
        stack_push(2)
        stack_push(1)
        stack_push(0)


def run_button_comma(entry):
    """Run '0' and ',' if no Entry preceded Comma, else dupe Top of Stack"""

    if entry is None:

        if stack_depth() < 1:
            entry_write_char(parms=["0"])
            entry_close_if_open()
        else:

            _x = stack_peek(1, default=0)
            stack_push(_x)


def entry_write_char(parms):
    """Push the first Char, or append a later Char, of an Int or Float Literal"""

    word = parms.pop(0)

    _entry = pop_entry(default="")
    if word != ".":
        entry = _entry + word
    else:
        if not _entry:
            entry = "0."
        elif _entry.endswith("."):
            entry = _entry[:-1]
        else:
            entry = _entry.replace(".", "") + word

    entry += "_"

    stack_push(entry)


def entry_close_if_open():
    """Push the first Char, or append a later Char, of an Int or Float Literal"""

    entry = pop_entry()
    if entry is not None:

        try:
            evalled = int(entry)
        except ValueError:
            evalled = float(entry)

        stack_push(evalled)

    return entry  # not Eval'led


def pop_entry(default=None):
    """Pop the collected Chars and return them, else return the chosen Default"""

    entry = peek_entry(default=None)
    if entry is None:

        return default

    _ = stack_pop(1)

    return entry


def peek_entry(default):
    """Peek the collected Chars and return them, else return the chosen Default"""

    entry = default

    pair = stack_pairs_peek(1)[-1]
    (basename, value) = pair

    if basename is not None:
        if basename.endswith("_"):
            basename_json = json.dumps(basename)
            if basename_json == value:

                evalled = stack_loads(value, default=None)
                assert evalled is not None, repr(value)

                if re.match("^[-+.0-9][-+.0-9Ee]*_$", string=evalled):
                    entry = byo.str_removesuffix(evalled, suffix="_")

    return entry


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byopyvm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
