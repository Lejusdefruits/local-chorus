"""Unit tests for the OllamaClient. No real server hit — httpx is mocked."""

from __future__ import annotations

import httpx
import pytest

from local_chorus.llm.ollama import OllamaClient


@pytest.mark.asyncio
async def test_chat_returns_message_content():
    """Single-shot chat returns the assistant's content string."""
    expected = "hello back"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/chat"
        return httpx.Response(
            200,
            json={"message": {"role": "assistant", "content": expected}, "done": True},
        )

    transport = httpx.MockTransport(handler)
    async with OllamaClient(base_url="http://fake") as client:
        client._client = httpx.AsyncClient(transport=transport)  # type: ignore[assignment]
        reply = await client.chat([{"role": "user", "content": "hi"}])
        assert reply == expected


@pytest.mark.asyncio
async def test_stream_yields_chunks():
    """Streaming yields each chunk's content and stops on `done`."""
    chunks = [
        b'{"message":{"content":"hel"},"done":false}\n',
        b'{"message":{"content":"lo"},"done":false}\n',
        b'{"message":{"content":""},"done":true}\n',
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"".join(chunks))

    transport = httpx.MockTransport(handler)
    async with OllamaClient(base_url="http://fake") as client:
        client._client = httpx.AsyncClient(transport=transport)  # type: ignore[assignment]
        out: list[str] = []
        async for chunk in client.stream([{"role": "user", "content": "hi"}]):
            out.append(chunk)
        assert "".join(out) == "hello"


@pytest.mark.asyncio
async def test_requires_context_manager():
    """Using the client outside `async with` raises a clear error."""
    client = OllamaClient(base_url="http://fake")
    with pytest.raises(RuntimeError, match="async with"):
        await client.chat([{"role": "user", "content": "hi"}])
