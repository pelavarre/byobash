#!/usr/bin/env python3

"""
usage: bind.py ...

look at what each keystroke means, or mess with it

options:
  --help       show this help message and exit
"""

import __main__
import sys
import textwrap


if __name__ == "__main__":

    if sys.argv[1:]:
        print(__main__.__doc__.strip())

        sys.exit(0)

    SUGGESTION = textwrap.dedent(
        """

        : # Stty keys
        : # Bash keys
        : # Ssh keys
        : # macOS keys
        : # Screen keys
        : # TMux keys
        : # Emacs keys
        : # Vim keys
        : # Slack keys
        : # Chrome keys

        """
    ).strip()

    print(SUGGESTION)
