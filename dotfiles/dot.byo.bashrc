# dotfiles/dot.byo.bashrc


function cd.py () {
    'cd' "$(~/Public/byobash/bin/cd.py $@)"
    dirs -p |head -1  # same as Bash:  dirs +0
}


function echo.py {
  local xc=$?
  if [ "$#" = 1 ] && [ "$1" = "--" ]; then
    'echo' "+ exit $xc"
  else
    command echo.py "$@"
  fi
}


# posted into:  https://github.com/pelavarre/byobash/blob/main/dotfiles/dot.byo.bashrc
# copied from:  git clone https://github.com/pelavarre/byobash.git
