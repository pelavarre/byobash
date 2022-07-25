#!/usr/bin/env python3

r"""
usage: byopyvm.py [--help] [WORD ...]

work quickly and concisely, over Dirs of Dirs of Files

positional arguments:
  WORD   a word of command

options:
  --help               show this help message and exit

advanced bash install:

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
  command bin/byopyvm.py --  # show the Advanced Bash Install of ByoPyVM Py and exit

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


#
# Declare some of how to divide Chars into Words of Python
#


NAME_REGEX = r"[A-Z_a-z][0-9A-Z_a-z]*"
CLOSED_NAME_REGEX = r"^" + NAME_REGEX + r"$"


DOTTED_NAME_REGEX = "({})([.]{})+".format(NAME_REGEX, NAME_REGEX)
CLOSED_DOTTED_NAME_REGEX = r"^" + DOTTED_NAME_REGEX + r"$"


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

    parms_run(parms=alt_parms)


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


def parms_run(parms):
    """Run the Parms = Read a Word, Evaluate the Word, Print the Result, Loop"""

    # Take each word, one at a time

    take_by_word = form_take_by_word()

    while parms:

        word = parms[0]
        if word not in take_by_word.keys():
            word = to_fuzzed_word(word)

        assert word in take_by_word.keys(), (word, parms)
        take = take_by_word[word]

        if not isinstance(take, collections.abc.Callable):
            value = take
            stack_push(value)
        else:
            func = take
            if take.__name__.startswith("parms_"):
                func(parms)
            else:
                func()

        parms[::] = parms[1:]


def to_fuzzed_word(word):
    """Pick out what kind of Input Word this is"""

    if re.match(CLOSED_INT_REGEX, string=word):

        return "lit_int"

    if re.match(CLOSED_FLOAT_REGEX, string=word):

        return "lit_float"

    if re.match(CLOSED_DOTTED_NAME_REGEX, string=word):

        return "dotted_name"

    if re.match(CLOSED_NAME_REGEX, string=word):

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

    d["0"] = "zero"  # Decimal Digits alone are not Python Names
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
    d["\\"] = "backslant"  # two syllables
    # d["]"]
    d["^"] = "hat"
    d["_"] = "skid"  # aka underscore

    d["`"] = "backtick"  # two syllables

    # d["{"]
    d["|"] = "bar"
    # d["}"]
    d["~"] = "tilde"  # two syllables  # aka "squiggle"

    return d

    # https://unicode.org/charts/PDF/U0000.pdf
    # http://www.catb.org/jargon/html/A/ASCII.html
    # https://www.dourish.com/goodies/jargon.html

    # http://www.forth.org/svfig/Win32Forth/DPANS94.txt
    # https://aplwiki.com/wiki/Unicode


NAME_BY_CHAR = form_name_by_char()


#
# Define Verbs
#


def form_take_by_word():
    """Declare our Built-In Verbs and Nouns"""

    # Define Sh Nouns of Forth

    take_by_sh_noun = dict(
        e=math.e,
        i=MATH_J,  # Sci Folk
        j=MATH_J,  # Eng Folk
        pi=math.pi,
    )

    take_by_sh_noun[STR_PI] = math.pi  # π

    # Define Sh Adverbs of Forth

    take_by_sh_adverb = dict(
        buttonfile=parms_buttonfile,
        dotted_name=parms_dotted_name,
        lit_float=parms_lit_float,
        lit_int=parms_lit_int,
        name=parms_name,
        hash=parms_hash,  # this 'hash' is not 'builtins.hash'
    )

    # Define SH Verbs of Forth

    take_by_sh_verb = dict(
        clear=do_clear,
        comma=do_comma,
        dash=do_dash,  # invite Monosyllabic Folk to speak of the '-' Dash
        dot=do_dot,
        equals=do_equals,
        minus=do_dash,  # invite Calculator Folk to speak of the '-' Minus
        over=do_clone_y,
        pow=do_pow,  # this 'pow' is not 'builtins.pow'
        plus=do_plus,
        slash=do_slash,
        sqrt=do_sqrt,
        star=do_star,
        swap=do_swap_y_x,
    )

    take_by_sh_verb[STR_SQRT] = do_sqrt  # √

    # Merge the Dicts of Words of Command

    d = dict()
    for kvs in (take_by_sh_adverb, take_by_sh_verb, take_by_sh_noun):
        for (k, v) in kvs.items():
            assert k not in d.keys(), k
            d[k] = v

    take_by_word = d

    # Succeed

    return take_by_word


#
# Define Sh Verbs of Forth
#


def parms_dotted_name(parms):
    """Eval a Dotted Name and push its Value"""

    py = parms[0]

    evalled = stackable_dotted_eval(py)

    pushable = evalled  # todo: factor out commonalities with 'def parms_name'
    if isinstance(evalled, collections.abc.Callable):
        pushable = evalled()  # might be:  pdb.set_trace()

    stack_push(pushable)  # you might next:  stack_peek(0)


def parms_lit_float(parms):
    """Eval the Chars of a Float Literal"""

    str_x = parms[0]
    x = float(str_x)
    stack_push(x)


def parms_lit_int(parms):
    """Eval the Chars of an Int Literal"""

    str_x = parms[0]
    x = int(str_x)
    stack_push(x)


def parms_name(parms):
    """Eval a Name and push its Value"""

    py = parms[0]

    evalled = stackable_eval(py)

    pushable = evalled  # todo: factor out commonalities with 'def parms_dotted_name'
    if isinstance(evalled, collections.abc.Callable):
        pushable = evalled()

    stack_push(pushable)


def parms_hash(parms):
    """Discard the remaining Parms as Commentary"""  # traditional in Sh at ': '

    parms[::] = list()


#
# Define Calculator Buttons
#


def do_dash():
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
        pairs = stack_pairs_peek(depth)
        for pair in pairs:
            (basename, _) = pair

            print(basename)


def do_pow():
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


def do_plus():
    """Push Y + X in place of Y X"""

    if not stack_has_x():
        stack_push(0)  # suggest 0 1 +, else 1 +
    elif not stack_has_y():
        stack_push(1)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y + x
        except Exception as exc:

            byo.exit_after_print_raise(exc)

        stack_pop(2)
        stack_push(x_)


def do_slash():
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


def do_sqrt():
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


def do_star():
    """Push Y * X in place of Y X"""

    if not stack_has_x():
        stack_push(1)  # suggest 1 2 *, else 2 *
    elif not stack_has_y():
        stack_push(2)
    else:

        (y, x) = stack_peek(2)

        try:
            x_ = y * x
        except Exception as exc:

            byo.exit_after_print_exc(exc)

        stack_pop(2)
        stack_push(x_)


#
# Define Calculator Stack Ops
#


def do_clear():  # a la GForth "clearstack"
    """Pop X till no more X"""

    stack_pairs_pop(depth=0)


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


def do_swap_y_x():
    """Drag the 2nd-to-Last Value to Top of Stack"""

    if not stack_has_x():
        stack_push(0)
    elif not stack_has_y():
        stack_push(0)
    else:

        pairs = stack_pairs_peek(2)
        pair = pairs[0]
        (basename, _) = pair

        shbasename = byo.shlex_dquote(basename)

        shline = "touch {}".format(shbasename)
        if basename.startswith("-"):
            shline = "touch -- {}".format(shbasename)

        byo.stderr_print("+ {}".format(shline))
        byo.subprocess_run_stdio(shline)


def stack_has_x():
    """Say when the Stack contains one or more Values (that is, when it is Truthy)"""

    has_x = bool(stack_depth())

    return has_x


def stack_has_y():
    """Say when the Stack contains two or more Values"""

    has_y = stack_depth() >= 2

    return has_y


def stack_depth():
    """Count the Values in the Stack"""

    pairs = stack_pairs_peek(0)  # todo: cache vs evalling for depth and again for use
    depth = len(pairs)

    return depth


#
# Adapt the Json File Format
#
#   Serialize what 'json.dumps' knows how to serialize
#   Serialize some of what Python Repr knows how to serialize too
#   Give out some of the Basenames that Python Str knows how to choose
#


def stackable_dotted_eval(py):
    """Call 'stackable_eval' but lazily import the Module it most obviously needs"""

    by_nickname = dict(D="decimal", dt="datetime", pd="pandas")
    assert by_nickname == BY_NICKNAME

    # Import the module now, if not cached earlier

    words = py.split(".")

    nickname = words[0]
    modulename = BY_NICKNAME[nickname] if (nickname in BY_NICKNAME.keys()) else nickname

    if nickname not in globals().keys():
        imported = None

        if modulename in sys.modules.keys():

            imported = sys.modules[modulename]

        else:

            try:
                imported = importlib.import_module(modulename)
            except ImportError:
                pass

        if imported:
            assert imported is sys.modules[modulename], imported
            globals()[nickname] = imported

    # Eval the Dotted Name and push its Value

    evalled = stackable_eval(py)

    return evalled


def stackable_eval(py):
    """Eval a Python expression & return its Value, else Stderr Print & Exit Nonzero"""

    try:
        evalled = eval(py)
    except Exception as exc:

        byo.exit_after_print_raise(exc)

    return evalled


def stackable_dumps(value):
    """Format an Object as Chars"""

    by_nickname = dict(D="decimal", dt="datetime", pd="pandas")
    assert by_nickname == BY_NICKNAME

    #

    try:
        poke = json.dumps(value)
    except TypeError:
        repr_value = repr(value)

        if isinstance(value, complex):
            poke = repr_value
        else:
            py = repr_value
            poke_py = repr(py)

            poke = "eval({})".format(poke_py)
            for (nickname, modulename) in BY_NICKNAME.items():
                prefix = modulename + "."
                if py.startswith(prefix):
                    alt_py = nickname + "." + py[len(prefix) :]
                    alt_poke_py = repr(alt_py)
                    poke = "eval({})".format(alt_poke_py)

                    break

            # such as eval('dt.datetime(2022, 7, 24, 16, 4, 7, 624925)')

    return poke


def stackable_loads(chars):
    """Unwrap the Object inside the Chars, else return None"""

    try:
        peek = json.loads(chars)
    except json.JSONDecodeError:

        prefix = "eval("
        suffix = ")"
        if chars.startswith(prefix) and chars.endswith(suffix):
            repr_py = chars[len(prefix) : -len(suffix)]

            py = ast.literal_eval(repr_py)

            peek = stackable_dotted_eval(py)

        else:  # todo:  much too weak reasons to conclude is Rep of Complex

            try:
                peek = complex(chars)
            except ValueError:
                peek = None  # todo: could:  raise ValueError(chars)

    return peek


def stackable_pair(value):
    """Name the Print's of an Object"""

    if isinstance(value, complex):
        assert not isinstance(value, collections.abc.Container)
        pair = stackable_pair_of_complex(value)

        return pair

    if isinstance(value, float):
        assert not isinstance(value, collections.abc.Container)
        pair = stackable_pair_of_float(value)

        return pair

    if isinstance(value, str):
        assert isinstance(value, collections.abc.Container)
        basename = value
        pair = (basename, value)

        return pair

    if isinstance(value, collections.abc.Container):
        basename = byo.dotted_typename(type(value))
        pair = (basename, value)

        return pair

    basename = str(value)
    pair = (basename, value)

    return pair


