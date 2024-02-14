"""Utility functions that perform mathematical operations with preset parameters"""
import logging
from collections import OrderedDict

import mpmath
import sympy
from sympy import Symbol

import constants

PRECISION = constants.PRECISION

logger = logging.getLogger('rm_web_app')


def cpython_gcd(a: mpmath.mpf, b: mpmath.mpf) -> mpmath.mpf:
    """
    Calculate the Greatest Common Divisor (GCD) of a and b
    """
    while b:
        a, b = b, a % b
    return a


def generalized_computed_values(a: sympy.core, b: sympy.core, symbol: Symbol, iterations: int = 500) -> (
        OrderedDict[int, mpmath.mpf], OrderedDict[int, mpmath.mpf], OrderedDict[int, mpmath.mpf]):
    """
    Compute values at each step iteratively for a polynomial continued fraction
    Parameters
    ----------
    :param iterations: computation depth
    :param b: partial numerator provided by user
    :param a: partial denominator provided by user
    :param symbol: the variable used by the user in numerator and denominator

    Returns
    -------
    list of values computed at each step from n = 1 to the number of iterations provided
    """
    # for complex a and b (note that the article reverses a and b)
    # see https://en.wikipedia.org/wiki/Generalized_continued_fraction#
    a_n = [mpmath.mpf(a.subs(symbol, n).evalf(PRECISION)) for n in range(0, iterations)]
    b_n = [mpmath.mpf(b.subs(symbol, n).evalf(PRECISION)) for n in range(0, iterations)]
    for i in range(0, min(constants.DEBUG_LINES, len(a_n))):
        logger.debug(f"a value at {i}: {a_n[i]}, b value at {i}: {b_n[i]}")

    # these arrays start at n = -1
    numerators = OrderedDict({-1: mpmath.mpf(1), 0: a_n[0]})
    denominators = OrderedDict({-1: 0, 0: mpmath.mpf(1)})
    convergents = OrderedDict({-1: None, 0: numerators[0] / denominators[0]})

    # note n >= 1 per the article above and a_n and b_n are switched since we consistently use a_n as the coefficient
    # and b_n as the numerator
    for n in range(1, iterations):
        numerators[n] = (a_n[n] * numerators[n - 1] + b_n[n] * numerators[n - 2])
        denominators[n] = (a_n[n] * denominators[n - 1] + b_n[n] * denominators[n - 2])

        if denominators[n] != 0:
            convergents[n] = (numerators[n] / denominators[n])
            if n <= constants.DEBUG_LINES:
                logger.debug(
                    f"generalized_computed_values n: {n} denom: {denominators[n]} num: {numerators[n]} "
                    f"num/denom: {convergents[n]}")
        else:
            logger.warning(
                f"generalized_computed_values n: {n} num: {numerators[n]} denom: {denominators[n]} ratio: Undefined")

    return convergents, numerators, denominators


def simple_computed_values(a: sympy.core, symbol: Symbol, iterations: int = 500) -> (
        OrderedDict[int, mpmath.mpf], OrderedDict[int, mpmath.mpf], OrderedDict[int, mpmath.mpf]):
    """
    Compute values at each step iteratively for a polynomial continued fraction. Series documentation can be found here:
    https://en.wikipedia.org/wiki/Continued_fraction#Infinite_continued_fractions_and_convergents.
    Parameters
    ----------
    :param iterations: computation depth
    :param a: partial numerator provided by user
    :param symbol: the variable used by the user in numerator and denominator

    Returns
    -------
    list of values computed at each step from n = 1 on to some n max
    """
    a_n = [mpmath.mpf(a.subs(symbol, n).evalf(PRECISION)) for n in range(0, iterations)]
    for i in range(0, min(constants.DEBUG_LINES, len(a_n))):
        logger.debug(f"a value at {i}: {a_n[i]}")

    # these arrays start at n = -2
    numerators = OrderedDict({-2: mpmath.mpf(0), -1: mpmath.mpf(1)})
    denominators = OrderedDict({-2: mpmath.mpf(1), -1: mpmath.mpf(0)})
    convergents = OrderedDict({-2: None, -1: None})

    for n in range(0, iterations):
        numerators[n] = a_n[n] * numerators[n - 1] + numerators[n - 2]
        denominators[n] = a_n[n] * denominators[n - 1] + denominators[n - 2]

        if denominators[n] != 0:
            convergents[n] = (numerators[n] / denominators[n])
            if n < constants.DEBUG_LINES:
                logger.debug(
                    f"simple computed values n: {n} num: {numerators[n]} denom: {denominators[n]} "
                    f"ratio: {convergents[n]}")
        else:
            logger.warning(
                f"simple computed values n: {n} num: {numerators[n]} denom: {denominators[n]} ratio: Undefined")

    return convergents, numerators, denominators
