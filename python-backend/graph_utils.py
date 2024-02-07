"""Utility functions that generate graphable coordinate pairs for the frontend"""
import logging
from typing import TypedDict

import mpmath
import sympy

from constants import DEBUG_LINES

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    x: int
    y: str


def error_coordinates(values: list[mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error of an expression log(|expression - L|)
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for i in range(0, len(values)):
        if values[i] is not None:
            # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
            # which is a gauge of the proximity of the value at n to the "limit"
            y_value = mpmath.log10(abs(values[i] - limit))
            if i <= DEBUG_LINES:
                logger.debug(f"Error {i} {values[i]} difference: {values[i] - limit} "
                             f"abs: {abs(values[i] - limit)} log10: {y_value}")

            x_y_pairs.append(Point2D(x=i, y=str(y_value)))

    return x_y_pairs


def slope_of_error_coordinates(values: list[mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error of an expression log(|expression - L|)
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    error_vals = error_coordinates(values, limit)
    for i in range(1, len(error_vals)):
        y_value = mpmath.mpf(error_vals[i]['y']) - mpmath.mpf(error_vals[i - 1]['y'])
        if i <= DEBUG_LINES:
            logger.debug(f"error slope at {i}: {y_value}")

        x_y_pairs.append(Point2D(x=i, y=str(y_value)))

    return x_y_pairs


def delta_coordinates(values: list[mpmath.mpf], q_values: list[mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param q_values: computed values for continued fraction - denominator only
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    for i in range(1, min(len(values), len(q_values))):
        # we test for values that would generate irrational results or exceptions
        # e.g. divide by zero when taking log10 of 1
        # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
        # which is a gauge of the proximity of the value at n to the "limit"
        # in this case we are then comparing that precision to the precision of the denominator
        if values[i] is not None and q_values[i] is not None and q_values[i] > 0 and q_values[i] != 1:
            y_value = (mpmath.mpf(-1) *
                       (mpmath.log10(abs(values[i] - limit)) / mpmath.log10(q_values[i]))
                       - mpmath.mpf(1))
            if i <= DEBUG_LINES:
                logger.debug(f"Delta {i} {y_value}")

            x_y_pairs.append(Point2D(x=i, y=str(y_value)))

    return x_y_pairs
