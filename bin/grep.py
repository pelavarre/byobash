# grep -w, vs grep '\<...\>'

_ = """

% echo |g -e 3.8.2 -e 3.10.5
+ grep -e -e 3.8.2 3.10.5  # <= FIXME |g -e 3.8.2 -e 3.10.5
grep: 3.8.2: No such file or directory
grep: 3.10.5: No such file or directory
zsh: done       echo |
zsh: exit 2     g -e 3.8.2 -e 3.10.5
%
"""
