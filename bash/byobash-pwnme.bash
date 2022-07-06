set -xeuo pipefail
cd ~/Public/byobash
git fetch
git rebase
git log --oneline --no-decorate -1
