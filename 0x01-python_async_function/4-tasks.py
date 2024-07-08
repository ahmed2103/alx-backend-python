#!/usr/bin/env python3
"""Module to spawn task multiple n times
and returns the results sorted."""

import asyncio
from typing import List


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Spawns a task n times"""
    task_wait_random = __import__('3-tasks').task_wait_random
    tasks = (task_wait_random(max_delay) for _ in range(n))
    results = await asyncio.gather(*tasks)
    return sorted(results)
