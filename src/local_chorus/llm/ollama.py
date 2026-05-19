"""Thin async client for the local Ollama server.

We intentionally do NOT use the `ollama` SDK — the goal in chapter 1 of the
roadmap is to speak the wire protocol by hand, then graduate. Using httpx
keeps the surface tiny and makes the streaming code explicit.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from local_chorus.config import settings


class OllamaClient:
    """Async client for Ollama's /api/chat endpoint.

    Usage:
        async with OllamaClient() as client:
            reply = await client.chat([{"role": "user", "content": "hi"}])
    """

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float | None = None,
    ) -> None:
        self.base_url = (base_url or settings.ollama_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.timeout_s = timeout_s or settings.request_timeout_s
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> OllamaClient:
        self._client = httpx.AsyncClient(timeout=self.timeout_s)
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _require_client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("OllamaClient must be used inside `async with`.")
        return self._client

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> str:
        """Single-shot chat. Returns the full assistant reply as a string."""
        client = self._require_client()
        resp = await client.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model or self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return str(data.get("message", {}).get("content", ""))

    async def stream(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Stream the assistant reply token-by-token (well, chunk-by-chunk)."""
        client = self._require_client()
        async with client.stream(
            "POST",
            f"{self.base_url}/api/chat",
            json={
                "model": model or self.model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": temperature},
            },
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.strip():
                    continue
                # Ollama streams one JSON object per line.
                chunk = json.loads(line)
                content = chunk.get("message", {}).get("content")
                if content:
                    yield content
                if chunk.get("done"):
                    return


__all__ = ["OllamaClient"]
