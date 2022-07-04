#!/usr/bin/env python3

"""
usage: screen.py [--h] [-ls] [-L [-Logfile LOG]] [-d] [-r [CLUE]] [-X hardcopy -h SNAP]

limit a Terminal window to a few rows and columns shared between hosts

options:
  --help  show this help message and exit
  -ls                  list the Screens you have made
  -L                   frequently flush a copy of the Screen output into './screenlog.0'
  -d                   detach the one you're in (or you can press ⌃A D)
  -r [CLUE]            re-attach a Screen found by name (default: list all Screens)
  -X hardcopy -h SNAP  export a LogFile of what Less Mode can see

quirks:

  works well with:  script.py
  classic Screen rudely opens a new anonymous Session, when given no Parms

  '-r' fails when you give no CLUE, if there is more than one Screen
  says 'Copy mode' to mean it's working in the Less Mode
  says 'Copy mode aborted' to mean it's back to working in the default Mode
  takes a '-Logfile LOGFILE' option at Linux to separate LogFiles from a shared Dir

examples:

  screen.py  &&: show these examples and exit
  screen.py --h  &&: show this help message and exit
  screen.py --  &&: todo: run as you like it

  screen ls  &&: say '[screen is terminating]'
  screen -ls  &&: list the Screens you have made
  screen  &&: make another Screen
  echo $STY  &&: show the one you're inside, or show nothing when you're outside
  screen -d  &&: detach the one you're in (or you can press ⌃A D)
  exit &&: delete this Screen that you've made (or you can press ⌃D)

  screen -S Screen1 -L  &&: name the Screen, often flush its Output to './screenlog.0'
  screen -r Screen1  &&: find a Screen by name, and re-attach that Screen
  # ⌃A ?  &&: show Keyboard Shortcuts
  # ⌃A A  &&: send an ordinary Control+A keystroke
  # ⌃A Esc  &&: enter the Less Mode, so ⌃B means page back, ⌃F means page ahead
  # Esc  &&: exit the Less Mode

  screen python  &&: show why 'screen ls' feels pointless
  screen -X hardcopy -h s.screenlog  &&: export a LogFile of what Less Mode can see

  cat screenlog.0  &&: trust and run the Esc sequences
  less -FIRX screenlog.0  &&: trust and run the Esc sequences
  less screenlog.0  &&: show the Esc sequences without running them
"""
# talk out how best to clear Bash History for a Bash Screen
# Linux only -Logfile LOG         choose a name for the LogFile (default: 'screenlog.0')
# screen.py -r  # pick the latest, and autonumber them a b c ..., don't demand just one
# screen.pr --rt  # sort by latest last
# -t      forward control of the local terminal (-tt for more force)


import byotools as byo


byo.exit(__name__)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/screen.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
