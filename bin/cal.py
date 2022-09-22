#!/usr/bin/env python3

"""
usage: cal.py [--h] [-h] [-H YMD] [-M | -S] [Y]

show what weekday it is or was or will be, of which year and month

positional arguments:
  Y       show a chosen year (or YMD or MD or D), in place of today, a la:  cal Y

options:
  --help  show this help message and exit
  -h      don't color the chosen day (default: do color at stdout isatty)
  -H YMD  show a chosen day, in place of today
  -m M    show a chosen month, in place of today
  -M      start the weeks on UK Monday's, not US Sunday's (default True)
  -S      start the weeks on US Sunday's, not UK Monday's (default False)

quirks:
  the DD|MMDD|YYMMDD|YYYYMMDD syntaxes sometimes worked as Parms, such as:  cal.py 314
  type 'ncal -M -b' to get flat weeks started on UK Monday's, from more Cal's
  type '-m' before M, and M in place of MD or D, from more Cal's
  call Cal twice to get the month of weeks around today, from more Cal's

examples:

  cal.py  # show these examples and exit
  cal.py --h  # show this help message and exit
  cal.py --  # todo: run as you like it

  cal.py  # a month of the five weeks around today
  MM=$(date +%m) && cal -m $((MM - 1)) && cal -m $MM && cal -m $((MM + 1))  # ditto
  cal.py 314  # show the Pi day of this year, a la:  cal -m 3
  cal.py 20210314  # show the Pi day of a chosen year
  cal.py 1999  # show the last year of last century
  cal.py -b  # flat weeks, started on UK Monday's, a la:  Linux ncal -M -b
  cal.py -S -b  # flat weeks, started on US Sunday's, a la:  Linux ncal -b
"""
# todo: test cal.py, fix cal.py -m 3, etc


import os
import subprocess
import sys

import byotools as byo


if __name__ == "__main__":

    path = os.path.expanduser("~/Public/pybashish/bin/cal.py")
    if not os.path.exists(path):

        byo.exit()

    else:

        # Take 'cal.py', 'cal.py --h', 'cal.py --he', ... 'cal.py --help'

        byo.exit_if_testdoc()  # cal.py
        byo.exit_if_argdoc()  # cal.py --help

        argv = list(sys.argv)
        argv[0] = path

        run = subprocess.run(argv)
        if run.returncode:
            sys.exit(run.returncode)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/cal.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
