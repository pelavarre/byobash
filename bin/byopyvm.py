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

  open macos/

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

  # More usage of:  / * - + . , pi π i e over pow sqrt √ clear

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
import datetime as dt
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

DEFAULT_NONE = None

_ = math
_ = pdb


BUTTONFILE_TESTCHARS = """

    @  # show these examples and exit

    # usage:  / * - + . , pi π i e over pow sqrt √ clear

    = clear  &&  @  1 2 3 ,  # 123
    = clear  &&  @  3 2 1 π π 4 5 ,  # 345
    = clear  &&  @  . - 1 2 3 ,  # -123

    = clear  &&  @  e  # 2.718...
    = clear  &&  @  1 e 3 ,  # 1000
    = clear  &&  @  . - e 3 ,  # -1000

    = clear  &&  @  i  # 1i
    = clear  &&  @  1 e 3 i ,  # 1000i
    = clear  &&  @  0 , 1 - 0 /  j *  # (NaN-Infi)

    = clear  &&  @  3 . 2 e - 1 ,  # 0.32

    = clear  &&  @  0 , 0 /  1 , 0 /   0 , 1 - 0 /  # NaN, Inf, -Inf

    = clear  &&  @  i  # 1j
    = clear  &&  @  e i pi * pow  # -1
    = clear  &&  @  i , i /  # 1
    = clear  &&  @  i , i *  # -1
    = clear  &&  @  i sqrt  # (0.707+0.707i)

    = clear  &&  @  dt.datetime.now dt.datetime.now over -  # dt.timedelta

    # 11 Easter Eggs at Dot Buttons

    = clear  &&  @  e i pi * +  . i  =  # 2.718  # because Dot Real
    = clear  &&  @  e i  . over  =  # i e  # because Dot Swap X Y
    = clear  &&  @  e i  . clear  =  # e  # because Dot Drop X

    = clear  &&  @  10 . - 3 pow  . pi  =  # -3  # because Dot Log 10 X
    = clear  &&  @  pi 2 pow  pi . pow  =  # 2  # because Dot Log Y X
    = clear  &&  @  e . - 1 pow  . e  =  # -1  # because Dot Log E X
    = clear  &&  @  2 , . - 5 pow  . sqrt  =  # -5  # because Dot Log 2 X

    = clear  &&  @  9 , 2 ,  . /  =  # 4  # because Dot // Slash Slash Floor Division
    = clear  &&  @  9 , 2 ,  . *  =  # 1  # because Dot % Mod
    = clear  &&  @  . - 7 ,  =  # -7  # because Dot - Negative Sign
    = clear  &&  @  . + 8 ,  =  # 8  # because Dot + Positive Sign

    # 10 Easter Eggs at Dot Comma Buttons

    = clear  &&  @  e i pi * +  . , i  =  # 3.142  # because Dot Comma Imag
    = clear  &&  @  0 , 1 , 2 , 3 ,  . , over  =  # 0 2 3 1  # because Dot Comma Rot Y X Z
    = clear  &&  @  0 , 1 , 2 , 3 ,  . , clear  =  # 0 2  # because Dot Comma Drop Y X

    = clear  &&  @  . - 3 ,  . , pi  =  # 0.001  # because Dot Comma 10 X **
    = clear  &&  @  . - 1 ,  . , e  =   # 0.001  # because Dot Comma E X **
    = clear  &&  @  64 ,  . , sqrt  =  # 18446744073709551616  # Dot Comma 2 X **

    = clear  &&  @  i  . , /  =  # -1j  # because Dot Comma 1 X /
    = clear  &&  @  i  . , *  =  # -1  # because Dot Comma X X *
    = clear  &&  @  . - i ,  . , -  =  # 1j  # because Dot Comma 0 X -
    = clear  &&  @  . + i ,  . , +  =  # 1j  # because Dot Comma X Abs

    # Easter Eggs at Modular Int Buttons

    = clear  &&  @  15 16  . , pow  # FIXME  # because Dot Comma Y X Base

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
# Declare some of how to divide Chars into Words of Python
#


NAME_REGEX = r"[A-Z_a-z][0-9A-Z_a-z]*"
CLOSED_NAME_REGEX = r"^" + NAME_REGEX + r"$"  # FIXME: call 're.fullmatch' on Open RegEx


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


OPEN_ENTRIES = ("", "+", "+e", "+j", ",", "-", "-e", "-j", ".", "e", "j")

BLURRY_ENTRIES = ("", "+", ",", "-", ".")
DROPPABLE_ENTRIES = ("", "+", ",", "-", ".")
FORKABLE_ENTRIES = (",", ".")
SIGNABLE_ENTRIES = ("", "+", "-", ".")

assert set(DROPPABLE_ENTRIES).issubset(set(OPEN_ENTRIES))
assert set(FORKABLE_ENTRIES).issubset(set(OPEN_ENTRIES))
assert set(SIGNABLE_ENTRIES).issubset(set(OPEN_ENTRIES))

ENTRY_REGEX = r"({}|{})[Jj]?".format(FLOAT_REGEX, INT_REGEX)
CLOSED_ENTRY_REGEX = r"^" + ENTRY_REGEX + r"$"


Q2 = '"'
Q3 = "_"


class StackableTriple(
    collections.namedtuple("StackableTriple", "name code obj".split())
):
    """Collect the 3 Takes on an Object:  its Filename, Serialization, and Self"""


class ButtonEntry(str):
    """Work like a classic Python Str, but de/serialize differently"""

    def stackable_dumps(self):
        """Format the Chars of this Str distinctly, apart from how Json Dumps would"""

        code = json.dumps(self)
        assert code.startswith(Q2) and code.endswith(Q2)

        skinless = code[len(Q2) :][: -len(Q2)]
        skidded = Q3 + skinless + Q3

        return skidded

    @classmethod
    def stackable_loads(cls, s):
        """Take the S as coming from 'json_dumps', else Raise 'json.JSONDecodeError'"""

        code = s

        if not code.startswith(Q3) or not code.endswith(Q3):

            raise json.JSONDecodeError(msg="not a ButtonEntry", doc=code, pos=0)

        skinless = code[len(Q3) :][: -len(Q3)]
        loadable = Q2 + skinless + Q2

        obj = json.loads(loadable)

        return obj


#
# Declare how to work with Modular Int's
#


class ModularInt:
    def __init__(self, bits, base, width):
        self.bits = bits
        self.base = base
        self.width = width


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
    ink = INK_BY_CHAR.get(parm_0, DEFAULT_NONE)  # such as 'plus' for '+'
    blur = to_blurry_word(parm_0, default=None)  # such as 'lit_int' for '123'

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

    parms_pyish(parms)  # such as:  dt.date dt.date:2022,4,8 -


BLURRY_WORDS = "lit_int lit_float fullname name".split()


def to_blurry_word(word, default):
    """Say what kind of Input Word this is, else say None"""

    blur = default  # often None

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

    by_char["//"] = "slash_slash"  # kin to Forth SlashMod

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
        j=MATH_J,
        pi=math.pi,
        tau=math.tau,
    )

    more = dict(
        i=MATH_J,
    )

    noun_by_word.update(more)

    return noun_by_word


def form_verb_by_word():
    """Declare our Built-In Verbs"""

    verb_by_word = dict(
        abs=do_abs_x,  # this key='abs' is a str, not the 'builtins.abs' Func
        base=do_base_y_x,
        clear=do_clear,
        comma=do_comma,
        dash=do_dash_y_x,
        dot=do_dot,
        drop=do_pop_x,
        drop2=do_pop_y_x,
        equals=do_equals,
        log=do_log_y_x,
        ln=do_log_e_x,
        mod=do_mod_y_x,
        over=do_clone_y,
        plus=do_plus_y_x,
        pow=do_pow_y_x,  # this key='pow' is a str, not the 'builtins.pow' Func
        rot=do_rot_y_x_z,
        slash=do_slash_y_x,
        slash_slash=do_slash_slash_y_x,  # kin to Forth SlashMod
        sqrt=do_sqrt_x,
        square=do_square_x,
        star=do_star_y_x,
        swap=do_swap_x_y,
    )

    more = dict(
        minus=do_dash_y_x,
    )

    verb_by_word.update(more)

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


def parms_pyish(parms):
    """Eval some incomplete Python Parm, such as 'dt.date' or 'dt.date:2022,4,8'"""

    pyish = parms[0]

    #

    funcname = pyish.partition(":")[0]
    is_name = re.fullmatch(FULLNAME_REGEX, string=funcname)
    is_name = is_name or re.fullmatch(NAME_REGEX, string=funcname)

    if not is_name:

        parms_eval(parms)

        return

    #

    tail = pyish.partition(":")[-1]

    shargs = list()
    if tail:
        shargs = tail.split(",")

    args = list()
    for sharg in shargs:
        try:
            arg = ast.literal_eval(sharg)
        except KeyboardInterrupt:
            arg = sharg

        args.append(arg)

    if not args:
        if funcname == "dt.date":
            now = dt.datetime.now()
            args = [now.year, now.month, now.day]

    py = "{}({})".format(funcname, ", ".join(repr(_) for _ in args))
    if py != pyish:
        parms[0] = py  # todo: don't mutate?

        byo.stderr_print("+ = {!r}".format(py))  # todo: quote Str well

    parms_eval(parms)


def parms_eval(parms):
    """Eval some complete Python Parm (such as a Name or other Py Fragment)"""

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

    parms_pyish(parms)


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

    parms_pyish(parms)


def parms_hash(parms):
    """Discard the remaining Parms as Commentary"""  # traditional in Sh at ': '

    parms[::] = list()


#
# Define the Button Files of our Calculator Folder
#


def do_dash_y_x():
    """Push Y - X in place of Y X"""

    if not stack_has_x():
        stack_push(1)  # suggest 0 1 -, else 0 X -
    elif not stack_has_y():
        stack_push(0)
        do_swap_x_y()  # push -X in place of X, when run twice  # a la HP "CHS"
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
        x = stack_pop(asif_before_rm="cat {} && ")  # FIXME, return None from Stack_Pop
        print(x)


def do_equals():
    """Show the Keys of the T Z Y X Stack, not its Values"""

    shline = "ls -1Frt |... |tail -4"
    byo.stderr_print("+ {}".format(shline))

    depth = min(4, stack_depth())
    if not depth:
        print()
    else:
        names = stack_triples_peek_names(depth)
        for name in names:
            print(name)


def do_mod_y_x():
    """Push Y % X in place of Y X, if X not zeroed"""  # todo: what if zeroed

    if not stack_has_x():
        stack_push(9)  # suggest  9 2 %, else X 2 %
    elif not stack_has_y():
        stack_push(2)
    else:

        (y, x) = stack_peek(2)

        if y == x == 0:
            x_ = float("NaN")
        elif x == 0:
            x_ = float("-Inf") if (y < 0) else float("InF")
        else:

            try:
                x_ = y % x
            except Exception as exc:

                byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_log_y_x():
    """Push Log Base X of Y in place of Y X, by way of 'log(y, base_x)'"""

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
        do_swap_x_y()  # push (1 / X) in place of X, when run twice  # a la HP "1/X"
    else:

        (y, x) = stack_peek(2)

        if y == x == 0:
            x_ = float("NaN")
        elif x == 0:
            x_ = float("-Inf") if (y < 0) else float("InF")
        else:

            try:
                x_ = y / x  # Python True Division
            except Exception as exc:

                byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_slash_slash_y_x():  # kin to Forth SlashMod
    """Push Y // X in place of Y X, if X not zeroed"""  # todo: what if zeroed

    if not stack_has_x():
        stack_push(9)  # suggest  9 2 //, else X 2 //
    elif not stack_has_y():
        stack_push(2)
    else:

        (y, x) = stack_peek(2)

        if y == x == 0:
            x_ = float("NaN")
        elif x == 0:
            x_ = float("-Inf") if (y < 0) else float("InF")
        else:

            try:
                x_ = y // x  # Python Floor Division
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
            x_ = x**2
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
# Define the Button Filenames mentioned by 'macos/README.md'
#


