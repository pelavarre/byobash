
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


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/datetime.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
