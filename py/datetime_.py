#!/usr/bin/env python3


_ = """


# give the " " of RFC 3339, as less loud than ISO 8601 "T"

import datetime as dt

now = dt.datetime.now()
FORMAT_YMD_HM = "%Y-%m-%d %H:%M"
ymd_hm = now.strftime(FORMAT_YMD_HM)  # such as '2022-07-25 08:24'
print(ymd_hm)


# take the r"[ Tt]" from RFC 3339, to allow " " less loud than ISO 8601 "T"

import datetime as dt

ymd_hm = "2022-07-25 08:24"
ymd_t_hm = ymd_hm.replace(" ", "T")
FORMAT_YMD_T_HM = "%Y-%m-%dT%H:%M"
then = dt.datetime.strptime(ymd_t_hm, FORMAT_YMD_T_HM)
print(then)  # such as '2022-07-25 08:24:00' from:  dt.datetime(2022, 7, 25, 8, 24)

"""


# todo:
#
#   def dt_timedelta():
#       """Get the Time Delta since the local 1970-01-01T00:00:00 dawn of Unix Time"""
#
#   def dt_timedelta_strftime(td, format):
#       """Fill out %y %m %w %d %H %M %S %f"""
#

_ = """

import datetime as dt
td = dt.datetime.now() - dt.datetime(1970, 1, 1)

t = td.total_seconds()

u = 365.25 * 24 * 3600
y = int(t / u)
t = t - (y * u)

u /= 12
m = int(t / u)
t = t - (m * u)

u = 7 * 24 * 3600
w = int(t / u)
t = t - (w * u)

u = 24 * 3600
d = int(t / u)
t = t - (d * u)

u = 3600
H = int(t / u)
t = t - (H * u)

u = 60
M = int(t / u)
t = t - (M * u)

S = int(t)

print(f"{y}Y {m}M {w}W {d}D {H}h {M}m {S}s")

"""


# posted into:  https://github.com/pelavarre/byobash/blob/main/py/datetime_.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
