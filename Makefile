# byobash/Makefile:  Run a self test


default:
	@echo ''
	@echo 'ls'
	@echo ''
	@echo 'open https://github.com/pelavarre/byobash/blob/main/QuickStart.md'
	@echo 'open https://github.com/pelavarre/byobash#readme'
	@echo 'open https://github.com/pelavarre/byobash/blob/main/ReadMore.md'
	@echo 'open https://twitter.com/intent/tweet?text=@PLaVarre'
	@echo ''
	@echo 'make help'
	@echo 'make push'
	@echo ''



help:
	:
	:
	: # usage: make [black|flake8|help|push|selftest|setup]
	:
	: come work with me now to make me feel more agency and power
	:
	: examples:
	:
	:   ls
	:
	:   open https://github.com/pelavarre/byobash/blob/main/QuickStart.md
	:   open https://github.com/pelavarre/byobash#readme
	:   open https://github.com/pelavarre/byobash/blob/main/ReadMore.md
	:
	:   open https://twitter.com/intent/tweet?text=@PLaVarre
	:
	:


push: black flake8 selftest
	git log --oneline --no-decorate -1
	git status --short --ignored
	git describe --always --dirty
	:
	: did you mean:  git push
	: press ⌃D to execute, or ⌃C to quit
	cat -
	git push


black:
	. ~/bin/pips.source && black $$PWD/../byobash/


FLAKE8_OPTS=--max-line-length=999 --max-complexity 10 --ignore=E203,W503
# --max-line-length=999  # Black max line lengths over Flake8 max line lengths
# --ignore=E203  # Black '[ : ]' rules over Flake8 E203 whitespace before ':'
# --ignore=W503  # 2017 Pep 8 and Black over Flake8 W503 line break before binary op


flake8:
	. ~/bin/pips.source && flake8 ${FLAKE8_OPTS} $$PWD/../byobash/


selftest:
	:
	for F in $$(find . |grep '[.]py$$' |sort); do python3 $$F >/dev/null; done
	rm -fr bin/__pycache__/
	:
# as if:  for F in $(find . |grep '[.]py$' |sort); do python3 $F >/dev/null; done


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


# posted into:  https://github.com/pelavarre/byobash/blob/main/Makefile
# copied from:  git clone https://github.com/pelavarre/byobash.git
