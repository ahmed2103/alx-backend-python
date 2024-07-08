#!/usr/bin/env python3
"""Module that measures the avg of the runtime
for a multiple coroutine"""

from asyncio import run
from time import perf_counter


def measure_time(n: int, max_delay: int) -> float:
    """measures the runtime of a coroutines avg"""
    wait_n = __import__('1-concurrent_coroutines').wait_n
    start = perf_counter()
    run(wait_n(n, max_delay))
    end = perf_counter()
    elapsed = end - start
    return elapsed / n
