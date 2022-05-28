# pip freeze | wc -l  # lots, or a few
#
# mkdir -p ~/.venvs/
# cd ~/.venvs/
# rm -fr jupyterlab/
# python3 -m venv --prompt JPLAB jupyterlab/
#
# cd -
# source ~/.venvs/jupyterlab/bin/activate
# which pip
# pip freeze | wc -l  # 1
#
# pip install --upgrade pip
# pip install --upgrade wheel
#
# pip install pandas
#
# pip install jupyterlab
#
# pip freeze | wc -l  # 71
#
# jupyter notebook --ip=0.0.0.0
