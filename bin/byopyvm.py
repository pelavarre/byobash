#!/usr/bin/env python3

r"""
usage: byopyvm.py [--help] [WORD ...]

work quickly and concisely, over Dirs of Dirs of Files

positional arguments:
  WORD   a word of command

options:
  --help               show this help message and exit

advanced Bash install:

  alias @='~/Public/byobash/bin/byopyvm.py buttonfile'

  function = {
    : : 'Show Stack, else else do other Stack Work' : :
    if [ "$#" = 0 ]; then
        ~/Public/byobash/bin/byopyvm.py =
    else
        ~/Public/byobash/bin/byopyvm.py "$@"
    fi
  }

quick start:

  git clone https://github.com/pelavarre/byobash.git
  cd byobash/

  function = { ~/Public/byobash/bin/byopyvm.py "$@"; }
  = 12 34 +

  alias @='~/Public/byobash/bin/byopyvm.py buttonfile'
  @ 1 2 , 3 4 +

  source dotfiles/dot.byo.bashrc

examples:

  byopyvm.py  # show these examples and exit
  byopyvm.py --h  # show this help message and exit
  command bin/byopyvm.py --  # show the Advanced Bash Install of ByoPyVm Py and exit

  # Maths

  =  pi
  =  2 *
  =  .

  =  pi 2 * .  # all at once

  # Debugger

  =  pdb.set_trace  # like to follow up with:  stack_peek(0)

  # More sequences of digits and:  / * - + . , pi π i e over pow sqrt √ clear

  =  e i pi * pow  # another calculation
  =  dt.datetime.now dt.datetime.now over -  # dt.timedelta

  =  clear  pow , .  pow pow , .  pow pow , .  2>/dev/null  # 2, 4, 16, ...
  =  clear  / , .    / / , .      / / , .      2>/dev/null  # 0, inf, 0, ...
  =  clear  * , .    * * , .      * * , .      2>/dev/null  # 1, 2, 4, ...
  =  clear  + , .    + + , .      + + , .      2>/dev/null  # 0, 1, 2, ...
  =  clear  - , .    - - , .      - - , .      2>/dev/null  # 1, -1, 1, ...

  =  clear   / / / / /  # 0, 1 0, Inf, 1 Inf, 0, ...  # looping
  =  clear   * * *   # 0, 0 1, 0, ...  # looping
  =  clear   + + +   # 1, 1 0, 1, ...  # looping
  =  clear   - - - - -  # 1, 0 1, -1, 0 -1, 1, ...  # looping
  =  clear   % % % % %  # 9, 9 2, 1, 1 2, 1, ...  # looping
"""

# todo:  # Files and Dirs
# todo:  = ls  # ls -1Frt |tail -4
# todo:  = cp  # cp -ip ... ...~$(date +%m%dpl%H%M%S)~
# todo:  = cp  # cp -ipR .../ ...~$(date +%m%dpl%H%M%S)~
# todo:  = mv  # mv -i ... ...~$(date +%m%dpl%H%M%S)~


import ast
import collections
import importlib
import json
import math
import os
import pathlib
import pdb
import re
import subprocess
import sys
import textwrap
import traceback

import byotools as byo

_ = math
_ = pdb


BUTTONFILE_TESTCHARS = """

    @  # show these examples and exit

    = clear  &&  @  1 2 3 ,  # 123
    = clear  &&  @  3 2 1 π π 4 5 ,  # 345
    = clear  &&  @  . - 1 2 3 ,  # -123

    = clear  &&  @  e  # 2.718...
    = clear  &&  @  . e ,  # 2.718...  # same answer, less directly
    = clear  &&  @  . e 3 ,  # 1000
    = clear  &&  @  . - e 3 ,  # -1000

    = clear  &&  @  i  # 1i
    = clear  &&  @  . i ,  # 1i  # same answer, less directly
    = clear  &&  @  . e 3 i ,  # 1000i

    = clear  &&  @  3 . 2 e - 1 ,  # 0.32

    = clear  &&  @  . ,  . + ,  . - ,  # NaN, Inf, -Inf

    = clear  &&  @  e i pi * pow  # -1
    = clear  &&  @  j , j /  # 1
    = clear  &&  @  j , j *  # -1
    = clear  &&  @  j sqrt  # (0.707+0.707i)

    = clear  &&  @  dt.datetime.now dt.datetime.now over -  # dt.timedelta

    = clear && @ 9 , 2 , . slash  # take Dot Slash as Mod
    = clear && @ 12 . sqrt   # take Dot Sqrt as Square
    = clear && @ 10 e . pow   # take Dot Pow as Log
    = clear && @ . pi  # take Dot Pi as Tau

    = clear && @ 123 456 . clear   # take Dot Clear as Drop
    = clear && @ 123 456 . over    # take Dot Over as Swap

    # sequences chosen from digits and:  / * - + . , pi π i e over pow sqrt √ clear

"""

BUTTONFILE_TESTDOC = textwrap.dedent(BUTTONFILE_TESTCHARS).strip()


#
# Configure
#

BY_NICKNAME = dict(D="decimal", dt="datetime", pd="pandas")  # abbreviate Module Names

EPSILON = 0  # last wins
EPSILON = 1e-15  # say how much to round off to make comparisons come out equal

FILENAME_PRECISION_3 = 3  # 3 digits means mention 'math.pi' as '3.142'

MATH_J = 1j  # work around for Python forgetting to define 'math.j'

SH_J = "j"  # last wins
SH_J = "i"  # choose the Char to mark 'str' of '.imag', from outside r"[-+.012345679Ee]"

STR_PI = "\N{Greek Small Letter Pi}"  # π
STR_SQRT = "\N{Square Root}"  # √
STR_TAU = "\N{Greek Small Letter Tau}"  # τ


#
# Declare how to change the Meaning of a Word by marking the Word
# FIXME: Key Map
#

ALT_BY_WORD = dict(
    clear="drop", over="swap", pi="tau", slash="mod", sqrt="square", pow="log"
)
ALT_BY_WORD["/"] = ALT_BY_WORD["slash"]
ALT_BY_WORD[STR_PI] = ALT_BY_WORD["pi"]


#
# Declare some of how to divide Chars into Words of Python
#


NAME_REGEX = r"[A-Z_a-z][0-9A-Z_a-z]*"
CLOSED_NAME_REGEX = r"^" + NAME_REGEX + r"$"


