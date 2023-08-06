clean: clean-build clean-pyc clean-sha256 ## remove all build, test, coverage and Python artifacts

project = library

uninstall: distclean
	rm -fr py.typed
	rm -fr __init__.py
	rm -fr setup.py
	rm -fr pyproject.toml
	find . -name '$(project)*' -not -name '*.wom' -exec rm -fr {} +

distclean: clean-build clean-pyc clean-sha256
	rm -fr Makefile

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-sha256:
	find . -name '*.sha256' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