def try_docs_button(word):
    """Run Buttons as sketched in Doc, even while not shipping deployed in Folder"""

    docs_defs = dict()  # todo: move out of Easter Eggs

    docs_defs["y↑x"] = do_pow_y_x
    docs_defs[".real"] = do_real_x
    docs_defs[".imag"] = do_imag_x

    # Run the hidden Egg, if found

    if word in docs_defs.keys():

        func = docs_defs[word]
        alt_word = func.__name__
        byo.stderr_print(
            "byopyvm.py: Easter Egg:  Found {} at {}".format(
                alt_word.title(), word.title()
            )
        )

        func()

        return True


#
# Define the Dot Button Files of our Calculator Folder, after a press of Dot
#


def try_dot_button(word):
    """Run differently while the Entry is just the '.' Dot"""

    # Quit unless an Entry Open as just the '.' Dot

    entry = entry_peek_else(default=None)
    if entry != ".":

        return

    # Hide 9 Easter Eggs

    dot_defs = dict(  # FIXME: move these to compile time
        i=do_real_x,
        j=do_real_x,
        over=do_swap_x_y,
        clear=try_buttonfile_drop_x,
        pi=do_log_10_x,
        e=do_log_e_x,
        pow=do_log_y_x,  # this key='pow' is a str, not the 'builtins.pow' Func
        sqrt=do_log_2_x,
        slash=do_slash_slash_y_x,
        star=do_mod_y_x,
    )

    dot_defs["*"] = dot_defs["star"]
    dot_defs["/"] = dot_defs["slash"]

    dot_defs[STR_PI] = dot_defs["pi"]
    dot_defs[STR_SQRT] = dot_defs["sqrt"]

    # Run the hidden Egg, if found

    if word in dot_defs.keys():
        do_pop_x()  # drop the "." Dot Entry, in place of 'entry_close_if_open()'

        func = dot_defs[word]
        alt_word = func.__name__
        byo.stderr_print(
            "byopyvm.py: Easter Egg:  Found {} at Dot {}".format(
                alt_word.title(), word.title()
            )
        )

        func()

        return True


