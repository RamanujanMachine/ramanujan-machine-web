"""Utility functions that generate graphable coordinate pairs for the frontend"""
import logging
from typing import TypedDict, OrderedDict

import mpmath
import sympy

from constants import DEBUG_LINES
from math_utils import cpython_gcd

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    """
    a type used to store coordinate pairs
    """
    x: int
    y: str


def growth_coordinates(numerator_values: OrderedDict[int, mpmath.mpf],
                       denominator_values: OrderedDict[int, mpmath.mpf]) -> list[Point2D]:
    """
    graph coords for the growth rate of an expression: denominator / gcd(numerator, denominator)
    :param numerator_values: computed values for continued fraction
    :param denominator_values: computed values for continued fraction
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for n in numerator_values.keys():
        if (n >= 1
                and numerator_values[n] is not None
                and denominator_values[n] is not None
                and denominator_values[n] != 0):
            # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
            # which is a gauge of the proximity of the value at n to the "limit"
            y_value = (denominator_values[n]) / cpython_gcd(denominator_values[n], numerator_values[n])
            if n <= DEBUG_LINES:
                logger.debug(f"Growth at {n}: {y_value} ")

            x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def error_coordinates(values: OrderedDict[int, mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error of an expression: log(|expression - L|)
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for n in values.keys():
        if n >= 1 and values[n] is not None:
            # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
            # which is a gauge of the proximity of the value at n to the "limit"
            difference = mpmath.fabs(values[n] - limit)
            y_value = mpmath.log10(difference)

            if n <= DEBUG_LINES:
                logger.debug(f"Error {n} {values[n]} difference: {difference} log10: {y_value}")

            x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def slope_of_error_coordinates(values: OrderedDict[int, mpmath.mpf], limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the slope of the error of an expression: (y_2 - y_1) / (x_2 - x_1)
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    error_vals = error_coordinates(values, limit)
    for n in range(1, len(error_vals)):
        y_value = mpmath.fabs(mpmath.mpf(error_vals[n]['y']) - mpmath.mpf(error_vals[n - 1]['y']))
        if n <= DEBUG_LINES:
            logger.debug(f"error slope at {n}: {y_value}")

        x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def delta_coordinates(values: OrderedDict[int, mpmath.mpf], p_values: OrderedDict[int, mpmath.mpf],
                      q_values: OrderedDict[int, mpmath.mpf],
                      limit: mpmath.mpf) -> list[Point2D]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param p_values: computed values for continued fraction - numerator only
    :param q_values: computed values for continued fraction - denominator only
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    for n in values.keys():
        # we test for values that would generate irrational results or exceptions
        # e.g. divide by zero when taking log10 of 1
        # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
        # which is a gauge of the proximity of the value at n to the "limit"
        # in this case we are then comparing that precision to the precision of the denominator
        if (n >= 1
                and values[n] is not None
                and q_values[n] is not None
                and q_values[n] > 0
                and q_values[n] != 1):
            error = mpmath.log10(mpmath.fabs(values[n] - limit))
            reduced_q = mpmath.fabs(q_values[n] / cpython_gcd(p_values[n], q_values[n]))
            y_value = - 1 - (error / mpmath.log10(reduced_q))
            if n <= DEBUG_LINES:
                logger.debug(f"Delta {n} {y_value}")

            x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def delta_n_coordinates(a_n: OrderedDict[int, mpmath.mpf], b_n: OrderedDict[int, mpmath.mpf]) -> list[Point2D]:
    """
    computes delta n = 1 + 4b_n/(a_n*a_n-1)
    :param a_n: computed values for a
    :param b_n: computed values for b
    """
    x_y_pairs = []
    for n in a_n.keys():
        if n >= 1 and (a_n[n] * a_n[n - 1]) != 0:
            result = mpmath.mpf(1) + mpmath.mpf(4) * b_n[n] / (a_n[n] * a_n[n - 1])
            x_y_pairs.append(Point2D(x=n, y=str(result)))
    return x_y_pairs
