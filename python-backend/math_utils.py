"""Utility functions that perform mathematical operations with preset parameters"""
import logging
from typing import Callable

import mpmath
from sympy import Symbol, sympify, limit_seq, simplify
from sympy.core.numbers import Number

import constants

PRECISION = constants.PRECISION

logger = logging.getLogger('rm_web_app')


def generalized_computed_values(a: Callable[[Number], mpmath.mpf],
                                b: Callable[[Number], mpmath.mpf],
                                iterations: int = 500) -> tuple[
    dict[int, mpmath.mpf], dict[int, mpmath.mpf], dict[int, mpmath.mpf]]:
    """
    Compute values at each step iteratively for a polynomial continued fraction
    Parameters
    ----------
    :param iterations: computation depth
    :param b: partial numerator provided by user
    :param a: partial denominator provided by user

    Returns
    -------
    list of values computed at each step from n = 1 to the number of iterations provided
    """
    # for complex a and b (note that the article reverses a and b)
    # see https://en.wikipedia.org/wiki/Generalized_continued_fraction#

    # doubling the iteration count facilitates approximation of a limit
    a_n = [a(n) for n in range(0, 2 * iterations)]
    b_n = [b(n) for n in range(0, 2 * iterations)]
    for i in range(0, min(constants.DEBUG_LINES, len(a_n))):
        logger.debug(f"a value at {i}: {a_n[i]}, b value at {i}: {b_n[i]}")

    # these arrays start at n = -1
    numerators = dict({-1: mpmath.mpf(1), 0: a_n[0]})
    denominators = dict({-1: mpmath.mpf(0), 0: mpmath.mpf(1)})
    convergents = dict({-1: None, 0: numerators[0] / denominators[0]})

    # note n >= 1 per the article above and a_n and b_n are switched since we consistently use a_n as the coefficient
    # and b_n as the numerator
    for n in range(1, 2 * iterations):
        numerators[n] = (a_n[n] * numerators[n - 1] + b_n[n] * numerators[n - 2])
        denominators[n] = (a_n[n] * denominators[n - 1] + b_n[n] * denominators[n - 2])

        try:
            convergents[n] = (numerators[n] / denominators[n])
            if n <= constants.DEBUG_LINES:
                logger.debug(
                    f"generalized_computed_values n: {n} denom: {denominators[n]} num: {numerators[n]} "
                    f"num/denom: {convergents[n]}")
        except ZeroDivisionError:
            logger.warning(
                f"generalized_computed_values n: {n} num: {numerators[n]} denom: {denominators[n]} ratio: Undefined")
            break

    return convergents, numerators, denominators


def simple_computed_values(a: Callable[[Number], mpmath.mpf], iterations: int = 500) -> tuple[
    dict[int, mpmath.mpf], dict[int, mpmath.mpf], dict[int, mpmath.mpf]]:
    """
    Compute values at each step iteratively for a polynomial continued fraction. Series documentation can be found here:
    https://en.wikipedia.org/wiki/Continued_fraction#Infinite_continued_fractions_and_convergents.
    Parameters
    ----------
    :param iterations: computation depth
    :param a: partial numerator provided by user

    Returns
    -------
    list of values computed at each step from n = 1 on to some n max
    """
    a_n = [a(n) for n in range(0, 2 * iterations)]
    for i in range(0, min(constants.DEBUG_LINES, len(a_n))):
        logger.debug(f"a value at {i}: {a_n[i]}")

    # these arrays start at n = -2
    numerators = dict({-2: mpmath.mpf(0), -1: mpmath.mpf(1)})
    denominators = dict({-2: mpmath.mpf(1), -1: mpmath.mpf(0)})
    convergents = dict({-2: None, -1: None})

    for n in range(0, 2 * iterations):
        numerators[n] = a_n[n] * numerators[n - 1] + numerators[n - 2]
        denominators[n] = a_n[n] * denominators[n - 1] + denominators[n - 2]

        try:
            convergents[n] = (numerators[n] / denominators[n])
            if n < constants.DEBUG_LINES:
                logger.debug(
                    f"simple computed values n: {n} num: {numerators[n]} denom: {denominators[n]} "
                    f"ratio: {convergents[n]}")
        except ZeroDivisionError:
            logger.warning(
                f"simple computed values n: {n} num: {numerators[n]} denom: {denominators[n]} ratio: Undefined")
            break

    return convergents, numerators, denominators


def laurent(a: Number, b: Number, symbol: Symbol = None, term_count=2) -> str:
    """
    compute laurent series in symbol up to term_count terms
    """
    result = 0
    power = 0

    if symbol is None:
        expression = 1 + 4 * b / (a * a)
        while limit_seq(expression).is_infinite:
            power += 1

        def limit_lambda() -> Number:
            """
            compute limit of series where the expression is a constant
            """
            return limit_seq(expression)
    else:
        expression = 1 + 4 * b / (a * a.subs(symbol, symbol - 1))
        while limit_seq(expression / symbol ** power).is_infinite:
            power += 1

        def limit_lambda() -> Number:
            """
            compute limit of series where the expression is variable
            """
            return limit_seq(expression / symbol ** power) * symbol ** power

    logger.debug(f"initial expression: {expression}")
    logger.debug(f"power at which limit is no longer infinite: {power}")

    while term_count:
        limit = limit_lambda()
        logger.debug(f"loop limit: {limit}")
        if limit:
            result += limit
            logger.debug(f"loop iteration {term_count} result: {result}")
            expression = simplify(expression - limit)
            logger.debug(f"loop iteration {term_count} expression: {expression}")
            term_count -= 1
        if not expression:
            logger.debug(f"loop terminating result {result}")
            return str(result)
        power -= 1

    power += 1

    order = f'1/n**{-power}' if power < -1 else str(symbol ** power)
    return f'{result} + o({order})'


def assess_convergence(series: str, symbol: Symbol):
    """
    Takes the result of the laurent series function and analyzes whether it suggests convergence
    """
    # manually separating off first term because the o(...) bit confuses normal poly parsing
    logger.debug(f"symbol is {type(symbol)}")
    if symbol is not None:
        first_term = sympify(series.split(' ')[0], {str(symbol): symbol},
                             rational=True).as_ordered_terms()
        first_exponent = first_term[0].as_powers_dict()[symbol]
        first_coeff_list = first_term[0].as_coefficients_dict(symbol)
        first_coeff = first_coeff_list[list(first_coeff_list.keys())[0]]

        logger.debug(
            f"in the series {series}, the first term is {first_term}, "
            f"its coefficient is {first_coeff} and its power is {first_exponent}")
        if first_exponent <= -1 or (first_exponent <= 2 and first_coeff > 0):
            return True
        else:
            return False
