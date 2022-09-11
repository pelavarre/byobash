#!/usr/bin/env awk

# usage: ... |headgrafs.awk
#
# indent each hit beneath an empty line and a print of its pathname
#
# examples:
#  grep -Hi Awk bin/*.py |awk -F: -f awk/headgrafs.awk
#

{
    if (k != $1) {
        print ""
        print $1":"
        k = $1
    }
    gsub(/^[^:]*:/, "")
    print "   ", $0
}

# A='{if (k != $1) {print ""; print $1":"; k = $1}; gsub(/^[^:]*:/, ""); print "   ", $0}'
# alias -- --a="awk -F: '$A'"
# unset A
