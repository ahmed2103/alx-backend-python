#!/usr/bin/env python3
"""Module generates random from 0 to 10 for 10 times asynchronously"""

import asyncio
from random import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """Generates random from 0 to 10 for 10 times asynchronously"""
    for _ in range(10):  # range is sync function so no aiter > iter
        await asyncio.sleep(1)
        yield random() * 10
