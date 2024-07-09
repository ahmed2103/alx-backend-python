#!/usr/bin/env python3
"""Module to implement comprehension from async generator"""


import asyncio
from typing import List


async def async_comprehension() -> List[float]:
    """Comprehension from async generator returning list of floats"""
    async_generator = __import__('0-async_generator').async_generator
    return [_ async for _ in async_generator()]
