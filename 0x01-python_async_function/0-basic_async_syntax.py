#!/usr/bin/env python3
"""Module for an async function that wait for x time then returns x"""

import asyncio
from random import uniform


async def wait_random(max_delay: int = 10) -> float:
    """Generates random float between 0 and max_delay and returns it"""
    delay = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