def do_real_x():
    """Push the Real part of the Complex X"""

    if not stack_has_x():
        stack_push(math.e + (1j * math.pi))  # suggest:  j π * e +
    else:

        x = stack_peek()

        try:
            x_ = complex(x)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_.real)


def do_log_10_x():
    """Push Log Base 10 of X in place of X, by way of 'log(x, base_10)'"""

    if not stack_has_x():
        stack_push(math.e)  # suggest the e of:  e 10 log
    else:

        x = stack_peek()

        base_10 = 10
        try:
            x_ = math.log(x, base_10)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_log_e_x():
    """Push Log Base E of X in place of X, by way of 'log(x)'"""

    if not stack_has_x():
        stack_push(10)  # suggest the 10 of:  10 e log
    else:

        x = stack_peek()

        try:
            x_ = math.log(x)  # implicit ', base_e'
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_log_2_x():
    """Push Log Base 2 of X in place of X, by way of 'log(x, base_2)'"""

    if not stack_has_x():
        stack_push(10)  # suggest the 10 of:  10 2 log
    else:

        x = stack_peek()

        base_2 = 2
        try:
            x_ = math.log(x, base_2)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


#
# Define the Dot Comma Button Files of our Calculator Folder, after a press of Dot Comma
#


def try_comma_button(word):
    """Run differently while the Entry is just the ',' Comma"""

    # Quit unless an Entry Open as just the ',' Comma

    entry = entry_peek_else(default=None)
    if entry != ",":

        return

    # Hide 10 Easter Eggs

    comma_defs = dict(  # FIXME: move these to compile time
        dash=do_negate_x,
        i=do_imag_x,
        j=do_imag_x,
        over=do_rot_y_x_z,
        clear=try_buttonfile_drop_y_x,
        pi=do_pow_10_x,
        e=do_pow_e_x,
        pow=do_base_y_x,  # this key='pow' is a str, not the 'builtins.pow' Func
        sqrt=do_pow_2_x,
        slash=do_slash_1_x,
        star=do_square_x,
        minus=do_negate_x,
        plus=do_abs_x,
    )

    comma_defs["*"] = comma_defs["star"]
    comma_defs["/"] = comma_defs["slash"]
    comma_defs["-"] = comma_defs["minus"]
    comma_defs["+"] = comma_defs["plus"]

    comma_defs[STR_PI] = comma_defs["pi"]
    comma_defs[STR_SQRT] = comma_defs["sqrt"]

    # Run the hidden Egg, if found

    if word in comma_defs.keys():
        do_pop_x()  # drop the "," Comma Entry, in place of 'entry_close_if_open()'

        func = comma_defs[word]
        alt_word = func.__name__
        byo.stderr_print(
            "byopyvm.py: Easter Egg:  Found {} at Dot Comma {}".format(
                alt_word.title(), word.title()
            )
        )

        func()

        return True


