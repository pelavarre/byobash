#!/usr/bin/env python3

"""
usage:  import buttonfile as bf
"""

import os
import pdb
import sys

_ = pdb


def at_import():
    """Substitute the Buttonfile Py from the Dir Above for this Buttonfile Py"""

    globals_ = globals()

    module = sys.modules[__name__]
    module_file = os.path.realpath(module.__file__)
    module_dirname = os.path.dirname(module_file)
    module_pardir = os.path.join(module_dirname, os.pardir)

    # Import that Buttonfile Py in place of this Buttonfile Py

    del sys.modules[__name__]

    sys.path.insert(0, module_pardir)
    try:

        import buttonfile as bf

    finally:
        sys.path.pop(0)

    # Import that Buttonfile Py in place of an imported Bf too

    assert bf is not module

    if globals_.get("bf") is module:
        globals_["bf"] = bf

    if globals_.get("buttonfile") is module:  # todo:  test this too
        globals_["buttonfile"] = bf


if __name__ != "__main__":
    at_import()


# posted into:  https://github.com/pelavarre/byobash/blob/main/macos/more/buttonfile.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
