# Contributing

This is a personal learning project, but PRs are welcome — keep your
expectations honest.

## Project state

I work on this in evenings and weekends. Response time on issues / PRs is
typically 1-2 weeks. The roadmap is fixed (it tracks the AgentForge
curriculum) so feature requests outside it will probably be declined.

## Setup

```bash
uv sync
uv run pre-commit install
make all  # lint + typecheck + test should pass green
```

## Pull requests

- Run `make all` before opening a PR.
- One concern per PR. Refactors and features in separate PRs.
- Add a test if you fix a bug.
- Commit messages: imperative, lowercase, no trailing period.
  Example: `fix ollama client timeout when server is slow`.

## Style

- Python 3.12 minimum.
- Type hints everywhere in `src/`. Tests can skip them.
- Prefer `pathlib` over `os.path`.
- Prefer `loguru` over `print` and `logging`.
- Async by default for I/O.

## Code of conduct

Be kind, be precise.
