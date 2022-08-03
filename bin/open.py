#!/usr/bin/env python3

"""
usage: open.py [-h] ADDRESS

tell the browser to visit an address

positional arguments:
  ADDRESS     some web address, maybe ending in '/' plus '?' '&' '=' pairs

options:
  -h, --help  show this help message and exit

quirks:

  goes well with:  curl.py
  requires quoting of '&' when run inside any ordinary Sh
  requires quoting of '*' or '?' in Address'es, when haunted by 'zsh: no matches found'
  doesn't visit Address when run as 'open.py --', instead
    prints many forms of address to choose from, spun out from one address

examples:

  open.py  # show these examples and exit
  open.py --h  # show this help message and exit

  open.py -- 'http://google.com/search?tbm=isch&q=Carelman+Everyday'
  open.py -- http://jira/issues/?jql=text%20~%20%27Hobbit%27
  open.py -- http://wiki
  open.py -- https://twitter.com/pelavarre/status/1543460479720337409?s=20
  open.py -- 'https://www.google.com/search?tbm=isch&q=Carelman+Everyday'
"""


import sys
import urllib.parse


import byotools as byo


def main():

    if "--" not in sys.argv[1:]:
        byo.exit()

    args = byo.parse_epi_args(epi="quirks")
    address = args.address

    # Open with a mention of the Original

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
    if alt_splits != splits:

        print()
        print(urllib.parse.urlunsplit(alt_splits))

    # Add Line-Break's to the Query

    if splits.query:
        root = byo.str_removesuffix(address, suffix=splits.query)

        print()
        print(root.rstrip("?"))

        print()
        print(root)
        pairs = urllib.parse.parse_qsl(splits.query)
        for (index, pair) in enumerate(pairs):
            (name, value) = pair
            qvalue = urllib.parse.quote(value)
            if not index:
                print("    {}={}".format(name, qvalue))
            else:
                print("    &{}={}".format(name, qvalue))

    # Close with a mention of the Original

    print()
    print(address)

    print()


if __name__ == "__main__":
    main()


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/open.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
