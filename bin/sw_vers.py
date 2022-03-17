#!/usr/bin/env python3

"""
usage: sw_vers.py [-h]  ...

print macOS version

options:
  -h, --help  show this help message and exit

examples:
  sw_vers  # such as:  macOS 12.2.1 21D62
  sw_vers |grep ^ProductVersion: |cut -f2 |cut -d'.' -f-2  # such as:  12.1
  :
  : Sep/2018 Mojave macOS X 10.14  # yearly, technically minor, release date
  : Oct/2019 Catalina macOS X 10.15  # yearly, technically minor, release date
  : Nov/2020 Big Sur macOS 11  # major release date
  : Oct/2021 Monterey macOS 12  # major release date
  :
"""

# FIXME: add ArgParse


import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    SUGGESTION = textwrap.dedent(
        """
        sw_vers  # such as:  macOS 12.2.1 21D62
        sw_vers |grep ^ProductVersion: |cut -f2 |cut -d'.' -f-2  # such as:  12.1
        :
        : Sep/2018 Mojave macOS X 10.14  # yearly, technically minor, release date
        : Oct/2019 Catalina macOS X 10.15  # yearly, technically minor, release date
        : Nov/2020 Big Sur macOS 11  # major release date
        : Oct/2021 Monterey macOS 12  # major release date
        :
        """
    ).strip()

    print(SUGGESTION)


# copied from:  git clone https://github.com/pelavarre/byobash.git
