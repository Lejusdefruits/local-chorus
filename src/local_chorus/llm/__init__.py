"""Local LLM clients.

This package wraps the local inference layer (Ollama for now, llama.cpp
direct later). The public surface stays tiny: a `ChatClient` protocol so the
rest of the app does not care which backend is running.
"""
