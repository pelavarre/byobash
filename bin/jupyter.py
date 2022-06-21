#!/usr/bin/env python3

"""
usage: jupyter.py [--h] ...

serve web pages that interpret Python language

options:
  --help       show this help message and exit

examples:
  pip freeze | wc -l  # lots, or a few

  mkdir -p ~/.venvs/
  cd ~/.venvs/
  rm -fr jplab/
  python3 -m venv --prompt JPLAB jplab/

  cd -
  source ~/.venvs/jplab/bin/activate
  which pip
  pip freeze | wc -l  # 1

  pip install --upgrade pip
  pip install --upgrade wheel

  pip install --upgrade pandas
  pip install --upgrade jupyterlab

  pip freeze | wc -l  # 71

  jupyter notebook --ip=0.0.0.0
"""


import byotools as byo


if __name__ == "__main__":

    byo.exit()


# copied from:  git clone https://github.com/pelavarre/byobash.git
