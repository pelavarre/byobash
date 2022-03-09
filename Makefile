# byobash/Makefile:  Run the self-test's


default: black flake8 selftest
	:
	: PASSED ByoBash SelfTest :
	:


black:
	source ~/bin/pips.source && black $$PWD/../byobash/


FLAKE8_OPTS=--max-line-length=999 --ignore=E203,W503
# --max-line-length=999  # Black max line lengths over Flake8 max line lengths
# --ignore=E203  # Black '[ : ]' rules over Flake8 E203 whitespace before ':'
# --ignore=W503  # 2017 Pep 8 and Black over Flake8 W503 line break before binary op


flake8:
	source ~/bin/pips.source && flake8 ${FLAKE8_OPTS} $$PWD/../byobash/


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

# copied from:  git clone https://github.com/pelavarre/byobash.git
