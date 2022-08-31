#!/usr/bin/env python3

"""
usage: dataclass_hello.py

introduce the slowly evolving Data Class idea of Python

motivation:

  sometimes it helps to have
  a data type similar to the Pascal “record” or C “struct”,
  bundling together a few named data items

  -- Docs-Python-Org > Python Tutorial > 9.7 Odds and Ends
  -- https://docs.python.org/3/tutorial/classes.html#odds-and-ends

tech:

  an im/mutable Data Dict Class can declare

  1 Keys
  2 Types of Values
  3 how to print Keys and Values of Instances

  class Class2
  class Class26(collections.namedtuple("Class26", ...  # immutable
  class Class27(argparse.Namespace)
  class Class33(types.SimpleNamespace)
  @dataclasses.dataclass class Class37

  the Funcs and Modules of Python's work like Instances of Data Classes

examples:

  hellos/dataclass_hello.py  # print these examples
  python3 -i hellos/dataclass_hello.py --  # run 'def main'
  python3 -i -c 'from hellos.dataclass_hello import *'  # don't run 'def main'
"""

# code reviewed by people, and by Black and Flake8


#
# Pull in what's available
#


import __main__
import argparse
import collections
import datetime as dt
import sys
import textwrap
import time
import types


try:
    _ = types.SimpleNamespace
except AttributeError:
    print("Upgrade to >= Sep/2012 Python 3.3 to Import SimpleNameSpace")
    types.SimpleNamespace = None


try:
    import dataclasses
except ImportError:
    print("Upgrade to >= Jun/2018 Python 3.7 to Import DataClass Decorators")
    dataclasses = None


#
# Run from the Sh Command Line
#


def main():
    """Run from the Sh Command Line"""

    # Default to print help and quit

    if not sys.argv[1:]:
        doc = __main__.__doc__.strip()

        test_doc = doc[doc.index("examples:") :]
        test_doc = "\n".join(test_doc.splitlines()[1:])
        test_doc = textwrap.dedent(test_doc).strip()

        print()
        print(test_doc)
        print()

        sys.exit(0)

    # Form one Instance of each Class, & copy-edit that Instance to form a 2nd Instance

    o2a = Class2()
    o2a.measure = 200
    o2a.modified = later()
    o2b = Class2()
    o2b.measure = o2a.measure
    o2b.modified = later()

    o26a = Class26(260, modified=later())
    o26b = o26a._replace(modified=later())
    # o26b.modified = later()  # nope, raises:  AttributeError: can't set attribute

    o27a = Class27(measure=270, modified=later())
    o27b = Class27(**vars(o27a))
    o27b.modified = later()

    if types.SimpleNamespace:

        o33a = Class33(measure=330, modified=later())
        o33b = Class33(**vars(o33a))
        o33b.modified = later()

    if dataclasses:

        o37a = Class37(measure=330, modified=later())
        o37b = Class37(**vars(o37a))
        o37b.modified = later()
        o37c = Class37()
        o37c.measure = o37a.measure

    # Print each pair of Instances

    now = later()

    print()
    print(str(now))  # 2022-08-31 11:41:53.527224
    print(repr(now))  # datetime.datetime(2022, 8, 31, 11, 41, 53, 527224)

    print()
    print(o2a)  # <__main__.Class2 object at 0x...>
    print(o2b)  # <__main__.Class2 object at 0x...>

    print()
    print(o26a)  # Class26(measure=260, modified=...datetime(2022, 8, 31, ... 516542))
    print(o26b)  # Class26(measure=260, modified=...datetime(2022, 8, 31, ... 517871))

    print()
    print(o27a)  # Class27(measure=270, modified=...datetime(2022, 8, 31, ... 518949))
    print(o27b)  # Class27(measure=270, modified=...datetime(2022, 8, 31, ... 520111))

    print()
    print(o33a)  # Class33(measure=330, modified=...datetime(2022, 8, 31, ... 521514))
    print(o33b)  # Class33(measure=330, modified=...datetime(2022, 8, 31, ... 522941))

    print()
    print(o37a)  # Class37(measure=330, modified=...datetime(2022, 8, 31, ... 524385))
    print(o37b)  # Class37(measure=330, modified=...datetime(2022, 8, 31, ... 525830))
    print(o37c)  # Class37(measure=330, modified=...datetime(2022, 8, 31, ... 512178))

    # Pin this work in memory for a later debugger to inspect it,
    # making the Func "main" and the Module "__main__" into a kind of DataClass Instance

    main.o2a = o2a
    main.o26a = o26a
    main.o27a = o27a
    main.o33a = o33a
    main.o37a = o37a

    __main__.o2b = o2b
    __main__.o26b = o26b
    __main__.o27b = o27b
    __main__.o33b = o33b
    __main__.o37b = o37b
    __main__.o37c = o37b

    # a debugger can reach into __builtins__ to try:  print(vars(main).keys())
    # a debugger can reach into __builtins__ to try:  print(vars(__main__).keys())


#
# Declare five kinds of Data Classes
#


class Class2:
    """Odds & Ends, since practically forever"""


class Class26(collections.namedtuple("Class26", "measure modified".split())):
    """Named Tuple Classes, since Oct/2008 Python 2.6"""


class Class27(argparse.Namespace):
    """Basic Namespace of Import ArgParse, since Jul/2010 Python 2.7"""

    # a Python 3 that defaults to sort Namespace keys is May/2021 Python 3.8.10
    # a Python 3 that leaves Namespace keys in insertion order is Python Jun/2022 3.10.5


if types.SimpleNamespace:

    class Class33(types.SimpleNamespace):
        """Simple Namespace of Import Types, since Sep/2012 Python 3.3"""


if dataclasses:

    @dataclasses.dataclass
    class Class37:
        """DataClass Decorators, since Jun/2018 Python 3.7"""

        measure: int = -1  # old Python's - 3.4, 2.7.18, etc - fail here w SyntaxError
        modified: dt.datetime = dt.datetime.now()


#
# Mark one time apart from the next
#


def later():
    """Return later and later Timestamp's, when called again and again"""

    time.sleep(0.001)

    t0 = dt.datetime.now()

    return t0

    # repr(t0) such as datetime.datetime(2022, 7, 5, 15, 22, 37, 15037)
    # str(t0) such as '2022-07-05 15:22:37.015037'


#
# Run from the Sh command line, when not imported
#


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/hellos/dataclass_hello.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
