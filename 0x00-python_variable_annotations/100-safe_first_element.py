#!/usr/bin/env python3
"""Module to annotate function in ALX task"""


from typing import Any, Union, Sequence


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """This is not my function so i will annotate it only"""
    if lst:
        return lst[0]
    else:
        return None
