# local-chorus

A local-first AI assistant. Local LLMs, local memory, local voice. No cloud anywhere.

Built in public over 12 months following the [AgentForge roadmap](https://github.com/lejusdefruits/agentforge).

## Status

Pre-alpha. Chapter 1 of 6 — `The Local Awakens`.

## Quickstart

```bash
# 1. Install uv (one-time): https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sync the env
uv sync

# 3. Install pre-commit hooks
uv run pre-commit install

# 4. Confirm it works
uv run chorus status
uv run chorus hello juu
```

## What works today

- [x] `chorus status` — prints resolved config
- [x] `chorus hello <name>` — smoke test
- [x] `OllamaClient` — async client for `/api/chat` (single + streaming)
- [ ] Local model bench (q04)
- [ ] OpenAI-shape API wrapper (q06)
- [ ] Tool-calling loop (q09)
- [ ] RAG layer (chapter 3)
- [ ] Voice IO (chapter 6)

The TODO list mirrors the AgentForge roadmap.

## Repo layout

```
local-chorus/
├── src/local_chorus/    # the installable package
│   ├── cli.py           # `chorus` entrypoint (typer)
│   ├── config.py        # pydantic-settings, .env loading
│   ├── logging.py       # loguru setup
│   ├── llm/             # local model clients
│   ├── voice/           # STT / TTS / wake word
│   ├── agents/          # tool calling, ReAct
│   ├── rag/             # embeddings, retrieval, memory
│   └── eval/            # golden sets, regression tests
├── tests/               # pytest, asyncio-aware
├── pyproject.toml       # deps + tooling config
├── Makefile             # common commands
└── .pre-commit-config.yaml
```

## Common commands

```bash
make help           # list targets
make install        # uv sync + pre-commit install
make lint           # ruff check
make format         # ruff format
make typecheck      # mypy
make test           # pytest
make all            # lint + typecheck + test
make run            # python -m local_chorus
make clean          # nuke .venv, .cache, __pycache__
```

## Config

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

All env vars are prefixed `LOCAL_CHORUS_*` so they don't collide.

## Requirements

- Python 3.12+
- Ollama running on `http://localhost:11434` (default)
- For voice features (later): `whisper.cpp`, `piper-tts`, `openWakeWord`

## License

MIT — see [LICENSE](LICENSE).

## Why "local-chorus"?

A chorus is many voices in one piece. The assistant is several small models
(triage, planner, executor, critic) working together, all running locally on
my own hardware.
