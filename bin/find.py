# find .  -name '*.py'  -not -type d  -not -path './.git/*'

# works well with:  cat.py

#   Find Py chooses the empty TOP '', not the explicit './' TOP, when given no Parms
#   classic Find rudely declines to choose the TOP itself, but Linux Find chooses '.'


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/find.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
