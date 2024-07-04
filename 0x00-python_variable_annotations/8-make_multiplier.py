#!/usr/bin/env bash
"""Module to myltiply number with annotated function"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Function to return multiplier function of multiplier"""
    def multiplier(num: float) -> float:
        """Function to perform multiplication with float"""
        return multiplier * num
    return multiplier
