#!/usr/bin/env python3
"""Module to spawn wait function multiple n times
and returns the results sorted."""

import asyncio
from typing import List


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Spawns a wait function n times"""
    wait_random = __import__('0-basic_async_syntax').wait_random
    objects = [wait_random(max_delay) for _ in range(n)]
    # Coroutine objects are lazy evaluated
    results = await asyncio.gather(*objects)
    return sorted(results)
