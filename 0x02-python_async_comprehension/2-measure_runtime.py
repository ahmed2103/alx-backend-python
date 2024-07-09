#!/usr/bin/env python3
"""Module to benchmark the runtime of an async function"""

from asyncio import gather
from time import perf_counter


async def measure_runtime() -> float:
    """Measure the runtime of a function"""
    async_comprehension = (__import__('1-async_comprehension')
                           .async_comprehension)
    start = perf_counter()
    await gather(*[async_comprehension() for _ in range(4)])
    end = perf_counter()
    return end - start
