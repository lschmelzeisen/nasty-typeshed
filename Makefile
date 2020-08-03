# See: https://blog.thapaliya.com/posts/well-documented-makefiles/
help: ##- Show this help message.
	@awk 'BEGIN {FS = ":.*##-"; printf "usage: make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z0-9_-]+:.*##-/ { printf "  \033[36m%-29s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
.PHONY: help

# ------------------------------------------------------------------------------

.venv:
	@python3.6 -m venv .venv

.venv/.devinstall: .venv
	@.venv/bin/pip install --upgrade pip setuptools wheel
	@grep git+git setup.cfg | awk '{ gsub (" ", "", $$0); print}' | xargs -r .venv/bin/pip install --upgrade
	@.venv/bin/pip install -e .[test,dev]
	@touch .venv/.devinstall

devinstall: ##- Install the project in editable mode with all test and dev dependencies (in a virtual environment).
	@rm -f .venv/.devinstall
	@make --silent .venv/.devinstall
.PHONY: devinstall

# ------------------------------------------------------------------------------

test: .venv/.devinstall ##- Test type-checking in the currently active environment.
	@.venv/bin/mypy .
	@ls src --ignore=*.egg-info | xargs printf -- '-p %s\n' | xargs .venv/bin/mypy
.PHONY: test

test-nox: .venv/.devinstall ##- Test type-checking against all supported Python versions (in separate environments).
	@.venv/bin/nox
.PHONY: test-nox

# ------------------------------------------------------------------------------

check: check-flake8 check-isort check-black ##- Run linters and perform static type-checking.
.PHONY: check

# Not using the following in `check`-rule because it always spams output, even
# in case of success (no quiet flag) and because most of the checking is already
# performed by flake8.
check-autoflake: .venv/.devinstall ##- Check for unused imports and variables.
	@.venv/bin/autoflake --check --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --recursive .
.PHONY: check-autoflake

check-flake8: .venv/.devinstall ##- Run linters.
	@.venv/bin/flake8 src *.py
.PHONY: check-flake8

check-isort: .venv/.devinstall ##- Check if imports are sorted correctly.
	@.venv/bin/isort --check-only --quiet .
.PHONY: check-isort

check-black: .venv/.devinstall ##- Check if code is formatted correctly.
	@.venv/bin/black --check .
.PHONY: check-black


# ------------------------------------------------------------------------------

format: format-licenseheaders format-autoflake format-isort format-black ##- Auto format all code.
.PHONY: format

format-licenseheaders: .venv/.devinstall ##- Prepend license headers to all code files.
	@.venv/bin/licenseheaders --tmpl LICENSE.header --years 2019-2020 --owner "Lukas Schmelzeisen" --dir src --additional-extensions python=.pyi
.PHONY: format-licenseheaders

format-autoflake: .venv/.devinstall ##- Remove unused imports and variables.
	@.venv/bin/autoflake --in-place --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --recursive .
.PHONY: format-autoflake

format-isort: .venv/.devinstall ##- Sort all imports.
	@.venv/bin/isort --quiet .
.PHONY: format-isort

format-black: .venv/.devinstall ##- Format all code.
	@.venv/bin/black .
.PHONY: format-black

# ------------------------------------------------------------------------------

publish: publish-setuppy publish-twine-check ##- Build and check source and binary distributions.
.PHONY: publish

publish-setuppy: .venv/.devinstall #-- Build source and binary distributions.
	@rm -rf build dist
	@.venv/bin/python setup.py sdist bdist_wheel
.PHONY: publish-setuppy

publish-twine-check: .venv/.devinstall ##- Check source and binary distributions for upload.
	@.venv/bin/twine check dist/*
.PHONY: publish-twine-check

publish-twine-upload-testpypi: .venv/.devinstall ##- Upload to TestPyPI.
	@.venv/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*
.PHONY: publish-twine-upload-testpypi

publish-twine-upload: .venv/.devinstall ##- Upload to PyPI.
	@.venv/bin/twine upload dist/*
.PHONY: publish-twine-upload

# ------------------------------------------------------------------------------

clean: ##- Remove all created cache/build files, and virtual environments.
	@rm -rf .eggs .mypy_cache .nox .venv build dist src/*/_version.py src/*.egg-info
	@find . -type d -name __pycache__ -exec rm -r {} +
.PHONY: clean
