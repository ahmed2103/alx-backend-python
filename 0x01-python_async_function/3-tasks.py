#!/usr/bin/env python3
"""Module to return an async task after waiting"""


from asyncio import create_task, Task


def task_wait_random(max_delay: int) -> Task:
    """returns a random async task after waiting max_delay in sec"""
    wait_random = __import__('0-basic_async_syntax').wait_random
    return create_task(wait_random(max_delay))
