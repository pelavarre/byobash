# dotfiles/dot.byo.bashrc

function cd.py () {
  if [ "$#" = 1 ] && [ "$1" = "--" ]; then
    'cd' ~/Desktop && (dirs -p |head -1)
  else
    'cd' "$(~/Public/byobash/bin/cd.py $@)" && (dirs -p |head -1)
  fi
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