FULLNAME_REGEX = "({})([.]{})+".format(NAME_REGEX, NAME_REGEX)
CLOSED_FULLNAME_REGEX = r"^" + FULLNAME_REGEX + r"$"


DECINTEGER_REGEX = r"([1-9](_?[0-9])*)|(0(_0)*)"
INT_REGEX = r"[-+]?" + r"({})".format(DECINTEGER_REGEX)
CLOSED_INT_REGEX = r"^" + INT_REGEX + r"$"
# as per 2.4.5 'Integer literals' in Jun/2022 Python 3.10.5 at Docs Python Org
# https://docs.python.org/3/reference/lexical_analysis.html


DIGITPART_REGEX = r"[0-9](_?[0-9])*"
FRACTION_REGEX = r"[.]" + DIGITPART_REGEX
EXPONENT_REGEX = r"[Ee][-+]?" + DIGITPART_REGEX
POINTFLOAT_REGEX_1 = r"({})?{}".format(DIGITPART_REGEX, FRACTION_REGEX)
POINTFLOAT_REGEX_2 = DIGITPART_REGEX + r"[.]"
POINTFLOAT_REGEX = r"({})|({})".format(POINTFLOAT_REGEX_1, POINTFLOAT_REGEX_2)
EXPONENTFLOAT_REGEX = r"(({})|({})){}".format(
    DIGITPART_REGEX, POINTFLOAT_REGEX, EXPONENT_REGEX
)
FLOATNUMBER_REGEX = r"({})|({})".format(POINTFLOAT_REGEX, EXPONENTFLOAT_REGEX)
FLOAT_REGEX = r"[-+]?" + r"({})".format(FLOATNUMBER_REGEX)
CLOSED_FLOAT_REGEX = r"^" + FLOAT_REGEX + "$"
# as per 2.4.6 'Floating point literals' in Jun/2022 Python 3.10.5 at Docs Python Org
# https://docs.python.org/3/reference/lexical_analysis.html


#
# Declare how to accept Chars into Words of Python
#


SIGNABLE_ENTRIES = ("", "+", "-", ".")

OPEN_ENTRIES = ("", "+", "+e", "+j", "-", "-e", "-j", ".", "e", "j")
assert set(SIGNABLE_ENTRIES).issubset(set(OPEN_ENTRIES))

ENTRY_REGEX = r"({}|{})[Jj]?".format(FLOAT_REGEX, INT_REGEX)
CLOSED_ENTRY_REGEX = r"^" + ENTRY_REGEX + r"$"


Q2 = '"'
Q3 = "_"


class ButtonEntry(str):
    """Work like a classic Python Str, but de/serialize differently"""

    def json_dumps(self):
        """Format the Chars of this Str distinctly, apart from how Json Dumps would"""

        dumped = json.dumps(self)
        assert dumped.startswith(Q2) and dumped.endswith(Q2)

        skinless = dumped[len(Q2) :][: -len(Q2)]
        skidded = Q3 + skinless + Q3

        return skidded

    def json_loads(s):
        """Take the S as coming from 'json_dumps', else Raise 'json.JSONDecodeError'"""

        dumped = s

        if not dumped.startswith(Q3) or not dumped.endswith(Q3):

            raise json.JSONDecodeError(msg="not a ButtonEntry", doc=dumped, pos=0)

        skinless = dumped[len(Q3) :][: -len(Q3)]
        loadable = Q2 + skinless + Q2

        loaded = json.loads(loadable)

        return loaded


#
# Run from the Sh Command Line
#


def main():
    """Run from the Sh Command Line"""

    # Start up

    parms = sys.argv[1:]
    main.parms = parms

    collapse_star_parms(parms)

    patchdoc = """

      alias @='~/Public/byobash/bin/byopyvm.py buttonfile'

      function = {
        : : 'Show Stack, else else do other Stack Work' : :
        if [ "$#" = 0 ]; then
            ~/Public/byobash/bin/byopyvm.py =
        else
            ~/Public/byobash/bin/byopyvm.py "$@"
        fi
      }

    """

    # Quit conventionally

    byo.exit_if_patchdoc(patchdoc)  # command byopyvm.py --
    byo.exit_if_testdoc()  # byopyvm.py
    byo.exit_if_argdoc()  # byopyvm.py --help

    # Discard a lead word of "--"

    alt_parms = parms
    if parms and (parms[0] == "--"):
        alt_parms = parms[1:]

    # Run well

    parms_run_some(parms=alt_parms)


def collapse_star_parms(parms):
    """Reconstruct the Sh Input Line despite the presence of '*' as a word"""

    shline = "ls"

    run = byo.subprocess_run_stdio(shline, stdout=subprocess.PIPE)
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


def parms_run_some(parms):
    """Run the Parms = Read a Word, Evaluate the Word, Print the Result, Loop"""

    while parms:
        parms_run_one(parms)
        parms[::] = parms[1:]


def parms_run_one(parms):
    """Run one Parm"""

    # Index Words

    noun_by_word = form_noun_by_word()
    verb_by_word = form_verb_by_word()
    adverb_by_word = form_adverb_by_word()

    # Require each Word found exactly once
    # todo: run this Contradictions Self-Test less often

    keys = list()
    for kvs in (noun_by_word, verb_by_word, adverb_by_word, INK_BY_CHAR):
        keys.extend(kvs.keys())

    contradictions = list()
    for item in collections.Counter(keys).items():
        if item[-1] != 1:
            contradictions.append(item)

    assert not contradictions, contradictions

    # Accept the Word as Given, as Inked, or as Blurred

    parm_0 = parms[0]

    given = parm_0  # the Parm as given, as typed, without correction
    ink = INK_BY_CHAR.get(parm_0)  # such as 'plus' for '+', else None
    blur = to_blurry_word(parm_0)  # such as 'lit_int' for '123', else None

    for word in (given, ink, blur):

        # Call to work with Parms

        if word in adverb_by_word.keys():
            func = adverb_by_word[word]

            func(parms)  # such as the blur of 'parms_lit_int' at '123'

            return

        # Call to work without Parms

        elif word in verb_by_word.keys():
            func = verb_by_word[word]

            value = func()  # such as the ink 'plus' for 'do_plus_y_x' at '+'
            if value is not None:
                stack_push(value)

            return

        # Push a clone of a Noun

        elif word in noun_by_word.keys():
            value = noun_by_word[word]  # such as the ink 'pi' for 'math.pi' at 'π'

            stack_push(value)

            return

    # After all else, then still do fall back to eval as Python

    parms_eval(parms)  # such as when 'parms[0] == "dt.datetime(2038, 1, 19)"'


