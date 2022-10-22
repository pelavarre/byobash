#!/usr/bin/env python3


import random
import re
import string
import sys


if not sys.argv[1:]:

    sys.exit()


fromfile = "p.py"
with open(fromfile) as reading:
    chars = reading.read()

lines = chars.splitlines()


def fuzz(chars):

    repl_word = ""
    for ch in chars:
        if ch == "_":
            repl_word += ch
        elif ch in "aeiouy":
            repl_word += random.choice("aeiouy")
        else:
            repl_word += random.choice(string.ascii_lowercase)

    return repl_word  # such as X for Y


linux_pinned_words = """
    bin python3 usr
""".split()

docs_python_org_words = """
    __main__ __name__
    as continue def else except exit for from if import in return sys try
    ArgumentParser False None SystemExit True
    argparse print shlex
    add_argument env main parse_args
    dest help parser
    EXIT_BAD_ARGS EXIT_SUCCESS
""".split()

my_pinned_words = """
    args choices required
""".split()

pinned_words = linux_pinned_words + docs_python_org_words + my_pinned_words

repl_by_old = dict((k, k) for k in pinned_words)
repl_by_old["python"] = "python"
repl_by_old["python2"] = "python2"


for line in lines:

    repl_line = ""
    for m in re.finditer(r"[0-9]+|[0-9A-Z_a-z]+|[^0-9A-Z_a-z]+", string=line):
        old = m.string[m.start() : m.end()]
        if not re.match(r"^[A-Z_a-z][0-9A-Z_a-z]*", string=old):
            repl_line += old
        else:
            if old not in repl_by_old.keys():
                repl_by_old[old] = fuzz(old)
            repl_line += repl_by_old[old]

    print(repl_line)