def stackable_pair_of_float(value):
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

    pair = (basename, alt_value)

    return pair

    # such as '-0.0' to 0, at:  = 0 -1 /
    # such as '...' to 2.0000000000000004 at:  = 2 , sqrt , * -


def stackable_pair_of_complex(value):
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

    pair = (basename, alt_value)

    return pair

    # such as '(-1+0j)' to -1, at:  = j j *
    # such as '-1+1.2246467991473532e-16' to -1 at:  = e i pi * pow
    # such as '2.220446049250313e-16+1j' to 1j at:  = j sqrt , *


#
# Build a Stack out of Recently Touched Files in Cwd that contain Stackable LoadS
#


def stack_pop(depth=1, asif_before_rm=""):
    """Peek and eval and remove some of the Values most recently pushed"""

    peeks = stack_peek(depth)

    _ = stack_pairs_pop(depth, asif_before_rm=asif_before_rm)

    return peeks  # will be 'one_peek' in the corner of 'depth=1'


def stack_peek(depth=1):
    """Peek and eval some of the Values most recently pushed"""

    assert depth >= 0

    alt_depth = depth if depth else stack_depth()

    pairs = stack_pairs_peek(alt_depth)  # FIXME: stack_triples_peeks to get the evalled
    values = list(_[-1] for _ in pairs)

    peeks = list()
    for value in values:
        peek = stackable_loads(chars=value)
        peeks.append(peek)

    assert len(peeks) == alt_depth, (len(peeks), alt_depth)
    if depth == 1:  # only if 'depth == 1', not also if 'alt_depth == 1'
        one_peek = peeks[-1]

        return one_peek  # is 'one_peek' in the corner of 'depth=1'

    return peeks  # is zero, two, or more Peeks, in the corners of 'depth != 1'


