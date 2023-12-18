import sympy
from sympy import Symbol

import constants

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)
PRECISION = constants.PRECISION
X_VALUES = range(0, 1000, 25)


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
    return sympy.log(expression.subs(symbol, val)).evalf(PRECISION)


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


def error_coordinates(expression: sympy.core, symbol: Symbol, limit: sympy.core.numbers) -> [[int, float]]:
    """
    graph coords for the error of an expression log(|expression - L|) in terms of symbol
    :param expression: univariate mathematical expression comprising a ratio of two polynomials
    :param symbol: the variable used in expression
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    return [[val, float(error(expression, symbol, limit, val))] for val in X_VALUES if
            type(error(expression, symbol, limit, val)) in GRAPHABLE_TYPES]


def delta_coordinates(expression: sympy.core,
                      denominator: sympy.core,
                      symbol: Symbol,
                      limit: sympy.core.numbers) -> [[int, float]]:
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1 in terms of symbol
    :param expression: univariate mathematical expression comprising a ratio of two polynomials
    :param denominator: univariate polynomial
    :param symbol: the variable used in expression
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    return [[val, -1 * float(delta(expression, denominator, symbol, limit, val))] for val in X_VALUES if
            type(-1 * float(delta(expression, denominator, symbol, limit, val))) in GRAPHABLE_TYPES]
