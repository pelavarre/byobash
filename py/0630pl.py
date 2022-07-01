import glob
import os
import pathlib
import pdb

_ = pdb


POSTED = "# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/"
COPIED = "# copied from:  git clone https://github.com/pelavarre/byobash.git"

bin_hits = list(glob.glob("bin/*.py"))
py_hits = list(glob.glob("py/*.py"))
hits = bin_hits + py_hits

for hit in hits:
    filename = os.path.basename(hit)

    path = pathlib.Path(hit)
    if not path.is_dir():

        ichars = path.read_text()
        if ichars:
            ilines = ichars.splitlines()

            #

            olines = list(ilines)

            if not olines[-1]:
                olines = olines[:-1]
            if olines[-1].split()[:2] == "# copied".split():
                olines = olines[:-1]
            if olines[-1].split()[:2] == "# posted".split():
                olines = olines[:-1]
            if not olines[-1]:
                olines = olines[:-1]  # once
            if not olines[-1]:
                olines = olines[:-1]  # twice

            #

            olines.append("")
            olines.append("")
            olines.append(POSTED + filename)
            olines.append(COPIED)
            olines.append("")

            #

            ochars = "\n".join(olines)

            if ochars != ichars:
                print(hit)

                path.write_text(ochars)


# posted into:  https://github.com/pelavarre/byobash/blob/main/bin/0630pl.py
# copied from:  git clone https://github.com/pelavarre/byobash.git
