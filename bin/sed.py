# sed -i~ 's,STALE,FRESH,g' *.py  # global edit find search replace


# echo a b c d e |tr ' ' '\n' |sed -n -e '1p' -e '$p'
# echo a b c d e |tr ' ' '\n' |sed -n -e '1,2p' -e $'3i\\\n...' -e '$p'


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sed.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
