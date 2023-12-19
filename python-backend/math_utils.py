"""Utility functions that perform mathematical operations with preset parameters"""
import sympy
from sympy import Symbol

import constants

PRECISION = constants.PRECISION


def error(expression: sympy.core, symbol: Symbol, limit: sympy.core.numbers, val: int) -> sympy.core.numbers:
    """
    error calculation: log(|expression - L|)
    :param expression: mathematical expression provided by user to evaluate
    :param symbol: the variable to substitute in the expression
    :param limit: the limit of the expression toward positive infinity
    :param val: the x value and the value to substitute in for the symbol in the expression
    :return: the error, i.e. y coordinate, at the val provided
    """
    return sympy.log(abs(expression.subs(symbol, val) - limit), 10).evalf(PRECISION)


def log(expression: sympy.core, symbol: Symbol, val: int) -> sympy.core.numbers:
    """
    log base 10 of expression at val
    :param expression: mathematical expression provided by user to evaluate
    :param symbol: the variable to substitute in the expression
    :param val: the x value and the value to substitute in for the symbol in the expression
    :return: the log base 10, i.e. y coordinate, at the val provided
    """
    return sympy.log(expression.subs(symbol, val), 10).evalf(PRECISION)


def delta(expression: sympy.core,
          denominator: sympy.core,
          symbol: Symbol,
          limit: sympy.core.numbers,
          val: int) -> sympy.core.numbers:
    """
    delta as defined by the expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    :param expression: mathematical expression provided by user to evaluate
    :param denominator: denominator portion of the mathematical expression provided by user to evaluate
    :param symbol: the variable to substitute in the expression
    :param limit: the limit of the expression toward positive infinity
    :param val: the x value and the value to substitute in for the symbol in the expression
    :return: the delta or y coordinate at the val provided
    """
    return error(expression, symbol, limit, val) / log(denominator, symbol, val) - 1
