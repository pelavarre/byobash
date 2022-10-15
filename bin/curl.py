# curl -i -sS -O
#   goes well with:  open.py

_ = r"""

curl ifconfig.me && echo
curl ipinfo.io/ip && echo
curl ipecho.net/plain && echo

curl api.ipify.org && echo

curl -Ss wtfismyip.com/json |sed 's,Your.\{7\},Your,'

"""

# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/curl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
