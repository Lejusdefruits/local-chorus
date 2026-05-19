"""Smoke tests — confirm the install + entrypoints are wired."""

import local_chorus
from local_chorus.config import settings


def test_package_imports_cheaply():
    """Importing the top-level package must not crash."""
    assert hasattr(local_chorus, "__version__")
    assert isinstance(local_chorus.__version__, str)


def test_settings_have_defaults():
    """Config singleton loads without a .env file present."""
    assert settings.ollama_url.startswith("http")
    assert settings.ollama_model
    assert settings.request_timeout_s > 0


def test_cli_hello(cli, cli_app):
    """`chorus hello` smoke."""
    result = cli.invoke(cli_app, ["hello", "test"])
    assert result.exit_code == 0
    assert "hello, test" in result.stdout


def test_cli_status(cli, cli_app):
    """`chorus status` returns 0 and prints the table."""
    result = cli.invoke(cli_app, ["status"])
    assert result.exit_code == 0
    assert "ollama_url" in result.stdout
