"""local-chorus — a local-first AI assistant.

The package exposes a few high-level entry points; everything heavier
(model clients, vector stores, audio pipelines) lives in dedicated
subpackages and is imported lazily so `import local_chorus` stays cheap.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("local-chorus")
except PackageNotFoundError:  # editable install before first build
    __version__ = "0.0.0+dev"

__all__ = ["__version__"]