BLURRY_WORDS = "lit_int lit_float fullname name".split()


def to_blurry_word(word):
    """Say what kind of Input Word this is, else say None"""

    blur = None

    if re.match(CLOSED_INT_REGEX, string=word):
        blur = "lit_int"
    elif re.match(CLOSED_FLOAT_REGEX, string=word):
        blur = "lit_float"
    elif re.match(CLOSED_FULLNAME_REGEX, string=word):
        blur = "fullname"
    elif re.match(CLOSED_NAME_REGEX, string=word):
        blur = "name"

    return blur


def form_ink_by_char():
    """Choose Names for Chars that Python Names reject"""

    by_char = dict()

    by_char[" "] = "space"
    by_char["!"] = "bang"
    by_char['"'] = "quote"
    by_char["#"] = "hash"  # aka a form of "splat"
    by_char["$"] = "buck"
    by_char["%"] = "mod"
    by_char["&"] = "amp"
    by_char["'"] = "tick"
    # by_char["("]  # "in"  # "paren"  # two syllables
    # by_char[")"]  # "out"
    by_char["*"] = "star"  # aka a form of "splat"
    by_char["+"] = "plus"
    by_char[","] = "comma"
    by_char["-"] = "dash"
    by_char["."] = "dot"
    by_char["/"] = "slash"  # commonly misspoken as "backslash"

    by_char["0"] = "zero"  # Decimal Digits alone are not Python Names
    by_char["1"] = "one"
    by_char["2"] = "two"
    by_char["3"] = "three"
    by_char["4"] = "four"
    by_char["5"] = "five"
    by_char["6"] = "six"
    by_char["7"] = "seven"
    by_char["8"] = "eight"
    by_char["9"] = "nine"

    by_char[":"] = "colon"  # two syllables
    by_char[";"] = "semi"  # two syllables
    # by_char["<"]  # "from"  # "angle"  # two syllables
    by_char["="] = "equals"
    # by_char[">"]  # "to"
    by_char["?"] = "query"

    by_char["@"] = "at"

    # by_char["["]  # "bracket"  # two syllables
    by_char["\\"] = "backslant"  # two syllables  # commonly misspoken as "slash"
    # by_char["]"]
    by_char["^"] = "hat"
    by_char["_"] = "skid"  # aka three syllables "underscore"

    by_char["`"] = "backtick"  # two syllables

    # by_char["{"]  # "brace"
    by_char["|"] = "bar"
    # by_char["}"]
    by_char["~"] = "tilde"  # two syllables  # aka "squiggle"

    by_char["\N{Greek Small Letter Pi}"] = "pi"  # π  # STR_PI
    by_char["\N{Greek Small Letter Tau}"] = "tau"  # τ  # STR_TAU
    by_char["\N{Square Root}"] = "sqrt"  # √  # STR_SQRT

    return by_char

    # https://unicode.org/charts/PDF/U0000.pdf  # C0 Controls and Basic Latin
    # http://www.catb.org/jargon/html/A/ASCII.html  # Hacker's Dictionary > Ascii
    # https://www.dourish.com/goodies/jargon.html  # The Original Hacker's Dictionary

    # http://www.forth.org/svfig/Win32Forth/DPANS94.txt  # DPANS'94
    # http://forth.sourceforge.net/std/dpans/  # DPANS'94

    # https://aplwiki.com/wiki/Unicode


INK_BY_CHAR = form_ink_by_char()


#
# Define Verbs
#


def form_noun_by_word():
    """Declare our Built-In Nouns"""

    noun_by_word = dict(
        e=math.e,
        i=MATH_J,  # Sci Folk
        j=MATH_J,  # Eng Folk
        pi=math.pi,  # π  # Classic Folk
        tau=math.tau,  # τ  # Modern Folk
    )

    return noun_by_word


def form_verb_by_word():
    """Declare our Built-In Verbs"""

    verb_by_word = dict(
        clear=do_clear,
        comma=do_comma,
        dash=do_dash_y_x,  # invite Monosyllabic Folk to speak of the '-' Dash
        dot=do_dot,
        drop=do_pop_x,
        equals=do_equals,
        log=do_log_y_x,
        minus=do_dash_y_x,  # invite Calculator Folk to speak of the '-' Minus
        mod=do_mod_y_x,
        over=do_clone_y,
        plus=do_plus_y_x,
        pow=do_pow_y_x,  # this key='pow' is a str, not the 'builtins.pow' Func
        slash=do_slash_y_x,
        sqrt=do_sqrt_x,
        square=do_square_x,
        star=do_star_y_x,
        swap=do_swap_y_x,
    )

    return verb_by_word


def form_adverb_by_word():
    """Declare our Built-In Adverbs"""

    adverb_by_word = dict(
        buttonfile=parms_buttonfile,
        fullname=parms_fullname,
        lit_float=parms_lit_float,
        lit_int=parms_lit_int,
        name=parms_name,
        hash=parms_hash,  # this 'hash' is not the 'builtins.hash'
    )

    return adverb_by_word


#
# Define Sh Verbs of Forth
#


def parms_eval(parms):
    """Eval a Parm (such as a Name or Fullname or other Py)"""

    py = parms[0]

    # Eval

    evalled = stack_eval_once(py)

    # Call with No Args as Evalled, if Evalled as Callable, else Push as Evalled

    pushable = evalled
    if isinstance(evalled, collections.abc.Callable):
        pushable = evalled()

    stack_push(pushable)  # you might next:  stack_peek(0)


def parms_fullname(parms):
    """Eval a Fullname, spoken as ModuleName Dot Name or as DottedModuleName Dot Name"""

    parms_eval(parms)


def parms_lit_float(parms):
    """Eval a Float Literal"""

    str_x = parms[0]
    x = float(str_x)
    stack_push(x)


def parms_lit_int(parms):
    """Eval an Int Literal"""

    str_x = parms[0]
    x = int(str_x)
    stack_push(x)


def parms_name(parms):
    """Eval a Name, spoken as a Nickname without Dots"""

    parms_eval(parms)


def parms_hash(parms):
    """Discard the remaining Parms as Commentary"""  # traditional in Sh at ': '

    parms[::] = list()


