#!/usr/bin/env python3
"""Module to sum a list of float and integers with annotated function"""


from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, float]]) -> float:
    """Signed function returns sum a list of float and integers"""
    return float(sum(mxd_list))
