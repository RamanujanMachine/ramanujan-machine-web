"""Utility functions that generate graphable coordinate pairs for the frontend"""
import logging
from typing import TypedDict

import mpmath
import sympy

import math_utils

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    x: int
    y: str


def error_coordinates(values: list[mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error of an expression log(|expression - L|) in terms of symbol
    :param values: computed values for continued fraction
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for i in range(0, len(values)):
        if values[i] is not None:
            logger.debug(
                f"{i} {values[i]} difference: {values[i] - limit} abs: {abs(values[i] - limit)} log10: {mpmath.log10(abs(values[i] - limit))}")
            x_y_pairs.append(Point2D(x=i, y=str(mpmath.log10(abs(values[i] - limit)))))

    return x_y_pairs


def delta_coordinates(values: list[mpmath.mpf], q_values: list[mpmath.mpf],
                      limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1 in terms of symbol
    :param values: computed values for continued fraction
    :param q_values: computed values for continued fraction - denominator only
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    for i in range(0, min(len(values), len(q_values))):
        if values[i] is not None and q_values[i] is not None:
            x_y_pairs.append(Point2D(x=i, y=str(-1 * math_utils.delta(values[i], q_values[i], limit))))

    return x_y_pairs
