#!/usr/bin/env python3

"""
usage: cal.py [--help] [-h] [-H YMD] [-M | -S] [Y]

show what weekday it is or was or will be, of which year and month

positional arguments:
  Y       show a chosen year (or YMD or MD or D), in place of today, a la:  cal Y

options:
  --help  show this help message and exit
  -h      don't color the chosen day (default: do color at stdout isatty)
  -H YMD  show a chosen day, in place of today
  -m M    show a chosen month, in place of today
  -M      start the weeks on UK Monday's, not US Sunday's (default: true)
  -S      start the weeks on US Sunday's, not UK Monday's (default: false)

notes:
  type 'ncal -M -b' to get flat weeks started on UK Monday's, from more Cal's
  type '-m' before M, and M in place of MD or D, from more Cal's
  call Cal twice to get the month of weeks around today, from more Cal's

examples:
  cal.py  &&: a month of the five weeks around today
  MM=$(date +%m) && cal -m $((MM - 1)) && cal -m $MM && cal -m $((MM + 1))  &&: ditto
  cal.py 314  &&: show the Pi day of this year, a la:  cal -m 3
  cal.py 1999  &&: show the last year of last century
  cal.py -b  &&: flat weeks, started on UK Monday's, a la:  Linux ncal -M -b
  cal.py -S -b  &&: flat weeks, started on US Sunday's, a la:  Linux ncal -b
"""
# todo: test cal.py, fix cal.py -m 3, etc

import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    doc = __main__.__doc__
    epilog = doc[doc.index("examples:") :]
    tests = "\n".join(epilog.splitlines()[1:])
    print(textwrap.dedent(tests))
