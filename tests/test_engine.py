"""Unit and stress tests for AsyncEngine scheduler."""

import pytest
import asyncio
from zenith.core.engine import AsyncEngine, EngineConfig


@pytest.mark.asyncio
async def test_engine_basic_execution():
    engine = AsyncEngine()
    await engine.start()
    res = await engine.submit(lambda: 42)
    assert res == 42
    await engine.shutdown()