#
# Define Calculator Buttons
#


def do_dash_y_x():
    """Push Y - X in place of Y X"""

    if not stack_has_x():
        stack_push(1)  # suggest 0 1 -, else 0 X -
    elif not stack_has_y():
        stack_push(0)
        do_swap_y_x()  # push -X in place of X, when run twice  # a la HP "CHS"
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y - x
        except Exception as exc:  # todo: indeed we could subtract Str, List, Tuple, ...

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_dot():  # kin to Python's '-i' doing nothing after each None result
    """Pop X but print its Value, or do nothing if Stack is Empty"""

    if stack_has_x():
        x = stack_pop(asif_before_rm="cat {} && ")
        print(x)


def do_equals():
    """Show the Keys of the T Z Y X Stack, not its Values"""

    shline = "ls -1Frt |... |tail -4"
    byo.stderr_print("+ {}".format(shline))

    depth = min(4, stack_depth())
    if not depth:
        print()
    else:
        basenames = stack_triples_peek_basenames(depth)
        for basename in basenames:
            print(basename)


def do_mod_y_x():
    """Push Y % X in place of Y X, if X not zeroed"""

    if not stack_has_x():
        stack_push(9)  # suggest  9 2 %, else X 2 %
    elif not stack_has_y():
        stack_push(2)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y % x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_log_y_x():
    """Push Log Base X of Y in place of Y X, by way of 'log(y, x)'"""

    if not stack_has_x():
        stack_push(10)  # suggest 10 e log, else e log
    elif not stack_has_y():
        stack_push(math.e)
    else:

        (y, x) = stack_peek(2)

        base_x = x
        try:
            x_ = math.log(y, base_x)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_pow_y_x():
    """Push Y ** X in place of Y X, by way of 'pow(y, exp=x)'"""

    if not stack_has_x():
        stack_push(2)  # suggest 2 2 **, else 2 **
    elif not stack_has_y():
        stack_push(2)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = pow(y, exp=x)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_plus_y_x():
    """Push Y + X in place of Y X"""

    if not stack_has_x():
        stack_push(1)  # suggest 1 0 +, else 0 +
    elif not stack_has_y():
        stack_push(0)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y + x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_slash_y_x():
    """Push Y / X in place of Y X, and slide into -Inf, NaN, InF when X zeroed"""

    if not stack_has_x():
        stack_push(0)  # suggest  1 0 /, else 1 X /
    elif not stack_has_y():
        stack_push(1)
        do_swap_y_x()  # push (1 / X) in place of X, when run twice  # a la HP "1/X"
    else:

        (y, x) = stack_peek(2)

        if y == x == 0:
            x_ = float("NaN")
        elif x == 0:
            x_ = float("-Inf") if (repr(y).startswith("-")) else float("InF")
        else:

            try:
                x_ = y / x
            except Exception as exc:

                byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_square_x():
    """Push (X ** 2) in place of X"""

    if not stack_has_x():
        stack_push(-0.5)  # suggest -0.5 Square
    else:

        x = stack_peek()

        try:
            x_ = x ** 2
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_sqrt_x():
    """Push (X ** (1 / 2)) in place of X, and slide into Complex when X negative"""

    if not stack_has_x():
        stack_push(-1)  # suggest -1 Sqrt
    else:

        x = stack_peek()

        try:
            x_ = x ** (1 / 2)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_star_y_x():
    """Push Y * X in place of Y X"""

    if not stack_has_x():
        stack_push(0)  # suggest 0 1 *, else 1 *
    elif not stack_has_y():
        stack_push(1)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y * x
        except Exception as exc:

            byo.exit_after_print_exc(exc)

        stack_pop(2)
        stack_push(x_)


#
# Define Stack Ops
#


def do_clear():  # a la GForth "clearstack"
    """Pop X till no more X"""

    stack_triples_pop(depth=0)

    # different than our 'def try_buttonfile_clear'