def do_imag_x():
    """Push the Imag part of the Complex X"""

    if not stack_has_x():
        stack_push(math.e + (1j * math.pi))  # suggest:  j π * e +
    else:

        x = stack_peek()

        try:
            x_ = complex(x)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_.imag)


def do_pow_10_x():
    """Push (X ** 10) in place of X"""

    if not stack_has_x():
        stack_push(-1)  # suggest -1 Pow 10 X
    else:

        x = stack_peek()

        try:
            x_ = 10**x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_pow_e_x():
    """Push (X ** E) in place of X"""

    if not stack_has_x():
        stack_push(-1)  # suggest -1 Pow E X
    else:

        x = stack_peek()

        try:
            x_ = math.exp(x)  # todo: compare vs 'math.e ** x'
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_pow_2_x():
    """Push (X ** 2) in place of X"""

    if not stack_has_x():
        stack_push(-1)  # suggest -1 Pow 10 X
    else:

        x = stack_peek()

        try:
            x_ = 2**x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_slash_1_x():
    """Push (1 / X) in place of X"""

    if not stack_has_x():
        stack_push(-1)  # suggest 1 -1 /
    else:

        x = stack_peek()

        try:
            x_ = 1 / x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_negate_x():
    """Push -X in place of X"""

    if not stack_has_x():
        stack_push(1)  # suggest 1 -1 *
    else:

        x = stack_peek()

        try:
            x_ = -x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


def do_abs_x():
    """Push ABS(X) in place of X"""

    if not stack_has_x():
        stack_push(-1)  # suggest -1 Abs
    else:

        x = stack_peek()

        try:
            x_ = abs(x)
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop()
        stack_push(x_)


#
# Work with Based Ints
#


def do_base_y_x():
    assert False


#
# Define the Button Files of our Calculator Folder, after a push of ModularInt
#


def try_bits_button(word):
    """Run differently while Top of Stack is a ModularInt"""

    # Quit unless Top of Stack is a ModularInt

    entry = entry_peek_else(default=None)
    if entry is not None:

        return

    if not stack_has_x():

        return

    x = stack_peek()
    if not isinstance(x, ModularInt):

        return

    # Hide 9 Easter Eggs

    bits_defs = dict(
        i=do_weigh_x,
        pi=do_shrink_x,
        e=do_grow_x,
        pow=do_int_x,  # this key='pow' is a str, not the 'builtins.pow' Func
        sqrt=do_flip_x,
        slash=do_hat_y_x,
        star=do_amp_y_x,
        minus=do_amp_flip_y_x,
        plus=do_bar_x,
    )

    # Run the hidden Egg, if found

    if word in bits_defs.keys():

        func = bits_defs[word]
        alt_word = func.__name__
        byo.stderr_print(
            "byopyvm.py: Easter Egg:  Found {} at Bits {}".format(
                alt_word.title(), word.title()
            )
        )

        func()

        return True


def do_weigh_x():
    assert False


def do_shrink_x():
    assert False


