# usage: qbin/pwnme
# usage: bash/byobash-pwnme.bash

set -xeuo pipefail

cd "$(dirname $0)"/..
dirs -p |tail -1

git fetch
git rebase
git log --oneline --no-decorate -1