def do_clone_x():  # a la Forth "DUP", a la HP "Enter"
    """Push X X in place of X"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 Dup
    else:

        x = stack_peek()
        stack_push(x)


def do_clone_y():  # a la Forth "OVER", a la HP "RCL Y"
    """Push Y X Y in place of Y X"""  # chain bin ops at:  Y X  Over %  Over %  ...

    if not stack_has_x():
        stack_push(1)  # suggest:  1 0 Over, else 0 Over
    elif not stack_has_y():
        stack_push(0)
    else:

        (y, x) = stack_peek(2)
        stack_push(y)


def do_pop_x():  # a la Forth "DROP"
    """Pop X if X"""

    if stack_has_x():
        stack_pop()

    # different than our 'def try_buttonfile_drop'


def do_swap_y_x():
    """Drag the 2nd-to-Last Value to Top of Stack"""

    if not stack_has_x():
        stack_push(0)
    elif not stack_has_y():
        stack_push(0)
    else:

        basenames = stack_triples_peek_basenames(2)
        basename = basenames[0]

        shbasename = byo.shlex_dquote(basename)

        shline = "touch {}".format(shbasename)
        if basename.startswith("-"):
            shline = "touch -- {}".format(shbasename)

        byo.stderr_print("+ {}".format(shline))
        byo.subprocess_run_stdio(shline)


def stack_depth():
    """Count the Values in the Stack"""

    triples = stack_triples_peek(0)  # todo: cache vs evalling for depth and to process
    depth = len(triples)

    return depth


def stack_eval_once(py):
    """Eval a Python expression & return its Value, else Stderr Print & Exit Nonzero"""

    by_nickname = dict(D="decimal", dt="datetime", pd="pandas")
    assert by_nickname == BY_NICKNAME

    # Eval the Py

    try:

        evalled = eval(py)

        return evalled

    # Try once to Eval again after inferring 1 Import

    except NameError as exc:

        name = exc.name
        modulename = BY_NICKNAME[name] if (name in BY_NICKNAME.keys()) else name
        if modulename not in sys.modules.keys():

            imported = importlib.import_module(modulename)
            assert imported is sys.modules[modulename], imported
            globals()[name] = imported

            try:

                evalled = eval(py)

                return evalled

            except Exception:

                # Else fuhgeddaboudit

                byo.exit_after_print_raise(exc)

    except UnboundLocalError as exc:  # UnboundLocalError is a Subclass of NameError

        byo.exit_after_print_raise(exc)

    except Exception as exc:

        byo.exit_after_print_raise(exc)

    return evalled


def stack_has_x():
    """Say when the Stack contains one or more Values (that is, when it is Truthy)"""

    has_x = bool(stack_depth())

    return has_x


def stack_has_y():
    """Say when the Stack contains two or more Values"""

    has_y = stack_depth() >= 2

    return has_y


#
# Adapt the Json File Format
#
#   Serialize what 'json.dumps' knows how to serialize
#   Serialize some of what Python Repr knows how to serialize too
#   Give out some of the Basenames that Python Str knows how to choose
#


def stackable_dumps(obj):
    """Format an Object as Chars"""

    by_nickname = dict(D="decimal", dt="datetime", pd="pandas")
    assert by_nickname == BY_NICKNAME

    repr_obj = repr(obj)
    repr_repr_obj = repr(repr_obj)

    # Dump some Types differently than Json would

    if hasattr(obj, "json_dumps"):
        assert isinstance(obj, ButtonEntry), byo.class_mro_join(type(obj))

        dumped = obj.json_dumps()  # such as: '_-1.2e_'

    # Dump any Json Type

    else:
        try:

            dumped = json.dumps(obj)  # such as '"abc"'

        # Dump Complex Obj

        except TypeError:
            if isinstance(obj, complex):

                dumped = repr_obj  # such as:  '(-1+2j)'

            # Dump other Obj's as a Py Sourceline to Eval the Chars of Repr
            # todo:  Repr of Collections.Counter etc omits its ModuleName

            else:
                dumped = "eval({})".format(repr_repr_obj)

                for (nickname, modulename) in BY_NICKNAME.items():
                    prefix = modulename + "."
                    if repr_obj.startswith(prefix):
                        alt_py = nickname + "." + repr_obj[len(prefix) :]
                        alt_repr_repr_obj = repr(alt_py)

                        dumped = "eval({})".format(alt_repr_repr_obj)
                        # such as:  "eval('dt.datetime(2022, 7, 24, 16, 4, 7, 624925)')"

                        break

    return dumped


def stackable_loads_else(s):
    """Unwrap the Object inside the Chars, else return None"""

    dumped = s

    # Load any Json Type

    try:

        loaded = json.loads(dumped)

    except json.JSONDecodeError:

        # Load a Py Sourceline to Eval the Chars of Repr

        prefix = "eval("
        suffix = ")"
        if dumped.startswith(prefix) and dumped.endswith(suffix):
            repr_py = dumped[len(prefix) : -len(suffix)]
            py = ast.literal_eval(repr_py)

            loaded = stack_eval_once(py)

        # Load Complex Values

        else:  # todo:  much too weak reasons to conclude is Rep of Complex
            try:

                loaded = complex(dumped)

            except ValueError:
                try:

                    loaded = ButtonEntry.json_loads(dumped)

                except json.JSONDecodeError:

                    loaded = None  # todo: could:  raise ValueError(dumped)

    return loaded


def stackable_triple(value):
    """Name the Print's of an Object"""

    basename = str(value)
    dumped = stackable_dumps(value)

    if isinstance(value, complex):
        assert not isinstance(value, collections.abc.Container), type(value)

        triple = stackable_triple_of_complex(value)

        return triple

    if isinstance(value, float):
        assert not isinstance(value, collections.abc.Container), type(value)

        triple = stackable_triple_of_float(value)

        return triple

    if isinstance(value, str):  # test Str before trying Container
        assert isinstance(value, collections.abc.Container), type(value)

        basename = value
        triple = (basename, dumped, value)

        return triple

    if isinstance(value, collections.abc.Container):

        basename = byo.class_fullname(type(value))
        triple = (basename, dumped, value)

        return triple

    triple = (basename, dumped, value)

    return triple


def stackable_triple_of_float(value):
    """Give a Basename to Float's, and snap out extreme precision"""

    basename = None
    alt_value = value

    # Give mixed case Basename's to the named Float's

    for str_float in ("-Inf", "NaN", "Inf"):
        if str(value) == str_float.lower():
            basename = str_float

    # Snap Float to Int

    if basename is None:
        int_value = int(value)
        if abs(value - int_value) < EPSILON:
            alt_value = int_value
            basename = str(alt_value)

    # Snap most of the precision out of the Basename

    if basename is None:
        basename = str(round(value, FILENAME_PRECISION_3))

    # Succeed

    assert basename

    alt_dumped = stackable_dumps(alt_value)
    triple = (basename, alt_dumped, alt_value)

    return triple

    # such as '-0.0' to 0, at:  = 0 -1 /
    # such as '...' to 2.0000000000000004 at:  = 2 , sqrt , * -


def stackable_triple_of_complex(value):
    """Give a Basename to Complex'es, and snap out extreme precision"""

    alt_value = value

    # Snap the Complex to Int, in its Real dimension, in its Imag, or in both

    real = value.real
    alt_real = int(real) if (abs(real - int(real)) < EPSILON) else real

    imag = value.imag
    alt_imag = int(imag) if (abs(imag - int(imag)) < EPSILON) else imag

    # Drop the Imag when it bumps against Zero

    if not alt_imag:
        alt_value = alt_real
    elif (alt_real != value.real) or (alt_imag != value.imag):
        alt_value = complex(alt_real, imag=alt_imag)

    # Snap most of the precision out of the Basename

    if not alt_imag:
        basename = str(round(alt_value, FILENAME_PRECISION_3))
    elif not alt_real:
        basename = str(round(alt_value.imag, FILENAME_PRECISION_3)) + SH_J
    else:
        fuzzed_alt_real = round(alt_value.real, FILENAME_PRECISION_3)
        fuzzed_alt_imag = round(alt_value.imag, FILENAME_PRECISION_3)
        fuzzed_alt_value = complex(fuzzed_alt_real, imag=fuzzed_alt_imag)
        basename = str(fuzzed_alt_value).replace("j", SH_J)

    # Succeed

    alt_dumped = stackable_dumps(alt_value)
    triple = (basename, alt_dumped, alt_value)

    return triple

    # such as '(-1+0j)' to -1, at:  = j j *
    # such as '-1+1.2246467991473532e-16' to -1 at:  = e i pi * pow
    # such as '2.220446049250313e-16+1j' to 1j at:  = j sqrt , *


