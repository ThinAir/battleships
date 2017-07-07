.DEFAULT_GOAL := test

.PHONY: clean
clean:
	find . -name \*.pyc -delete
	find . -name \*~ -delete

.PHONY: test
test: clean
	python ./test.py

.PHONY: lint
lint:
	pep8 battleship
	pylint --rcfile=.pylintrc battleship