def do_grow_x():
    assert False


def do_int_x():
    assert False


def do_flip_x():
    assert False


def do_hat_y_x():
    assert False


def do_amp_y_x():
    assert False


def do_amp_flip_y_x():
    assert False


def do_bar_x():
    assert False


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
        stack_push(1)  # suggest:  1 0 Over, else Y 0 Over
    elif not stack_has_y():
        stack_push(0)
    else:

        (y, x) = stack_peek(2)
        stack_push(y)


def do_pop_x():  # a la Forth "DROP"
    """Pop X if X"""

    if stack_has_x():
        stack_pop()

    # different than our 'def try_buttonfile_drop_x'


def do_pop_y_x():  # a la Forth "2DROP" kin to 2DUP, 2OVER, 2SWAP
    """Pop X if X"""

    if stack_has_y():  # todo: think more about 'def do_pop_y_x' after 1 Push, not 0
        stack_pop(2)

    # different than our 'def try_buttonfile_drop_y_x'


def do_rot_y_x_z():
    """Drag the 3rd-to-Last Value to Top of Stack"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 1 2 Rot, else 1 2 Rot, else 2 Rot
    elif not stack_has_y():
        stack_push(1)
    elif not stack_has_z():
        stack_push(2)
    else:

        names = stack_triples_peek_names(3)
        name = names[0]  # the Z File

        shname = byo.shlex_dquote(name)

        shline = "touch {}".format(shname)
        if name.startswith("-"):
            shline = "touch -- {}".format(shname)

        byo.stderr_print("+ {}".format(shline))
        byo.subprocess_run_stdio(shline)


def do_swap_x_y():
    """Drag the 2nd-to-Last Value to Top of Stack"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 1 Swap, else Y 0 Swap
    elif not stack_has_y():
        stack_push(1)
    else:

        names = stack_triples_peek_names(2)
        name = names[0]  # the Y File

        shname = byo.shlex_dquote(name)

        shline = "touch {}".format(shname)
        if name.startswith("-"):
            shline = "touch -- {}".format(shname)

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

            try:
                imported = importlib.import_module(modulename)
            except Exception:

                byo.exit_after_print_raise(exc)

            assert imported is sys.modules[modulename], imported
            globals()[name] = imported

            try:

                evalled = eval(py)

            except Exception:

                byo.exit_after_print_raise(exc)

            return evalled

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


def stack_has_z():
    """Say when the Stack contains three or more Values"""

    has_z = stack_depth() >= 3

    return has_z


#
# Adapt the Json File Format
#
#   Serialize what 'json.dumps' knows how to serialize
#   Serialize some of what Python Repr knows how to serialize too
#   Give out some of the Filename Basenames that Python Str knows how to choose
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

        code = obj.stackable_dumps()  # such as: '_-1.2e_'

    # Dump any Json Type

    else:
        try:

            code = json.dumps(obj)  # such as '"abc"'

        # Dump Complex Obj

        except TypeError:
            if isinstance(obj, complex):

                code = repr_obj  # such as:  '(-1+2j)'

            # Dump other Obj's as a Py Sourceline to Eval the Chars of Repr
            # todo:  Repr of Collections.Counter etc omits its ModuleName

            else:
                code = "eval({})".format(repr_repr_obj)

                for (nickname, modulename) in BY_NICKNAME.items():
                    prefix = modulename + "."
                    if repr_obj.startswith(prefix):
                        alt_py = nickname + "." + repr_obj[len(prefix) :]
                        alt_repr_repr_obj = repr(alt_py)

                        code = "eval({})".format(alt_repr_repr_obj)
                        # such as:  "eval('dt.datetime(2022, 7, 24, 16, 4, 7, 624925)')"

                        break

    return code


def stackable_loads_else(s, default):
    """Unwrap the Object inside the Chars, else return None"""

    code = s

    # Load any Json Type

    try:

        obj = json.loads(code)

    except json.JSONDecodeError:

        # Load a Py Sourceline to Eval the Chars of Repr

        prefix = "eval("
        suffix = ")"
        if code.startswith(prefix) and code.endswith(suffix):
            repr_py = code[len(prefix) : -len(suffix)]
            py = ast.literal_eval(repr_py)

            obj = stack_eval_once(py)

        # Load Complex Values

        else:  # todo:  much too weak reasons to conclude is Rep of Complex
            try:

                obj = complex(code)

            except ValueError:
                try:

                    obj = ButtonEntry.stackable_loads(code)

                except json.JSONDecodeError:

                    obj = default

    return obj


def stackable_triple(obj):
    """Form the 3 Takes on an Object:  its Filename, Serialization, & Self"""

    # Work differently for Complex or Float

    if isinstance(obj, complex):
        assert not isinstance(obj, collections.abc.Container), type(obj)

        triple = stackable_triple_from_complex(obj)

        return triple

    if isinstance(obj, float):
        assert not isinstance(obj, collections.abc.Container), type(obj)

        triple = stackable_triple_from_float(obj)

        return triple

    # Work differently for Container, except Not differently for Str

    if not isinstance(obj, str):
        if isinstance(obj, collections.abc.Container):

            name = byo.class_fullname(type(obj))
            code = stackable_dumps(obj)
            triple = StackableTriple(name, code=code, obj=obj)

            return triple

    # Fall back on to the naive choices

    name = str(obj)  # the Look of the Self
    code = stackable_dumps(obj)  # Code for Cloning the Self, like a Repr for Json
    triple = StackableTriple(name, code=code, obj=obj)

    return triple


