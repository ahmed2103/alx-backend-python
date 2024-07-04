#!/usr/bin/env python3
"""Module to implement an annotated function that return the params in another shape"""


from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Returns the string and the square of the float in a tuple"""
    return (k, float(v*v))
