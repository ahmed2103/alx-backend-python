#!/usr/bin/env python3
"""Task to annotate funcion"""


from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """This is not my function so i will annotate it only"""
    return [(i, len(i)) for i in lst]
