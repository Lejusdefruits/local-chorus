"""Shared pytest fixtures."""

import pytest
from typer.testing import CliRunner

from local_chorus.cli import app


@pytest.fixture
def cli() -> CliRunner:
    """A typer CliRunner. Stderr is captured separately by default."""
    return CliRunner()


@pytest.fixture
def cli_app():
    """The typer app under test."""
    return app
