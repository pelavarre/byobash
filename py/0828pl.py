#!/usr/bin/env python3

"""
usage: python3 py/0828pl.py [--h] [--]

show two days behind and five days ahead of hourly time across some timezones

examples:
    python3.py py/0828pl.py  # show these examples
    python3.py py/0828pl.py --  # -7 +2 +5.5
"""


import datetime as dt
import os
import pdb
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

_ = byo


def main():
    """Run from the Sh Command Line"""

    byo.exit(shparms="--")  # do nothing without Parms

    zones = (-7, +2, +5.5)
    str_zones = "-07:00 +02:00 +05:30".split()

    today = dt.datetime.now()
    today = dt.datetime(today.year, today.month, today.day)

    for days in range(-2, +5):
        for hours in range(7, 22):
            here = today + dt.timedelta(days=days, hours=hours)

            print()
            for (zone, str_zone) in zip(zones, str_zones):
                there = here + dt.timedelta(hours=(zone - zones[0]))
                print("{} {}".format(there.strftime("%a %b %Y-%m-%d %H:%M"), str_zone))


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/0828pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