def stack_pairs_pop(depth, asif_before_rm=""):
    """Peek and remove some of the Basename-Chars Pairs most recently pushed"""

    assert depth >= 0

    # Collect the work to do

    pairs = stack_pairs_peek(depth)

    paths = list(_[0] for _ in pairs)
    shpaths = " ".join(byo.shlex_dquote(_) for _ in paths if _ is not None)
    if shpaths:
        if any(_.startswith("-") for _ in paths):
            shline = "rm -f -- {}".format(shpaths)
        else:
            shline = "rm -f {}".format(shpaths)

        # Trace the work, and do the work

        byo.stderr_print("+ {}{}".format(asif_before_rm.format(shpaths), shline))
        byo.subprocess_run_stdio(shline, stdout=subprocess.PIPE, check=True)

    return pairs


def stack_pairs_peek(depth=1):
    """Peek at some of the Basename-Chars Pairs most recently pushed"""

    assert depth >= 0

    # List Filenames by Modified Ascending

    shline = "ls -1art"
    run = byo.subprocess_run_stdio(shline, stdout=subprocess.PIPE, check=True)
    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    filenames = lines

    # Visit each File

    pairs = list()

    for filename in filenames:
        path = pathlib.Path(filename)

        chars = None
        if path.is_file():
            try:
                chars = path.read_text()
            except UnicodeDecodeError:
                pass

        if chars is not None:
            strip = chars.rstrip()

            # Count the File only if it holds an intelligible Value

            peek = stackable_loads(strip)
            if peek is None:  # such as json.JSONDecodeError

                continue

            pair = (str(path), strip)  # FIXME: stack_triples_peeks to get the evalled
            pairs.append(pair)  # FIXME: send the raw chars, not the strip?

    # Limit the Depth peeked, except reserve Depth 0 to mean No Limit

    if depth:
        pairs = pairs[-depth:]  # todo: stop evalling more Pairs than needed

        assert len(pairs) == depth, len(pairs)

    return pairs


