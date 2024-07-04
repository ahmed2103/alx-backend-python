#!/usr/bin/env python3
"""Module to implement an annotated function that return the params in another shape"""


from typing import Tuple, Union


def to_kv(k: str, v: Tuple[Union[int, float]]) -> Tuple[str, float]:
    """Crazy function with no purpose except learning annotation"""
    return k, float(v*v)
