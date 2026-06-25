# Makefile
# cookiecutter-repo-governance
#
# Copyright © 2026 Dagitali LLC. All rights reserved.
#
# Local automation for maintaining this Cookiecutter template.
#
# Responsibilities
# - Provide concise entry points for installing development dependencies.
# - Run the same lint, test, and template-validation checks used by CI.
# - Render a disposable sample project for manual inspection.
# - Remove local Python and Cookiecutter build/test artifacts.
#
# Maintainer Notes
# - Keep targets focused on template maintenance, not generated-project
#   application behavior.
# - Keep target names and help text aligned with the supported contributor and
#   CI workflows.
# - Add new validation logic to pytest before adding broad shell checks here.
#
# References
# - GNU Make documentation: https://www.gnu.org/software/make/manual/make.html
# - GNU Make conventions reference: https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html
# - GNU Make include directive reference: https://www.gnu.org/software/make/manual/html_node/Include.html
# - Cookiecutter documentation: https://cookiecutter.readthedocs.io/
# - Python Makefile guide: https://earthly.dev/blog/python-makefile/
# - Python virtualenv Makefile guide: https://stackoverflow.com/questions/24736146/how-to-use-virtualenv-in-makefile
#
# Common Flows
#
# 1) Create venv + install dev tooling and the package (editable).
# $ make dev
#
# 2) Run static checks & tests.
# $ make check
#
# 3) Render a disposable sample project for inspection.
# $ make render
#
# 4) Run the release-readiness command.
# $ make release-check
#
# 5) Clean build artifacts or nuke the venv.
# $ make clean
# $ make clean-venv


# SECTION: INCLUDES ========================================================= #


-include .env


# SECTION: VARIABLES ======================================================== #


### Make ###

.DEFAULT_GOAL := help

### Cookiecutter ###

RENDER_OUTPUT_DIR ?= /tmp/cookiecutter-repo-governance-render

### Python ###

# Python to bootstrap the venv. To override the interpreter, set PY on the CLI:
#   make dev PY=python3.13
#   make dev PY=python3.14
PY ?= python3

# Package root (where pyproject.toml lives)
PKG_DIR := .

# Virtualenv lives inside the package folder
VENV_DIR := $(PKG_DIR)/.venv

# Python formatter width; keep aligned with .ruff.toml:line-length.
PY_LINE_LENGTH ?= 88

# Cross-platform venv bin paths
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV_DIR)/Scripts
	PYTHON := $(VENV_BIN)/python.exe
	PIP := $(VENV_BIN)/pip.exe
else
	VENV_BIN := $(VENV_DIR)/bin
	PYTHON := $(VENV_BIN)/python
	PIP := $(VENV_BIN)/pip
endif

### Testing ###

# Default test marker expression.
# Override with: make test TEST_MARK_EXPRESSION="not perf and not slow"
TEST_MARK_EXPRESSION ?= not perf


# SECTION: PHONY TARGETS ==================================================== #


.PHONY: check
check: doclint lint typecheck test ## Run docstring lint, code lint, type-check, and tests

.PHONY: check-pre-push
check-pre-push: doclint lint typecheck test ## Run the fast mandatory local pre-push guardrails

.PHONY: check-ci-local
check-ci-local: release-check doclint typecheck ## Run the heavier opt-in local CI-parity workflow

.PHONY: clean
clean: ## Remove local build, test, and cache artifacts
	find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name '.pytest_cache' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name '.ruff_cache' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf "$(PKG_DIR)/.mypy_cache" "$(PKG_DIR)/build" "$(PKG_DIR)/dist" "$(PKG_DIR)"/*.egg-info

.PHONY: clean-venv
clean-venv: ## Remove the local virtual environment
	rm -rf "$(VENV_DIR)"

.PHONY: dev
dev: venv ## Install development dependencies into the local virtual environment
	$(PIP) install -e "$(PKG_DIR)[dev]"

.PHONY: doclint
doclint: dev ## Run docstring linters
	find hooks tests -type f -name '*.py' \
		! -path '*/__pycache__/*' \
		-print0 | xargs -0 $(VENV_BIN)/pydocstyle --add-ignore=D102,D401
	$(VENV_BIN)/pydoclint --style numpy hooks tests

.PHONY: fix
fix: dev ## Auto-fix lint violations with Ruff
	$(PYTHON) -m ruff check . --fix

.PHONY: fmt
fmt: fix ## Format Python files with autopep8 normalization
	files="$$(git ls-files '*.py')" && \
	if [ -n "$$files" ]; then \
		$(PYTHON) -m autopep8 --in-place --max-line-length=$(PY_LINE_LENGTH) $$files; \
	fi

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "%-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: venv ## Install the package in editable mode
	$(PIP) install -e "$(PKG_DIR)"

.PHONY: lint
lint: dev ## Run Python lint and formatting-drift checks
	$(PYTHON) -m ruff check .
	files="$$(git ls-files '*.py')" && \
	if [ -n "$$files" ]; then \
		$(PYTHON) -m autopep8 --diff --exit-code --max-line-length=$(PY_LINE_LENGTH) $$files; \
	fi

.PHONY: release-check
release-check: ## Run release-readiness checks without creating a virtual environment
	SKIP=no-commit-to-branch pre-commit run --all-files
	ruff check .
	pytest -q -m "$(TEST_MARK_EXPRESSION)" tests

.PHONY: render
render: dev ## Render a sample project into RENDER_OUTPUT_DIR
	rm -rf "$(RENDER_OUTPUT_DIR)"
	$(PYTHON) -m cookiecutter . --no-input --output-dir "$(RENDER_OUTPUT_DIR)"

.PHONY: show-venv
show-venv: ## Print venv and interpreter locations
	@echo "PKG_DIR    = $(PKG_DIR)"
	@echo "VENV_DIR   = $(VENV_DIR)"
	@echo "VENV_BIN   = $(VENV_BIN)"
	@echo "PYTHON     = $(PYTHON)"
	@echo "PIP        = $(PIP)"

.PHONY: test
test: dev ## Run pytest
	$(PYTHON) -m pytest -q -m "$(TEST_MARK_EXPRESSION)" tests

.PHONY: test-meta
test-meta: dev ## Run repository meta guardrail tests
	$(PYTHON) -m pytest -q tests/meta

.PHONY: typecheck
typecheck: dev ## Type-check post-generation hooks
	$(VENV_BIN)/mypy hooks

.PHONY: venv
venv: ## Create the local virtual environment
	$(PY) -m venv "$(VENV_DIR)"
	$(PIP) install --upgrade pip