#
# Build a Stack out of Recently Touched Files in Cwd that contain Stackable LoadS
#


def stack_pop(depth=1, asif_before_rm=""):
    """Peek and eval and remove some of the Values most recently pushed"""

    peeks = stack_peek(depth)

    _ = stack_triples_pop(depth, asif_before_rm=asif_before_rm)

    return peeks  # will be 'one_peek' in the corner of 'depth=1'


def stack_peek(depth=1):
    """Peek and eval some of the Values most recently pushed"""

    assert depth >= 0

    alt_depth = depth if depth else stack_depth()

    values = stack_triples_peek_values(alt_depth)

    assert len(values) == alt_depth, (len(values), alt_depth)
    if depth == 1:  # only if 'depth == 1', not also if 'alt_depth == 1'
        one_value = values[-1]

        return one_value  # is 'one_value' in the corner of 'depth=1'

    return values  # is zero, two, or more Values, in the corners of 'depth != 1'


def stack_triples_pop(depth, asif_before_rm=""):
    """Peek and remove some of the Basename-Chars Triples most recently pushed"""

    assert depth >= 0

    # Collect the work to do

    triples = stack_triples_peek(depth)

    paths = list(_[0] for _ in triples)
    shpaths = " ".join(byo.shlex_dquote(_) for _ in paths if _ is not None)
    if shpaths:
        if any(_.startswith("-") for _ in paths):
            shline = "rm -f -- {}".format(shpaths)
        else:
            shline = "rm -f {}".format(shpaths)

        # Trace the work, and do the work

        byo.stderr_print("+ {}{}".format(asif_before_rm.format(shpaths), shline))
        byo.subprocess_run_stdio(shline, stdout=subprocess.PIPE, check=True)

    return triples


def stack_triples_peek_basenames(depth):
    """Peek at some of the Basename's most recently pushed"""

    triples = stack_triples_peek(depth)
    basenames = list(_[0] for _ in triples)  # as if:  (basename, _, _) = triple

    return basenames


def stack_triples_peek_values(depth):
    """Peek at some of the Value's most recently pushed"""

    triples = stack_triples_peek(depth)
    values = list(_[-1] for _ in triples)  # as if:  (_, _, value) = triple

    return values


def stack_triples_peek(depth=1):
    """Peek at some of the Basename-Chars Triples most recently pushed"""

    assert depth >= 0

    # List Filenames by Modified Ascending

    shline = "ls -1art"
    run = byo.subprocess_run_stdio(shline, stdout=subprocess.PIPE, check=True)
    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    filenames = lines

    # Visit each File

    triples = list()

    for filename in filenames:
        path = pathlib.Path(filename)

        chars = None
        if path.is_file():
            try:
                chars = path.read_text()
            except UnicodeDecodeError:
                pass

        if chars is not None:
            dumped = chars.rstrip()  # todo: strip only trailing "\n"?

            if False:
                if filename == "2.718_":
                    pdb.set_trace()

            # Count the File only if it holds an intelligible Value

            peek = stackable_loads_else(dumped)
            if peek is None:  # such as json.JSONDecodeError

                continue

            triple = (str(path), dumped, peek)
            triples.append(triple)

    # Limit the Depth peeked, except reserve Depth 0 to mean No Limit

    if depth:
        triples = triples[-depth:]  # todo: stop evalling more Triples than needed

        assert len(triples) == depth, len(triples)

    return triples


def stack_push(value):
    """Push the Json Chars of a Value, into a new Autonamed File"""

    (basename, dumped, alt_value) = stackable_triple(value)

    stack_push_basename_alt_value(basename, value=value, alt_value=alt_value)


def stack_push_basename_alt_value(basename, value, alt_value):
    """Push the Json Chars of a Value, into a fresh File"""

    # Choose the given Basename, else the next that doesn't already exist

    path = pathlib.Path(basename)

    alt_path = path
    if path.exists():
        alt_path = find_alt_path(path)

    alt_shpath = byo.shlex_dquote(str(alt_path))

    # Trace and run

    alt_dumped = stackable_dumps(alt_value)
    alt_shvalue = byo.shlex_dquote(alt_dumped)

    alt_shcomment = "  # {!r}".format(value) if (repr(alt_value) != repr(value)) else ""

    echo_shline = "echo {} >{}{}".format(alt_shvalue, alt_shpath, alt_shcomment)
    byo.stderr_print("+ {}".format(echo_shline))

    with open(alt_path, "w") as writing:
        writing.write("{}\n".format(alt_dumped))


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


def parms_buttonfile(parms):
    """Take one Double-Click of a Dot-Command ButtonFile"""

    if not parms[1:]:

        print()
        print(BUTTONFILE_TESTDOC)
        print()

        sys.exit(0)  # Exit 0 after printing Help Lines

    while parms[1:]:

        try:

            try_buttonfile(parms)

        except Exception:
            byo.stderr_print()
            traceback.print_exc()
            byo.stderr_print("Press ⌃D TTY EOF to quit\n")

            sys.stdin.read()

            raise

        parms[::] = parms[1:]

        parms.insert(0, "buttonfile")


def try_buttonfile(parms):
    """Run the Name of a Dot-Command ButtonFile, without its Ext, as a Word"""

    assert parms

    # Take the Name of the Filename as the Word of Command, without the Ext

    main_file = parms.pop(1)

    if main_file == "/":  # FIXME: less hack to welcome quick test via extra Parms
        word = main_file
    else:
        basename = os.path.basename(main_file)
        (root, ext) = os.path.splitext(basename)

        word = root if (ext == ".command") else basename

    word = word.casefold()  # Ignore Upper/Lower Case in ButtonFile Names

    # Run the Word

    keyed = try_entry_dot_key_map(word)
    if not keyed:

        moved = try_entry_move_by_word(word)
        if not moved:
            if word == "clear":

                try_buttonfile_clear()  # works in place of 'entry_close_if_open()'

            elif word in (",", "comma"):

                entry = entry_close_if_open()
                if entry is None:
                    do_comma()

            else:

                entry_close_if_open()
                parms_run_some(parms=[word])


