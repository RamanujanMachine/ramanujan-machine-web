"""Utility functions that generate graphable coordinate pairs for the frontend"""
import logging
from typing import TypedDict

import mpmath
import sympy

from constants import DEBUG_LINES

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    """
    a type used to store coordinate pairs
    """
    x: int
    y: str


def error_coordinates(values: dict[int, mpmath.mpf], limit: mpmath.mpf, iterations: int) -> list[Point2D]:
    """
    graph coords for the error of an expression: |expression - L|
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param iterations: the number of values expected
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for n, value in values.items():
        if 1 <= n <= iterations and value is not None:
            # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
            # which is a gauge of the proximity of the value at n to the "limit"
            y_value = mpmath.fabs(mpmath.fsub(value, limit))

            if mpmath.almosteq(value, limit):
                logger.debug(f"Precision exhausted - difference is zero (string comparison)")
                break

            if n <= DEBUG_LINES:
                logger.debug(f"Error at {n} |{value}-{limit}| = {y_value}")

            x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def error_log_coordinates(error_values: list[Point2D],
                          values: dict[int, mpmath.mpf],
                          limit: mpmath.mpf,
                          iterations: int) -> list[Point2D]:
    """
    graph coords for the error log (i.e. digits of precision) of an expression: |log_10(|expression - L|)|
    :param error_values: output of error_coordinates()
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param iterations: the number of values expected
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for i in range(0, min(iterations, len(error_values) - 1)):
        if values[i] is not None and str(error_values[i]['y']) != '0.0':
            # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
            # which is a gauge of the proximity of the value at n to the "limit"
            n = error_values[i]['x']
            y_value = mpmath.fabs(mpmath.log10(error_values[i]['y']))

            if str(error_values[i]['y']) == '0.0':
                logger.debug(f"cannot take log10 of zero")

            if not mpmath.isinf(y_value):
                if i <= DEBUG_LINES:
                    logger.debug(f"log10 error at {n} |log10(|{values[n]}-{limit}|)| = {y_value}")
                x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def slope_of_error_coordinates(error_values: list[Point2D], iterations: int) -> list[Point2D]:
    """
    graph coords for the slope of the error of an expression: (y_2 - y_1) / (x_2 - x_1)
    (where the denom is always 1, so we don't bother computing it)
    :param error_values: computed error values from error_coordinates()
    :param iterations: the number of values expected
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    for i in range(1, min(iterations, len(error_values) - 1)):
        n = error_values[i]['x']
        y_value = mpmath.fabs(mpmath.fsub(error_values[i]['y'], error_values[i - 1]['y']))
        if i <= DEBUG_LINES:
            logger.debug(f"slope of error at {n}: {y_value}")

        x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def delta_coordinates(values: dict[int, mpmath.mpf],
                      q_values: dict[int, mpmath.mpf],
                      limit: mpmath.mpf,
                      iterations: int) -> list[Point2D]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param q_values: computed values for continued fraction - denominator only
    :param iterations: the number of values expected
    :return: array of [x,y] pairs for graphing purposes
    """
    x_y_pairs = []
    # |\frac{p_n}{q_n} - L|
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    for n in values.keys():
        # we test for values that would generate irrational results or exceptions
        # e.g. divide by zero when taking log10 of 1
        # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
        # which is a gauge of the proximity of the value at n to the "limit"
        # in this case we are then comparing that precision to the precision of the denominator
        if (iterations >= n >= 1
                and values[n] is not None
                and q_values[n] is not None
                and q_values[n] > 0
                and q_values[n] != 1
                and str(q_values[n]) != '0.0' and str(values[n] - limit) != '0.0'):

            if mpmath.almosteq(limit, values[n]):
                break

            error = mpmath.log10(mpmath.fabs(mpmath.fsub(values[n], limit)))
            q = mpmath.log10(mpmath.fabs(q_values[n]))

            if mpmath.almosteq(q, mpmath.mpf(0)):
                break

            y_value = mpmath.fsub(-1, (mpmath.fdiv(error, q)))

            if not mpmath.isinf(y_value):
                if n <= DEBUG_LINES:
                    logger.debug(
                        f"Delta at {n}: - 1 - log10(|{values[n]} - {limit}|) / log10(|{q_values[n]}|) = {y_value}")
                x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs


def reduced_delta_coordinates(values: dict[int, mpmath.mpf],
                              p_values: dict[int, mpmath.mpf],
                              q_values: dict[int, mpmath.mpf],
                              limit: mpmath.mpf,
                              iterations: int) -> list[Point2D]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param values: computed values for continued fraction
    :param limit: the limit of the expression as computed by PCF(a_n, b_n).limit()
    :param p_values: computed values for continued fraction - numerator only
    :param q_values: computed values for continued fraction - denominator only
    :param iterations: the number of values expected
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
        if (iterations >= n >= 1
                and values[n] is not None
                and q_values[n] is not None
                and q_values[n] > 0
                and q_values[n] != 1
                and str(q_values[n]) != '0.0'
                and str(values[n] - limit) != '0.0'):

            gcd = sympy.gcd(sympy.Rational(str(p_values[n])), sympy.Rational(str(q_values[n])))
            if mpmath.almosteq(gcd, mpmath.mpf(0)):
                break

            reduced_q = mpmath.fabs(mpmath.fdiv(q_values[n], gcd))
            if mpmath.almosteq(limit, values[n]):
                break

            y_value = mpmath.fsub(-1, mpmath.log(mpmath.fabs(mpmath.fsub(limit, values[n])), reduced_q))

            if not mpmath.isinf(y_value):
                if n <= DEBUG_LINES:
                    logger.debug(
                        f"Reduced delta at {n}: -1 - (log10(|{values[n]} - {limit}|) / log10(|{q_values[n]} / {gcd}|)) "
                        f"= {y_value}")
                x_y_pairs.append(Point2D(x=n, y=str(y_value)))

    return x_y_pairs