def stackable_triple_from_complex(obj):
    """Give a Basename to Complex'es, and snap out Extreme Precision"""

    abs_imag_triple = stackable_triple_from_float(obj=obj.imag)
    real_triple = stackable_triple_from_float(obj=obj.real)

    # Forward Real without Imag

    imag = abs_imag_triple.obj
    if not imag:

        return real_triple

    # Else forward Imag without Real

    real = real_triple.obj
    if not real:

        brief = abs_imag_triple.obj * 1j
        code = stackable_dumps(brief)
        name = "{}j".format(abs_imag_triple.name)

        triple = StackableTriple(name, code=code, obj=brief)

        return triple

    # Else forward Real with Imag

    brief = complex(real, imag=imag)

    code = str(brief)

    name = "({}+{}j)".format(real_triple.name, abs_imag_triple.name)
    if abs_imag_triple.name.startswith("-"):
        name = "({}{}j)".format(real_triple.name, abs_imag_triple.name)

    alt_name = name  # such as '(nan-infj)'
    alt_name = alt_name.replace("(", "").replace(")", "")
    alt_name = alt_name.replace("j", SH_J)  # such as 'NaN-Infi

    triple = StackableTriple(alt_name, code=code, obj=brief)

    return triple

    # such as '(-1+0j)' to -1, at:  = j j *
    # such as '-1+1.2246467991473532e-16' to -1 at:  = e i pi * pow
    # such as '2.220446049250313e-16+1j' to 1j at:  = j sqrt , *


def stackable_triple_from_float(obj):
    """Give a Basename to Float's, and snap out extreme Precision"""

    name = None

    # Give the conventional Mixed Case Basename's to the Named Float's

    for str_fuzz in ("-Inf", "NaN", "Inf"):
        if str(obj) == str_fuzz.lower():

            name = str_fuzz

    # Keep the whole Value, else snap Float to Int

    brief = obj
    if name is None:
        floor_int = int(math.floor(obj))
        if abs(obj - floor_int) < EPSILON:
            brief = floor_int

            name = str(brief)

    # Pick a Basename without much precision, if no Basename chosen already

    if name is None:
        fuzz = round(obj, FILENAME_PRECISION_3)

        name = str(fuzz)

    # Succeed

    assert name

    brief_code = stackable_dumps(brief)
    triple = StackableTriple(name, code=brief_code, obj=brief)

    return triple

    # such as '-0.0' to 0, at:  = 0 -1 /
    # such as '...' to 2.0000000000000004 at:  = 2 , sqrt , * -


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
    """Peek and remove some of the StackableTriple's most recently pushed"""

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


def stack_triples_peek_names(depth):
    """Peek at some of the Basename's most recently pushed"""

    triples = stack_triples_peek(depth)
    names = list(_[0] for _ in triples)  # as if:  (name, _, _) = triple

    return names


def stack_triples_peek_values(depth):
    """Peek at some of the Value's most recently pushed"""

    triples = stack_triples_peek(depth)
    values = list(_[-1] for _ in triples)  # as if:  (_, _, value) = triple

    return values


def stack_triples_peek(depth=1):
    """Peek at some of the StackableTriple's most recently pushed"""

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
            code = chars.rstrip()  # todo: strip only trailing "\n"?

            if False:
                if filename == "2.718_":
                    pdb.set_trace()

            # Count the File only if it holds an intelligible Value

            obj = stackable_loads_else(code, default=None)
            if obj is None:  # such as json.JSONDecodeError

                continue

            triple = StackableTriple(str(path), code=code, obj=obj)
            triples.append(triple)

    # Limit the Depth peeked, except reserve Depth 0 to mean No Limit

    if depth:
        triples = triples[-depth:]  # todo: stop evalling more Triples than needed

        assert len(triples) == depth, len(triples)

    return triples


def stack_push(obj):
    """Write the Code to clone the Obj into a Filename Basename of the Obj"""

    triple = stackable_triple(obj)

    # Mark up the Name to duck out of mutating some existing File

    path = fresh_path_from_name(triple.name)
    shpath = byo.shlex_dquote(str(path))

    # Write the Code to clone the Obj into the Marked-Up Name

    shcode = byo.shlex_dquote(triple.code)
    shcomment = "  # {!r}".format(obj) if (repr(triple.obj) != repr(obj)) else ""

    shline = "echo {} >{}{}".format(shcode, shpath, shcomment)
    byo.stderr_print("+ {}".format(shline))

    with open(shpath, "w") as writing:
        writing.write("{}\n".format(triple.code))


