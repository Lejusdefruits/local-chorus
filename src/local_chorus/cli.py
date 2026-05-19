"""Command-line entrypoint, exposed as `chorus` via [project.scripts].

Subcommands are added as they get implemented. For now the CLI just proves
the install works and prints a small status table.
"""

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import settings
from .log import logger

app = typer.Typer(
    name="chorus",
    help="local-chorus — a local-first AI assistant.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def hello(
    name: str = typer.Argument("world", help="Name to greet."),
) -> None:
    """Smoke test — prints a greeting via the logger and rich."""
    logger.info("CLI invoked with name={}", name)
    console.print(f"[bold green]hello, {name}[/]")


@app.command()
def status() -> None:
    """Show resolved runtime configuration. Useful for debugging .env."""
    table = Table(title="local-chorus · runtime config", title_style="bold")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("version", __version__)
    table.add_row("ollama_url", settings.ollama_url)
    table.add_row("ollama_model", settings.ollama_model)
    table.add_row("ollama_embed_model", settings.ollama_embed_model)
    table.add_row("request_timeout_s", str(settings.request_timeout_s))
    table.add_row("log_level", settings.log_level)
    table.add_row("data_dir", str(settings.data_dir))
    table.add_row("cache_dir", str(settings.cache_dir))
    console.print(table)


def main() -> None:
    """Entrypoint for `python -m local_chorus` and the installed script."""
    app()


if __name__ == "__main__":
    main()
