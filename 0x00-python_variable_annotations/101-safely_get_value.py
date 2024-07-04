#!/usr/bin/env python3
"""Module to annotate function in ALX task"""


from typing import Mapping, Any, Union, TypeVar


T = TypeVar('T')


def safely_get_value(dct: Mapping,
                     key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """This is not my function so i will annotate it only"""
    if key in dct:
        return dct[key]
    else:
        return default
