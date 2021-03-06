unittest-args = -m unittest discover --start-directory tests --top-level-directory .

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  docs-clean    Remove documentation."
	@echo "  docs-doctest  Check code samples in the documentation."
	@echo "  docs-html     Compile documentation to HTML."
	@echo "  lint          Run flake8 and pylint."
	@echo "  test          Run unit tests."
	@echo "  test-all      Run unit tests and doctests, measure coverage."

docs-clean:
	cd docs && $(MAKE) clean

docs-doctest:
	cd docs && $(MAKE) doctest

docs-html:
	cd docs && $(MAKE) html

lint:
	flake8 .
	pylint --reports=n --disable=I --ignore-imports=y fauxfactory docs/conf.py setup.py
# pylint should also lint the tests/ directory.

test:
	python $(unittest-args)

test-all: lint docs-doctest
	coverage run $(unittest-args)

.PHONY: help docs-clean docs-doctest docs-html lint test test-all