def stack_push(value):
    """Push the Json Chars of a Value, into a new Autonamed File"""

    (basename, alt_value) = stackable_pair(value)

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

    alt_chars = stackable_dumps(alt_value)
    alt_shvalue = byo.shlex_dquote(alt_chars)

    alt_shcomment = "  # {!r}".format(value) if (repr(alt_value) != repr(value)) else ""

    echo_shline = "echo {} >{}{}".format(alt_shvalue, alt_shpath, alt_shcomment)
    byo.stderr_print("+ {}".format(echo_shline))

    with open(alt_path, "w") as writing:
        writing.write("{}\n".format(alt_chars))


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

    # Run the Word
    # FIXME: Clear the Stack if asked to Clear at Clear Entry

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
            parms_run(parms=[word])


def try_entry_move_by_word(word):
    """Return None after closing or dropping the Entry, else return the Open Entry"""

    # Edit the Entry in one of many ways

    entry = entry_peek_else()
    signable = entry_is_signable(entry)

    moved = True
    if (entry is not None) and (word == "clear"):
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

    pairs = stack_pairs_pop(depth=0)
    if not pairs:
        stack_push(3)
        stack_push(2)
        stack_push(1)
        stack_push(0)


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

    # Strongly mark the Entry as sincerely inviting further input

    memorable = fit + "_"
    if fit == ".":
        memorable = "_._"

    # Replace the Entry, else start the Entry

    if entry is not None:
        _ = stack_pop(1)

    stack_push(memorable)  # FIXME: serialize Entry's differently than Strings