def try_entry_dot_key_map(word):
    """Run an Alt Key Map after a leading "." Dot"""

    entry = entry_peek_else()

    if entry == ".":
        alt_word = ALT_BY_WORD.get(word)
        if alt_word is not None:
            byo.stderr_print(
                "byopyvm.py: Easter Egg:  Found {} at Dot {}".format(
                    alt_word.title(), word.title()
                )
            )  # Egg's of Mod Drop Log Square Swap Tau at Slash Clear Pow Sqrt Over Pi

            do_pop_x()  # drop the "." Dot Entry, in place of 'entry_close_if_open()'

            if alt_word == "drop":
                try_buttonfile_drop()
            else:
                parms_run_some(parms=[alt_word])

            return True


def try_entry_move_by_word(word):
    """Return None after closing or dropping the Entry, else return the Open Entry"""

    entry = entry_peek_else()
    signable = entry_is_signable(entry)

    # Edit the Entry in one of many ways

    moved = True

    if entry and (word == "clear"):  # take Clear to empty the Entry, else empty Stack
        entry_write_char("")
    elif (entry is not None) and (word in ("pi", STR_PI)):  # π
        entry_write_char("π")
    elif signable and (word in ("+", "plus")):
        entry_write_char("+")
    elif signable and (word in ("-", "dash", "minus")):
        entry_write_char("-")
    elif word in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
        entry_write_char(word)
    elif (entry is not None) and (word in ("E", "e")):
        entry_write_char("e")
    elif (entry is not None) and (word in ("I", "J", "i", "j")):
        entry_write_char("j")
    elif word in (".", "dot"):
        entry_write_char(".")
    else:

        moved = False

    # Succeed anyhow, but return False after running no Word

    return moved


def entry_is_signable(entry):
    """Say when to take the + - Buttons to Choose Sign"""

    signable_entries = ("", "+", "-", ".")
    assert signable_entries == SIGNABLE_ENTRIES

    open_entries = ("", "+", "+e", "+j", "-", "-e", "-j", ".", "e", "j")
    assert open_entries == OPEN_ENTRIES

    # Sign the SIGNABLE_ENTRIES and the 'fit_before_0' entries that end in 'e'

    signable = False
    if entry is None:
        pass
    elif entry in SIGNABLE_ENTRIES:
        signable = True
    elif entry in OPEN_ENTRIES:
        pass
    elif entry.endswith("e"):
        signable = True
    else:
        pass

    # Say when

    return signable


def try_buttonfile_clear():
    """Pop X till no more X, else push 3, 2, 1, 0"""

    triples = stack_triples_pop(depth=0)
    if not triples:
        stack_push(3)  # suggest:  3 2 1 0 Clear
        stack_push(2)
        stack_push(1)
        stack_push(0)


def try_buttonfile_drop():
    """Pop X if X, else push 0"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 Drop
    else:
        stack_pop()


def do_comma():
    """Open Entry if no Entry open, else dupe Top of Stack"""

    if not stack_has_x():
        entry_write_char("")
    else:
        do_clone_x()  # a la Forth "DUP", a la HP "Enter"


def entry_write_char(ch):
    """Take a Char into the Entry"""

    open_entries = ("", "+", "+e", "+j", "-", "-e", "-j", ".", "e", "j")
    assert open_entries == OPEN_ENTRIES

    # Peek the Entry

    entry = entry_peek_else()

    # Edit the Entry

    edited = entry_take_char(entry, ch=ch)

    # Suggest some AutoCorrection's

    fit_before_0 = edited + "0"

    fit_after_1 = "1" + edited
    if edited[:1] in "+-":
        fit_after_1 = edited[:1] + "1" + edited[1:]

    fit_after_1_before_0 = fit_after_1 + "0"

    # Immediately apply an AutoCorrection at left, if available

    fit = edited
    if edited not in OPEN_ENTRIES:
        if not re.match(CLOSED_ENTRY_REGEX, string=edited):

            if not re.match(CLOSED_ENTRY_REGEX, string=fit_before_0):
                matched = re.match(CLOSED_ENTRY_REGEX, string=fit_after_1_before_0)
                assert matched, (ch, entry, edited, fit_after_1_before_0)

                fit = fit_after_1

    # Add a Strong Mark of the Entry as inviting further input

    value = fit + "_"
    if fit == ".":
        value = "_._"

    # Replace the Entry, else start the Entry

    if entry is not None:
        _ = stack_pop(1)

    stack_push(ButtonEntry(value))


def entry_take_char(entry, ch):
    """Edit the Entry = Take the Ch as an Editor Command for the Entry"""

    editing = "" if (entry is None) else entry

    signable_entries = ("", "+", "-", ".")
    assert signable_entries == SIGNABLE_ENTRIES

    entry_celebrate_egg_found(entry, ch)

    # Work as instructed
    # (already at max C901 Complex 10, until we factor out the +/- and ./e/j work)

    if ch == "":

        edited = ""  # Clear => Drop all Chars

        # Allow Button Clear to drop much stale input

    elif ch == STR_PI:

        edited = editing[:-1]  # π Pi = Delete = Backspace => Drop the last Char

        # Allow π to make no reply, while Entry Empty

    elif ch in ("+", "-"):

        if editing.endswith("e"):
            edited = editing + ch  # Append Ch
        else:
            assert editing in SIGNABLE_ENTRIES, (entry, ch, editing)
            edited = ch  # +, - => Start over with a choice of Sign

        # Allow Buttons "+" and "-" to make no reply, while Entry is "+" or "-"

    elif ch in (".", "e", "j"):

        if ch in editing:
            edited = editing.partition(ch)[0]  # . => Cut back to before Ch
        elif editing == ".":
            assert ch != ".", (entry, ch, editing)
            edited = ch  # Start over with Ch
        else:
            edited = editing + ch  # Append Ch  # may be wrongly after "j" till fixed

        # Allow Button E to drop much stale input

    elif not editing:

        edited = ch  # Start with Ch

    else:

        edited = editing + ch  # Append Ch  # may be wrongly after "j" till fixed

    # Warp the "j" to the far right end, if present, if not there already

    taken = edited
    if "j" in taken:
        taken = edited.replace("j", "") + "j"

    # Succeed

    return taken


def entry_celebrate_egg_found(entry, ch):
    """Celebrate finding an Egg, while editing an Entry"""

    eggs = dict()

    eggs["+"] = "Plus Sign at Dot Plus"
    eggs["-"] = "Minus Sign at Dot Minus"
    eggs["e"] = "Exp at Dot E"
    eggs["j"] = "Imag at Dot J"
    eggs[STR_PI] = "Delete at Dot Pi"

    if ch in eggs.keys():
        egg = eggs[ch]
        byo.stderr_print("byopyvm.py: Easter Egg:  Found {}".format(egg))


def entry_close_if_open():
    """Return an Unevalled Copy of the Entry, but replace it with its Eval"""

    # Report either of the two kinds of Got No Entry

    if not stack_has_x():  # Empty Stack

        return None

    entry = entry_peek()  # Top of Stack is Not an Entry
    if entry is None:

        return None

    # Eval the Entry

    evalled = entry_eval(entry)

    # Celebrate finding an Egg

    eggs = dict()

    eggs[""] = "None at Dot Comma"
    eggs["+"] = "Inf at Dot Plus Comma"
    eggs["-"] = "-Inf at Dot Minus Comma "
    eggs["."] = "NaN at Dot Comma"

    if entry in eggs.keys():
        egg = eggs[entry]
        assert str(evalled).casefold() == egg.split()[0].casefold(), (evalled, egg)
        byo.stderr_print("byopyvm.py: Easter Egg:  Found {}".format(egg))

    # Replace the Entry with its Evaluation, except discard an Empty Entry

    _ = stack_pop(1)
    if evalled is not None:
        stack_push(evalled)

    # Return an Unevalled Copy of the Entry

    return entry


def entry_eval(entry):
    """Eval an Entry"""

    open_entries = ("", "+", "+e", "+j", "-", "-e", "-j", ".", "e", "j")
    assert open_entries == OPEN_ENTRIES

    # Eval all the OPEN_ENTRIES that the Python 'complex' Func has rejected

    by_entry = dict()

    by_entry[""] = None
    by_entry["+"] = float("Inf")
    by_entry["+e"] = math.e
    assert complex("+j") == 1j
    by_entry["-"] = float("-Inf")
    by_entry["-e"] = -math.e
    assert complex("-j") == -1j
    by_entry["."] = float("NaN")
    by_entry["e"] = math.e
    assert complex("j") == 1j

    if entry in by_entry.keys():

        evalled = by_entry[entry]

        return evalled

    # Ask Python to eval the Entry, else append a "0" to autocomplete the Entry

    evalled = None

    fit_before_0 = entry + "0"
    for fitted in (entry, fit_before_0):

        evalled = None
        try:
            evalled = int(fitted)  # covers CLOSED_REGEX_INT
        except ValueError:
            try:
                evalled = float(fitted)  # covers CLOSED_REGEX_FLOAT
            except ValueError:
                try:
                    evalled = complex(fitted)  # covers "+j", "-j", and "j"
                except ValueError:
                    occasion = (fitted, entry, fit_before_0)
                    assert fitted == entry != fit_before_0, occasion

                    continue

        break

    # Succeed
    # Accept the whole precise eval, don't snap off excess precision till next Sh Word

    return evalled


def entry_peek_else():
    """Peek the collected Chars and return them, else return None"""

    entry = None
    if stack_has_x():
        entry = entry_peek()

    return entry


def entry_peek():
    """Peek the collected Chars and return them"""

    # Peek from the Top of Stack

    if stack_has_x():

        triple = stack_triples_peek()[-1]
        (basename, dumped, value) = triple

        # Peek only if the Basename ends with '_' and was Dumped

        if basename is not None:
            if basename.endswith("_"):
                basename_json = stackable_dumps(ButtonEntry(basename))
                if basename_json == dumped:

                    # Remove the Strong Mark of the Entry as inviting further input

                    entry = byo.str_removesuffix(value, suffix="_")
                    if value == "_._":
                        entry = "."

                    # Test that any Entry inviting further input is evallable

                    evalled = entry_eval(entry)
                    if entry == "":
                        assert evalled is None, (entry, evalled)
                    else:
                        assert evalled is not None, (entry, evalled)

                    # Succeed

                    return entry


#
# Track dreams
#


# FIXME: add Bits alongside Decimal Int and Decimal Float and Decimal Complex

# FIXME: add our TestDoc and our Button TestDoc here into Make SelfTest


_ = """

