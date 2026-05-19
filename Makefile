# local-chorus — common commands. Run `make help` for the list.
#
# Tab-indented (Makefile rule).
.DEFAULT_GOAL := help
.PHONY: help install sync lint format typecheck test test-cov all run clean pre-commit-run

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Sync deps + install pre-commit hooks. First-run command.
	uv sync
	uv run pre-commit install

sync: ## Re-sync deps (after editing pyproject.toml).
	uv sync

lint: ## Lint with ruff.
	uv run ruff check src tests

format: ## Format with ruff.
	uv run ruff format src tests

typecheck: ## Static-type check with mypy.
	uv run mypy src/local_chorus

test: ## Run the test suite.
	uv run pytest

test-cov: ## Run tests with coverage report.
	uv run pytest --cov=local_chorus --cov-report=term-missing

all: lint typecheck test ## Run lint + typecheck + test.

run: ## Run the CLI (passes ARGS along, e.g. `make run ARGS="status"`).
	uv run chorus $(ARGS)

pre-commit-run: ## Run all pre-commit hooks on every file.
	uv run pre-commit run --all-files

clean: ## Remove .venv, caches, build artifacts.
	rm -rf .venv .pytest_cache .ruff_cache .mypy_cache __pycache__ .coverage htmlcov dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