def entry_take_char(entry, ch):
    """Edit the Entry = Take the Ch as an Editor Command for the Entry"""

    editing = "" if (entry is None) else entry

    signable_entries = ("", "+", "-", ".")
    assert signable_entries == SIGNABLE_ENTRIES

    # Work as instructed

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


def entry_close_if_open():
    """Return an Unevalled Copy of the Entry, but replace it with its Eval"""

    # Report either of the two kinds of Got No Entry

    if not stack_has_x():  # Empty Stack

        return None

    entry = entry_peek()  # Top of Stack is Not an Entry
    if entry is None:

        return None

    # Replace the Entry with its Evaluation, except discard an Empty Entry

    evalled = entry_eval(entry)

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

    if stack_has_x():

        pair = stack_pairs_peek()[-1]
        (basename, value) = pair

        if basename is not None:
            if basename.endswith("_"):
                basename_json = stackable_dumps(basename)
                if basename_json == value:

                    memorable = stackable_loads(value)
                    assert memorable is not None, repr(value)

                    entry = byo.str_removesuffix(memorable, suffix="_")
                    if memorable == "_._":
                        entry = "."

                    evalled = entry_eval(entry)
                    if entry == "":
                        assert evalled is None, (entry, evalled)
                    else:
                        assert evalled is not None, (entry, evalled)

                    return entry


#
# Track dreams
#


# FixMe: add Bits alongside Decimal Int and Decimal Float and Decimal Complex


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

got puns in / for hex, . for dec, i for oct, * for bin
but too expensive so many buttons

dot dot ... to visit each base:  to-hex, to-dec, to-oct, to-bin
except skip the to- where we already are, so first strike is always to-hex else to-dec

# dot /
# dot *
Y@ dot - , = Inf
Y@ dot - ... = negative imaginary/ float/ int
Y@ dot + , = Inf
Y@ dot + ... = positive imaginary/ float/ int

# dot dot ... to-hex, to-dec, to-oct, to-bin
Y@ dot comma = NaN

dot sqrt = Square
dot pow = Log

dot pi = tau 𝜏
# dot i
Y@ dot e , = e
Y@ dot e ... = 1e...

dot over = Swap
dot clear = Drop

no hurry on the A B C D E F keys - first class, not mapped

i've long forgotten what a complex sqrt is ...

"""


_ = """

conversions to Bits first dupe as floor Decimal Int, if given Complex or Float
    except is it Ceiling when negative?

bits / to shift right >>
bits dot / to rotate right & >> |
bits * to shift left <<
bits dot * to rotate left & << |
bits + for bits |
# bits dot +
bits - for bits ~ &
# bits dot -

bits sqrt for bits ~
bits dot sqrt for 0 bits -

bits pow for bits ^
bits dot pow for 0 bits - &

bits comma = dup  # same as dec
# bits dot comma

# bits dot pi
# bits dot i
# bits dot e
# bits dot e ...

bits dot over = Swap  # same as dec
bits dot clear = Drop  # same as dec

"""

_ = """

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
