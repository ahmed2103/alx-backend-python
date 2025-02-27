#!/usr/bin/env python3
"""Module to fix code and bad annotation in ALX task"""


from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """This is not my function so i will annotate it only"""
    zoomed_in: List = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