def fresh_path_from_name(name):
    """Find the next precise Basename in the Dir that doesn't already exist"""

    path = pathlib.Path(name)
    if path.exists():
        path = pathlib.Path("{}~".format(name))  # the 0th Alt

        index = 1
        while path.exists():
            path = pathlib.Path("{}~{}~".format(name, index))

            index += 1

    return path

    # try "name", "name~", "name~1~", "name~2~", etc


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

        except Exception as exc:
            byo.stderr_print()
            traceback.print_exc()
            byo.stderr_print("Press ⌃D TTY EOF to quit")

            try:
                sys.stdin.read()
            except KeyboardInterrupt as exc2:
                byo.stderr_print()

                byo.exit_after_print_raise(exc2)

            byo.exit_after_print_raise(exc)

        parms[::] = parms[1:]

        parms.insert(0, "buttonfile")


def try_buttonfile(parms):
    """Run the Name of a Dot-Command ButtonFile, without its Ext, as a Word"""

    assert parms

    # Take the Root of the Basename as the Word, when given a Path with an Ext,
    # but otherwise take the Word as given, such as "/" as "/", to run as "Slash"

    main_file = parms.pop(1)

    mixed_word = main_file
    if main_file.endswith(".command"):
        basename = os.path.basename(main_file)
        (root, ext) = os.path.splitext(basename)

        mixed_word = root

    # Ignore Case in the Root of the Basename of the Filename of a Button File Path

    word = mixed_word.casefold()

    # Run the Word

    word_found = try_alt_defs(word)
    if not word_found:

        if word == "clear":

            try_buttonfile_clear()  # works in place of 'entry_close_if_open()'

        elif word in (",", "comma"):

            entry = entry_close_if_open()
            if entry is None:
                do_comma()

        else:

            entry_close_if_open()
            parms_run_some(parms=[word])


def try_alt_defs(word):
    """Run some Alt Def of the ButtonFile, if found in this Corner as an Easter Egg"""

    # Try the Buttons redefined while Entry in progress
    # todo: stop making order matter, and randomise to show order unimportant

    dot_found = try_dot_button(word)
    if dot_found:

        return True

    comma_found = try_comma_button(word)
    if comma_found:

        return True

    entry_found = try_entry_button(word)
    if entry_found:

        return True

    # Try the Buttons redefined while Modular Int at Top of Stack

    bits_found = try_bits_button(word)
    if bits_found:

        return True

    # Try the Buttons defined only as Calculator Buttons in Docs, not as ordinary Words

    docs_found = try_docs_button(word)
    if docs_found:

        return True


def try_entry_button(word):
    """Return None after closing or dropping the Entry, else return the Open Entry"""

    forkable_entries = (",", ".")
    assert forkable_entries == FORKABLE_ENTRIES

    # Fetch the Entry

    entry = entry_peek_else(default=None)
    signable = entry_is_signable(entry)

    # Edit the Entry in one of many ways

    entry_found = True

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
    elif (entry in FORKABLE_ENTRIES) and (word in (",", "comma")):
        entry_write_char(",")
    else:

        entry_found = False

    # Return True, else False

    return entry_found


def entry_is_signable(entry):
    """Say when to take the + - Buttons to Choose Sign"""

    signable_entries = ("", "+", "-", ".")
    assert signable_entries == SIGNABLE_ENTRIES

    open_entries = ("", "+", "+e", "+j", ",", "-", "-e", "-j", ".", "e", "j")
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


