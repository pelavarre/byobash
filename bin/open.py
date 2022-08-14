#!/usr/bin/env python3

"""
usage: open.py [-h] [ADDRESS]

tell the browser to visit an address, or just split it into parts

positional arguments:
  ADDRESS     some web address, maybe ending in '/' plus '?' '&' '=' pairs

options:
  -h, --help  show this help message and exit

quirks:
  goes well with:  curl.py
  requires quoting of '&' when run inside any ordinary Sh
  requires quoting of '*' or '?' in Address'es, when haunted by 'zsh: no matches found'
  accepts quoted '#' in place of '?' to introduce '&' '=' key-value pairs
  takes '--' to mean print many forms of the Address, don't visit it

examples:

  open.py  # show these examples and exit
  open.py --h  # show this help message and exit

  open.py --  # take an Address to split from Stdin

  open.py -- 'https://www.google.com/search?tbm=isch&q=Carelman+Everyday'
  open.py -- http://jira/issues/?jql=text%20~%20%27Hobbit%27
  open.py -- http://wiki.example.com/display/main/Welcome
  open.py -- https://twitter.com/pelavarre/status/1543460479720337409?s=20
"""
# todo: look for '#' over '?' examples of key-value pairs, but found outside the Vpn's


import os
import re
import sys
import urllib.parse


import byotools as byo


def main():
    """Run from the Sh Command Line"""

    if "--" not in sys.argv[1:]:
        byo.exit()

    args = byo.parse_epi_args(epi="quirks")

    if args.address is not None:
        print_forms_of_address(address=args.address)
    else:
        byo.stderr_print("open.py: Type a Web Address and press Return")
        byo.stderr_print()

        address = byo.stdin_readline_else()
        print_forms_of_address(address)
        while byo.select_select(sys.stdin):
            address = byo.stdin_readline_else()
            print_forms_of_address(address)


def print_forms_of_address(address):  # noqa C901 too complex (11)
    """Print many forms of the Address, don't visit it"""

    # Open with a mention of the Original

    print()
    print("-- original, as header --")
    print()
    print(address)

    # Break the Address into Parts

    splits = urllib.parse.urlsplit(address)  # scheme://netloc/path?query...
    scheme = splits.scheme
    netloc = splits.netloc

    # Look to give up some Precision or Privacy

    alt_splits = urllib.parse.urlsplit(address)
    if scheme == "https":
        alt_splits = alt_splits._replace(scheme="http")
    if netloc.startswith("www."):
        alt_splits = alt_splits._replace(netloc=byo.str_removeprefix(netloc, "www."))

    alt_unsplit = urllib.parse.urlunsplit(alt_splits)

    if alt_unsplit != address:

        print()
        print("-- shrug off Http S, WWW Dot --")
        print()
        print(urllib.parse.urlunsplit(alt_splits))

        # Try to give up some more Precision

        vpn_splits = urllib.parse.urlsplit(alt_unsplit)
        if "." in netloc:
            vpn_netloc = vpn_splits.netloc.split(".")[0]
            vpn_splits = vpn_splits._replace(netloc=vpn_netloc)

            vpn_unsplit = urllib.parse.urlunsplit(vpn_splits)

            print()
            print("-- local network without much domain --")
            print()
            print(vpn_unsplit)

    # Try to give up some Escapes

    basename = os.path.basename(splits.path)
    unquoted_basename = urllib.parse.unquote(basename)
    if unquoted_basename != basename:

        print()
        print("-- unquoted basename --")
        print()
        print(unquoted_basename)

        titled_basename = unquoted_basename
        titled_basename = titled_basename.replace("+", " ")
        titled_basename = titled_basename.replace(":", " - ")
        titled_basename = re.sub(r" +", repl=" ", string=titled_basename)
        titled_basename = titled_basename.title()

        print()
        print("-- titled unquoted basename --")
        print()
        print(titled_basename)

    # Add Line-Break's to the Query

    COUNT_1 = 1

    kv_ch = "?"
    kv_address = address
    kv_splits_query = splits.query
    if not splits.query:

        kv_ch = "#"
        kv_address = address.replace("#", "?", COUNT_1)
        kv_splits = urllib.parse.urlsplit(kv_address)
        kv_splits_query = kv_splits.query

    if kv_splits_query:
        root = byo.str_removesuffix(kv_address, suffix=kv_splits_query)

        rstrip = root.rstrip("?")

        print()
        print("-- without query --")
        print()
        print(rstrip)

        if rstrip.endswith("/edit"):

            print()
            print("-- without query, without basename --")
            print()
            print(byo.str_removesuffix(rstrip, suffix="/edit"))

        print()
        print("-- with line-broken query --")
        print()
        print(rstrip + kv_ch)
        pairs = urllib.parse.parse_qsl(kv_splits_query)
        for (index, pair) in enumerate(pairs):
            (name, value) = pair
            qvalue = urllib.parse.quote(value)
            if not index:
                print("    {}={}".format(name, qvalue))
            else:
                print("    &{}={}".format(name, qvalue))

        joinable_query = urllib.parse.urlencode(pairs)
        joinable_splits = urllib.parse.urlsplit(kv_address)
        joinable_splits = joinable_splits._replace(query=joinable_query)
        joinable_unsplit = urllib.parse.urlunsplit(joinable_splits)
        joinable_unsplit = joinable_unsplit.replace("?", kv_ch, COUNT_1)

        print()
        print("-- unsplit query --")
        print()
        print(joinable_unsplit)

    # Close with a mention of the Original

    print()
    print("-- original, as trailer --")
    print()
    print(address)

    # Print one last Empty Line to separate this Sh Verb Output from the Sh Prompt

    print()


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/open.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
