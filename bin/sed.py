# sed -i~ 's,STALE,FRESH,g' *.py  # global edit find search replace

#  works well with:  head.py, tail.py, tee.py
# echo a b c d e |tr ' ' '\n' |sed -n -e '1p' -e '$p'
# echo a b c d e |tr ' ' '\n' |sed -n -e '1,2p' -e $'3i\\\n...' -e '$p'

# classic Sed rudely hangs with no prompt, when given no Parms with no Stdin

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/sed.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
