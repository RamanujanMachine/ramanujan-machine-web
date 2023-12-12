import sympy
from sympy import Symbol

import constants

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)
PRECISION = constants.PRECISION
X_VALUES = range(0, 1000, 25)


def error_coordinates(expression: sympy.core, symbol: Symbol, limit: sympy.core.numbers):
    """
    graph coords for the error of an expression log(|expression - L|) in terms of symbol
    :param expression: univariate mathematical expression comprising a ratio of two polynomials
    :param symbol: the variable used in expression
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    return [[val, float(sympy.log(abs(expression.subs(symbol, val) - limit)).evalf(PRECISION))] for val in X_VALUES if
            type(sympy.log(abs(expression.subs(symbol, val) - limit)).evalf(PRECISION)) in GRAPHABLE_TYPES]


def delta_coordinates(expression: sympy.core, denominator: sympy.core, symbol: Symbol, limit: sympy.core.numbers):
    """
    graph coords for the error delta for an expression -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1 in terms of symbol
    :param expression: univariate mathematical expression comprising a ratio of two polynomials
    :param denominator: univariate polynomial
    :param symbol: the variable used in expression
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    # graph coords of error delta: -1 * (log(|Pn/Qn - L|) / log(Qn)) - 1
    return [[val, float(-1 * ((sympy.log(abs(expression.subs(symbol, val) - limit)).evalf(PRECISION)) / (
        sympy.log(denominator.subs(symbol, val)).evalf(PRECISION))) - 1)] for val in X_VALUES if
            type(-1 * ((sympy.log(abs(expression.subs(symbol, val) - limit)).evalf(PRECISION)) / (
                sympy.log(denominator.subs(symbol, val)).evalf(PRECISION))) - 1) in GRAPHABLE_TYPES]
