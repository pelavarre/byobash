_ = """

date -u -r86400
date -r86400
date
uname

% date -u -r86400
Fri Jan  2 00:00:00 UTC 1970
% date -r86400
Thu Jan  1 16:00:00 PST 1970
% date
Mon Jul 18 14:12:11 PDT 2022
% uname
Darwin
%

"""


_ = """

date -u --date @86400
date --date @86400
date
uname

$ date -u --date @86400
Fri Jan  2 00:00:00 UTC 1970
$ date --date @86400
Thu Jan  1 16:00:00 PST 1970
$ date
Mon Jul 18 14:13:23 PDT 2022
$ uname
Linux
$

"""

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/date.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
