"""Utility functions that perform mathematical operations with preset parameters"""
import logging

import mpmath
import sympy
from sympy import Symbol

import constants

PRECISION = constants.PRECISION

logger = logging.getLogger('rm_web_app')


def delta(limit: mpmath.mpf, val: mpmath.mpf, denom_val: mpmath.mpf) -> mpmath.mpf:
    """
    delta as defined by the expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param limit: the limit of the expression toward positive infinity
    :param val: the x value and the value to substitute in for the symbol in the expression
    :param denom_val: just the denominator of the compute value val
    :return: the delta or y coordinate at the val provided
    """
    return mpmath.mpf(-1) * mpmath.log10(abs(val - limit)) / mpmath.log10(denom_val) - mpmath.mpf(1)


def generalized_computed_values(a: sympy.core, b: sympy.core, symbol: Symbol, iterations: int = 500) -> (
list[mpmath.mpf], list[mpmath.mpf]):
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
    for i in range(0, len(a_n)):
        logger.debug(f"a value at {i}: {a_n[i]}, b value at {i}: {b_n[i]}")
    # these arrays start at n = -1, so we prepad the convergent list with values we will slice off
    numerators = [mpmath.mpf(1), a_n[0]]
    denominators = [0, mpmath.mpf(1)]
    convergents = [None, numerators[1] / denominators[1]]
    # note n >= 1 per the article above
    for i in range(1, len(b_n)):
        numerators.append(a_n[i] * numerators[i] + b_n[i] * numerators[i - 1])
        denominators.append(a_n[i] * denominators[i] + b_n[i] * denominators[i - 1])

        if denominators[i] != 0:
            convergents.append(numerators[-1] / denominators[-1])
            if i < 20:
                logger.debug(
                    f"generalized_computed_values n: {i} denom: {denominators[-1]} num: {numerators[-1]} num/denom: {convergents[-1]}")
        else:
            convergents.append(None)
            logger.warning(
                f"generalized_computed_values n: {i} num: {numerators[-1]} denom: {denominators[-1]} ratio: Undefined")

    # return from n = 0 on
    return convergents[1:], denominators[1:]


def simple_computed_values(a: sympy.core, symbol: Symbol, iterations: int = 500) -> (
list[mpmath.mpf], list[mpmath.mpf]):
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
    for i in range(0, len(a_n)):
        logger.debug(f"a value at {i}: {a_n[i]}")
    # these arrays start at n = -2, so we prepad the convergent list with values we will slice off
    numerators = [mpmath.mpf(0), mpmath.mpf(1)]
    denominators = [mpmath.mpf(1), mpmath.mpf(0)]
    convergents = [None, None]
    for i in range(0, len(a_n)):
        num = a_n[i] * numerators[i - 1 + 2] + numerators[i - 2 + 2]
        numerators.append(num)
        denom = a_n[i] * denominators[i - 1 + 2] + denominators[i - 2 + 2]
        denominators.append(denom)

        if denominators[i] != 0:
            convergents.append(numerators[-1] / denominators[-1])
            if i < 20:
                logger.debug(
                    f"simple computed values n: {i} num: {numerators[-1]} denom: {denominators[-1]} ratio: {convergents[-1]}")
        else:
            convergents.append(None)
            logger.warning(
                f"simple computed values n: {i} num: {numerators[-1]} denom: {denominators[-1]} ratio: Undefined")

    # return from n = 0 on
    return convergents[2:], denominators[2:]
