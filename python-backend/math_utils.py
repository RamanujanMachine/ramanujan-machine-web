"""Utility functions that perform mathematical operations with preset parameters"""
import logging
from typing import Callable

import mpmath
import sympy.core.numbers
from sympy import Symbol, sympify, limit_seq, simplify
from sympy.core.numbers import Number

import constants

logger = logging.getLogger('rm_web_app')


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
        logger.debug(limit_seq(expression / symbol ** power))
        while limit_seq(expression / symbol ** power) == sympy.core.numbers.Infinity:
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


def assess_convergence(series: str, symbol: Symbol) -> bool:
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