def try_buttonfile_drop_x():
    """Pop X if X, else push 0"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 Drop
    else:
        stack_pop()


def try_buttonfile_drop_y_x():
    """Pop Y X if Y X, else push 1 if Y, else push 0 1"""

    if not stack_has_x():
        stack_push(0)  # suggest:  0 1 Drop Y X, else Y 0 Drop Y X
    if not stack_has_y():
        stack_push(0)
    else:
        stack_pop(2)


def do_comma():
    """Open Entry if no Entry open, else dupe Top of Stack"""

    if not stack_has_x():
        entry_write_char("")
    else:
        do_clone_x()  # a la Forth "DUP", a la HP "Enter"


def entry_write_char(ch):
    """Take a Char into the Entry"""

    open_entries = ("", "+", "+e", "+j", ",", "-", "-e", "-j", ".", "e", "j")
    assert open_entries == OPEN_ENTRIES

    # Peek the Entry

    entry = entry_peek_else(default=None)

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

    name = fit + "_"
    if fit in (".", ","):
        name = "_" + fit + "_"  # "_._" else "_,_"  # todo: a more distinct "-,-"

    # Replace the Entry, else start the Entry

    if entry is not None:
        stack_pop(1)

    stack_push(ButtonEntry(name))


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

    elif ch in (",", ".", "e", "j"):

        if ch in editing:
            edited = editing.partition(ch)[0]  # . => Cut back to before Ch
        elif editing in (",", "."):
            assert ch != editing
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

    finds = dict()

    finds["+"] = "Plus Sign at Dot Plus"
    finds["-"] = "Minus Sign at Dot Minus"
    finds["e"] = "Exp at Dot E"
    finds["j"] = "Imag at Dot J"
    finds[STR_PI] = "Delete at Dot Pi"

    if ch in finds.keys():
        find = finds[ch]
        byo.stderr_print("byopyvm.py: Easter Egg:  Found {}".format(find))


def entry_close_if_open():
    """Return an Unevalled Copy of the Entry, but replace it with its Eval"""

    blurry_entries = ("", "+", ",", "-", ".")
    assert blurry_entries == BLURRY_ENTRIES

    # Report either of the two kinds of Got No Entry

    if not stack_has_x():  # Empty Stack

        return None

    entry = entry_peek()  # Top of Stack is Not an Entry
    if entry is None:

        return None

    # Eval the Entry

    evalled = entry_eval(entry)

    # Celebrate finding an Egg

    finds = dict()

    finds[""] = "None at Dot Dot Op"
    finds["+"] = "None at Dot Plus Op"
    finds[","] = "None at Dot Comma Op"
    finds["-"] = "None at Dot Minus Op"
    finds["."] = "None at Dot Op"

    if entry in finds.keys():
        find = finds[entry]
        assert str(evalled).casefold() == find.split()[0].casefold(), (evalled, find)
        byo.stderr_print("byopyvm.py: Easter Egg:  Found {}".format(find))

    # Replace the Entry with its Evaluation, except discard an Empty Entry

    stack_pop(1)
    if evalled is not None:
        stack_push(evalled)

    # Return an Unevalled Copy of the Entry

    return entry


def entry_eval(entry):
    """Eval an Entry"""

    # Eval the signed or unsigned "e" and "j" OPEN_ENTRIES by Math Conventions

    by_entry = dict()

    by_entry["+e"] = math.e
    by_entry["-e"] = -math.e
    by_entry["e"] = math.e

    assert complex("+j") == 1j
    assert complex("-j") == -1j
    assert complex("j") == 1j

    # Eval the remaining OPEN_ENTRIES, all of which are or could be FORKABLE_ENTRIES

    by_entry[""] = None
    by_entry["+"] = None
    by_entry[","] = None  # often intercepted by:  def try_comma_button
    by_entry["-"] = None
    by_entry["."] = None  # often intercepted by:  def try_dot_button

    keys_of_none = tuple(_[0] for _ in by_entry.items() if _[-1] is None)
    assert keys_of_none == DROPPABLE_ENTRIES

    if entry in by_entry.keys():

        evalled = by_entry[entry]

        return evalled

    # Ask Python to eval the Entry, else append a "0" to autocomplete the Entry

    fit_before_0 = entry + "0"
    for fitted in (entry, fit_before_0):

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


def entry_peek_else(default):
    """Peek the collected Chars and return them, else return None"""

    entry = default
    if stack_has_x():
        entry = entry_peek()

    return entry


def entry_peek():
    """Peek the collected Chars and return them"""

    droppable_entries = ("", "+", ",", "-", ".")
    assert droppable_entries == DROPPABLE_ENTRIES

    # Peek from the Top of Stack

    if stack_has_x():

        triple = stack_triples_peek()[-1]
        (name, code, value) = triple

        # Peek only if the Basename ends with '_' and was code

        if name is not None:
            if name.endswith("_"):
                name = stackable_dumps(ButtonEntry(name))
                if name == code:

                    # Remove the Strong Mark of the Entry as inviting further input

                    entry = byo.str_removesuffix(value, suffix="_")
                    if value == "_._":
                        entry = "."
                    elif value == "_,_":
                        entry = ","

                    # Test that any Entry inviting further input is evallable

                    evalled = entry_eval(entry)
                    if entry in DROPPABLE_ENTRIES:
                        assert evalled is None, (entry, evalled)
                    else:
                        assert evalled is not None, (entry, evalled)

                    # Succeed

                    return entry


#
# Track dreams
#


# FIXME: add our TestDoc and our Button TestDoc here into Make SelfTest


_ = """

towards buttons of Last X, Last Y
keep up  __pycache__/x
keep up  __pycache__/y
but ouch not quite worth creating __pycache__/ it it doesn't already exist

leading data type for the result
trailing data type for the op

= -i  # for interactive CLI, till ⌃D Tty Eof
@ -i  # for interactive CLI, till ⌃D Tty Eof

conversions to Bits first dupe as floor Decimal Int, if given Complex or Float
    except it is Ceiling when negative

no hurry on the A B C D E F keys - first class, not mapped

i've long forgotten what a complex sqrt is ...

same thing in a TUI, TUI in a GShell
--tui paper tape
main.stderr

= requests.get http://...
work with Files and Dirs, not just Maths
go with 'decimal.Decimal' over 'float'
consider '^' for 'pow' for decimal Int/ Float/ Decimal

factor the common code out from:  / * - +
refresh the 'macos/.DS_Store' often enough
    even though i often feel i have to log out to flush the Finder Cache of it

add an Undo Button

"""


#
# Run from the Command Line, when not imported into some other Main module
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/byopyvm.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
