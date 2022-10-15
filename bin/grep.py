# port over auto-corrections from:  bin/git.py g, gi, gl, gli
# port over auto-corrections from:  bin/shpipes.py g, gi, gl, gli

# grep I J K -- X Y Z  # to mean:  grep -e I -e J -e K -- X Y Z

# grep -- I  # to mean grep -- -e I

_ = """

A='{if (k != $1) {print ""; print $1":"; k = $1}; gsub(/^[^:]*:/, ""); print "   ", $0}'
alias -- --a="awk -F: '$A'"
unset A

# --orientation=portrait

awk -F: '''
    if (k != $1) {
        print ""
        print $1":"
        k = $1}
    gsub(/^[^:]*:/, "")
    print "   ", $0
}
'''


# todo: could abbreviate as -hh


"""

# grep -w, vs grep '\<...\>'

# default to search the $(ls -rt |tail -1)

_ = """

% echo |g -e 3.8.2 -e 3.10.5
+ grep -e -e 3.8.2 3.10.5  # <= FIXME |g -e 3.8.2 -e 3.10.5
grep: 3.8.2: No such file or directory
grep: 3.10.5: No such file or directory
zsh: done       echo |
zsh: exit 2     g -e 3.8.2 -e 3.10.5
%
"""

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/grep.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
