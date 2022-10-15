# find . -not -type d -not -path './.git/*'
# find . -not -type d -not -path './.git/*' |grep -v '/[.]'

# find __pycache__/ -mtime -1 -ls |wc -l
# du -sh $PWD/*
# df |grep /$

# goes well with:  cat.py

#   Find Py chooses the empty TOP '', not the explicit './' TOP, when given no Parms
#   classic Find rudely declines to choose TOP itself, Linux Find chooses './' not ''

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/find.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