todo:  . , should be : because no longer NaN
todo:  . √ should be Log2 because no longer X*X

main key map

      i      pi  7  8   9   /
     OVER    e   4  5   6   *
            POW  1  2   3   -
    CLEAR    √   0  .  DUP  +

dot key map - stacked as Entry .

          IMAG  TAU/DEL      7       8      9             MOD/SLASH
     SWAP/OVER  LN/EXP       4       5      6             LOG10/STAR
                LOGYX/POW    1       2      3             NEG/MINUS
     DROP/WIPE  LOG2/SQRT    0  BASE/.  :/-INF/INF/COMMA  POS/PLUS

dot comma key map - stacked as Entry :

     NAN   INT-FRAC  7  8  9  1/X
     DUP2    E**X    4  5  6  10**X
             Y.LAST  1  2  3  0-X
    DROP2     2**X   0  .  COMMA  X.LAST

"""

_ = """

leading data type for the result
trailing data type for the op

bits = hex, oct, or bin

= '~'
= '&'
= '|'
= '>>'
= '<<'
= ^

= -i  # for interactive CLI, till ⌃D Tty Eof
@ -i  # for interactive CLI, till ⌃D Tty Eof

"""

_ = """

dot dot ... to visit each base:  to-hex, to-dec, to-oct, to-bin
except skip the to- where we already are, so first strike is always to-hex else to-dec

# dot dot ... to-hex, to-dec, to-oct, to-bin

conversions to Bits first dupe as floor Decimal Int, if given Complex or Float
    except is it Ceiling when negative?

bits / to shift right >>
bits * to shift left <<
bits + for bits |
bits - for bits ~ &

bits sqrt for bits ~
bits pow for bits ^

bits dot / to rotate right & >> |
bits dot * to rotate left & << |
bits dot sqrt for 0 bits -
bits dot pow for 0 bits - &

no hurry on the A B C D E F keys - first class, not mapped

"""

_ = """

i've long forgotten what a complex sqrt is ...

same thing in a TUI, TUI in a GShell
--tui paper tape
main.stderr

add an Undo Button

= requests.get http://...
work with Files and Dirs, not just Maths
go with 'decimal.Decimal' over 'float'
consider '^' for 'pow' for decimal Int/ Float/ Decimal

factor the common code out from:  / * - +
refresh the 'macos/.DS_Store' often enough
    even though i often feel i have to log out to flush the Finder Cache of it

"""


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byopyvm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
