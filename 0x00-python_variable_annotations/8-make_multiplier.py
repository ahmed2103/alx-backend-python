#!/usr/bin/env bash
"""Module to myltiply number with annotated function"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Function to return multiplier function of multiplier"""
    return lambda num: num * multiplier
