#!/usr/bin/env python3

"""
usage: python3 py/0827pl.py [--h] [--]

print Starplots of Git Commits pushed by Authors across Days

examples:
    python3.py py/0827pl.py $PWD
"""


import collections
import datetime as dt
import os
import pdb
import shlex
import subprocess
import sys

_ = pdb


DIR = os.path.dirname(__file__)
TOP_DIR = os.path.join(DIR, os.pardir)  # one up from "py/"
BIN_DIR = os.path.join(TOP_DIR, "bin")

try:
    import byotools as byo
except ImportError:
    sys.path.insert(0, BIN_DIR)
    import byotools as byo


def main():
    """Run from the Sh Command Line"""

    print(dt.datetime.now())

    # ChDir as told

    parms = sys.argv[1:]
    assert len(parms) <= 1, parms

    if not parms:
        byo.exit()

    chdir = parms[0]
    if chdir != "--":
        print("+ chdir", chdir)
        os.chdir(chdir)

    # Blame one engineer first of all

    gcue_shline = "git config user.email"
    print("+", gcue_shline)
    gcue_argv = shlex.split(gcue_shline)

    gcue_run = subprocess.run(gcue_argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert not gcue_run.returncode, gcue_run.returncode
    assert not gcue_run.stderr, gcue_run.stderr

    gcue_stdout = gcue_run.stdout.decode()
    gcue_lines = gcue_stdout.splitlines()

    assert len(gcue_lines) == 1
    gcue_line = gcue_lines[-1]

    gcue = gcue_line.splitlines()[0]

    assert gcue == gcue.strip(), repr(gcue)

    # Sample Git Log once, across some Special Days

    shline = "git log --pretty='%ae\t%cd' --after=2022-04-16"
    argv = shlex.split(shline)

    print("+", shline)
    run = subprocess.run(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert not run.returncode, run.returncode
    assert not run.stderr, run.stderr

    stdout = run.stdout.decode()
    lines = stdout.splitlines()

    # Scrape this Git Log Stdout

    FORMAT_a_b_d_HMS_Y = "%a %b %d %H:%M:%S %Y"  # such as'Fri Dec 31 12:59:59 1999'

    commits_by_ae = collections.defaultdict(list)
    for line in lines:
        cells = line.split("\t")
        assert len(cells) == 2, cells

        ae = cells[0]
        str_cd = cells[-1]

        cd_words = str_cd.split()
        want_words = FORMAT_a_b_d_HMS_Y.split()
        assert len(cd_words) - len(want_words) in (0, 1), (len(cd_words), str_cd)

        parseable = " ".join(cd_words[: len(want_words)])
        cd = dt.datetime.strptime(parseable, FORMAT_a_b_d_HMS_Y)  # todo: timezones

        commits_by_ae[ae].append(cd)

    # Sort Authors by Count of Commits

    pairs = list(commits_by_ae.items())

    sorted_pairs = list(pairs)
    sorted_pairs.sort(key=lambda kv: (len(kv[-1]), kv))

    for visual in (1, 2):
        print()

        gcue_index = -1
        for (index, (ae, cds)) in enumerate(sorted_pairs):

            # Lift up our blamed Git Config User Email engineer

            if ae == gcue:
                assert gcue_index == -1, gcue_index
                gcue_index = index

            # Visualize the Commit Traffic pushed per Calendar Day by each Author

            cd_by_ymd = collections.defaultdict(list)
            for cd in reversed(cds):
                ymd = (cd.year, cd.month, cd.day)
                cd_by_ymd[ymd].append(cd)

            # Print by Author Index, sorted from least to most frequent

            counts = list(len(_) for _ in cd_by_ymd.values())
            sum_counts = sum(counts)
            str_counts = " ".join(str(_) for _ in counts)

            starbursts = list(_ * "*" for _ in counts)
            str_starbursts = " ".join(starbursts)

            blame = "by Author {}".format(index)
            if ae == gcue:
                blame = "by Author {} = {!r}".format(index, ae.split("@")[0])

            # Print as more or less visual

            if visual < 2:
                print(sum_counts, "as", str_counts, blame)
            else:
                print(str_starbursts, blame)

    _ = gcue_index


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0827pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
