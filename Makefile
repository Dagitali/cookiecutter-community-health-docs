# Makefile
# cookiecutter-repo-governance
#
# Copyright © 2026 Dagitali LLC. All rights reserved.
#
# Local automation for maintaining this Cookiecutter template.
#
# Responsibilities
# - Provide concise entry points for installing development dependencies.
# - Run the same lint and render-test checks used by CI.
# - Render a disposable sample project for manual inspection.
# - Remove local Python and Cookiecutter build/test artifacts.
#
# Maintainer Notes
# - Keep targets focused on template maintenance, not generated-project
#   application behavior.
# - Keep `check` aligned with `.github/workflows/ci.yml`.
# - Add new validation logic to pytest before adding broad shell checks here.
#
# References
# - GNU Make documentation: https://www.gnu.org/software/make/manual/make.html
# - Cookiecutter documentation: https://cookiecutter.readthedocs.io/


# SECTION: VARIABLES ======================================================== #


.DEFAULT_GOAL := help

PY ?= python3
VENV_DIR ?= .venv

ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV_DIR)/Scripts
	PYTHON := $(VENV_BIN)/python.exe
else
	VENV_BIN := $(VENV_DIR)/bin
	PYTHON := $(VENV_BIN)/python
endif

RENDER_OUTPUT_DIR ?= /tmp/cookiecutter-repo-governance-render


# SECTION: PHONY TARGETS ==================================================== #


.PHONY: check
check: lint test ## Run the local CI-equivalent checks

.PHONY: clean
clean: ## Remove local build, test, and cache artifacts
	find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name '.pytest_cache' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name '.ruff_cache' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache build dist *.egg-info

.PHONY: clean-venv
clean-venv: ## Remove the local virtual environment
	rm -rf "$(VENV_DIR)"

.PHONY: dev
dev: venv ## Install development dependencies into the local virtual environment
	$(PYTHON) -m pip install -e ".[dev]"

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "%-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: dev ## Run Ruff checks for hooks and tests
	$(PYTHON) -m ruff check hooks tests

.PHONY: render
render: dev ## Render a sample project into RENDER_OUTPUT_DIR
	rm -rf "$(RENDER_OUTPUT_DIR)"
	$(PYTHON) -m cookiecutter . --no-input --output-dir "$(RENDER_OUTPUT_DIR)"

.PHONY: test
test: dev ## Run pytest
	$(PYTHON) -m pytest

.PHONY: venv
venv: ## Create the local virtual environment
	$(PY) -m venv "$(VENV_DIR)"
	$(PYTHON) -m pip install --upgrade pip
