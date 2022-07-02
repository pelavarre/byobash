# byobash/Makefile:  Run a self test


default: black flake8 selftest
	:
	: PASSED ByoBash SelfTest :
	:


push: default
	# FIXME: solve cd.py inside
	# FIXME:    for F in $(find . |grep '[.]py$'); do python3 $F >/dev/null; done
	: did you mean:  git push
	: press ⌃D to execute, or ⌃C to quit
	cat -
	git push


black:
	. ~/bin/pips.source && black $$PWD/../byobash/


FLAKE8_OPTS=--max-line-length=999 --ignore=E203,W503
# --max-line-length=999  # Black max line lengths over Flake8 max line lengths
# --ignore=E203  # Black '[ : ]' rules over Flake8 E203 whitespace before ':'
# --ignore=W503  # 2017 Pep 8 and Black over Flake8 W503 line break before binary op


flake8:
	. ~/bin/pips.source && flake8 ${FLAKE8_OPTS} $$PWD/../byobash/


selftest:
	:
	rm -fr bin/__pycache__/
	:
	bin/cat_bashrc_source.py
	:
	PATH="$$PATH:$$PWD/bin" bin/cat_bashrc_source.py
	:
	/bin/bash -c 'source <(bin/cat_bashrc_source.py)'
	python -c ''  # call twice to workaround 'bash -c' returning too soon
	python -c ''
	:
	rm -fr bin/__pycache__/
	:


setup:
	exit 3

	mkdir -p ~/.venvs
	cd ~/.venvs/
	rm -fr pips/  # casually destructive

	python3 -m venv --prompt PIPS pips
	source pips/bin/activate  # works in Bash, doesn't work inside Makefile's

	which pip
	pip freeze |wc -l  # often 0

	pip install --upgrade pip
	pip install --upgrade wheel

	pip install --upgrade black
	pip install --upgrade flake8  # includes:  pip install --upgrade mccabe
	pip install --upgrade flake8-import-order

	pip freeze |wc -l  # often 11


#
# quirks:
#
#   1 ) Linux Sh understands '.' but does Not understand 'source'
#   2 ) work through our 'setup:' instructions to get your own '. ~/bin/pips.source'
#


# copied from:  git clone https://github.com/pelavarre/byobash.git
