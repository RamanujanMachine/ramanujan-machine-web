"""Utility functions that generate graphable coordinate pairs for the frontend"""
import json
import logging
from typing import TypedDict

import mpmath
import sympy
from fastapi import WebSocket

from constants import DEBUG_LINES, BATCH_SIZE

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    """
    a type used to store coordinate pairs
    """
    x: int
    y: str


async def chart_coordinates(values: dict[int, mpmath.mpf],
                            p_values: dict[int, mpmath.mpf],
                            q_values: dict[int, mpmath.mpf],
                            limit: mpmath.mpf,
                            iterations: int, websocket: WebSocket) -> tuple[
    list[Point2D], list[Point2D], list[Point2D], list[Point2D]]:
    """
    graph coords for the error of an expression: |expression - L|
    :param values: computed values for continued fraction, p_n/q_n
    :param p_values: computed values for continued fraction numerators, p_n
    :param q_values: computed values for continued fraction denominators, q_n
    :param limit: the computed approximate limit of the expression
    :param iterations: the number of values expected, n max
    :return: tuple of arrays of [x,y] pairs for graphing purposes
    """
    error_x_y_pairs = []
    log_error_x_y_pairs = []
    delta_x_y_pairs = []
    reduced_delta_x_y_pairs = []

    for n, value in values.items():

        if 1 <= n <= iterations and value is not None:
            # we take the difference between the actual value at n and the limit to see how far off we are at n
            error = mpmath.fabs(mpmath.fsub(value, limit))
            error_x_y_pairs.append(Point2D(x=n, y=str(error)))

            if mpmath.almosteq(value, limit):
                logger.debug(
                    f"Precision exhausted at n = {n}, the difference between value and limit is approximately zero")
                break

            if n <= DEBUG_LINES:
                logger.debug(f"Error at {n} | {value} - {limit} | = {error}")

            # compute precision coordinates
            if not mpmath.almosteq(error, mpmath.mpf(0)):
                # taking log 10 gives us the order of magnitude of the difference -  the number of zeros after the decimal
                # which is a gauge of the proximity of the value at n to the "limit"
                # since these are tiny decimal values the log is negative, so we take the absolute value
                error_log = mpmath.fabs(mpmath.log10(error))

                if not mpmath.isinf(error_log):
                    if n <= DEBUG_LINES:
                        logger.debug(f"log10 error at {n} | log10( | {value} - {limit} | ) | = {error_log}")
                    log_error_x_y_pairs.append(Point2D(x=n, y=str(error_log)))

            # prevent divide by zero exception
            if (q_values[n] is not None
                    and q_values[n] > 0
                    and str(q_values[n]) != '0.0'):

                # compute delta
                q_log = mpmath.log10(mpmath.fabs(q_values[n]))

                if not mpmath.almosteq(q_log, mpmath.mpf(0)):

                    delta_y_value = mpmath.fsub(-1, (mpmath.fdiv(error_log, q_log)))

                    if not mpmath.isinf(delta_y_value):
                        if n <= DEBUG_LINES:
                            logger.debug(
                                f"Delta at {n}: - 1 - log10( | {value} - {limit} | ) / log10( | {q_values[n]} | ) = {delta_y_value}")
                        delta_x_y_pairs.append(Point2D(x=n, y=str(delta_y_value)))

                # compute reduced delta
                gcd = sympy.gcd(sympy.Rational(str(p_values[n])), sympy.Rational(str(q_values[n])))

                if not mpmath.almosteq(gcd, mpmath.mpf(0)):

                    reduced_q = mpmath.fabs(mpmath.fdiv(q_values[n], gcd))

                    reduced_delta_y_value = mpmath.fsub(-1, error_log / reduced_q)

                    if not mpmath.isinf(reduced_delta_y_value):
                        if n <= DEBUG_LINES:
                            logger.debug(
                                f"Reduced delta at {n}: - 1 - (log10(|{value} - {limit}|) / log10(|{q_values[n]} / {gcd}|)) "
                                f"= {reduced_delta_y_value}")
                        reduced_delta_x_y_pairs.append(Point2D(x=n, y=str(reduced_delta_y_value)))

        # incremental response - remember that xy pairs start at n=1 but index 0
        if n % BATCH_SIZE == 0:
            # sending chunk
            await websocket.send_json({"error": json.dumps(log_error_x_y_pairs[n - BATCH_SIZE:n])})
            await websocket.send_json({"delta": json.dumps(delta_x_y_pairs[n - BATCH_SIZE:n])})
            await websocket.send_json({"reduced_delta": json.dumps(reduced_delta_x_y_pairs[n - BATCH_SIZE:n])})

    # final chunk
    await websocket.send_json({"error": json.dumps(log_error_x_y_pairs[n - n % BATCH_SIZE:])})
    await websocket.send_json({"delta": json.dumps(delta_x_y_pairs[n - n % BATCH_SIZE:])})
    await websocket.send_json({"reduced_delta": json.dumps(reduced_delta_x_y_pairs[n - n % BATCH_SIZE:])})
