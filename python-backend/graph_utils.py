"""Utility functions that generate graphable coordinate pairs for the frontend"""
import sympy
from sympy import Symbol

import math_utils

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)
X_VALUES = range(0, 1000, 25)


def error_coordinates(expression: sympy.core, symbol: Symbol, limit: sympy.core.numbers) -> [[int, float]]:
    """
    graph coords for the error of an expression log(|expression - L|) in terms of symbol
    :param expression: univariate mathematical expression comprising a ratio of two polynomials
    :param symbol: the variable used in expression
    :param limit: the computed limit of the expression as it goes to infinity
    :return: array of [x,y] pairs for graphing purposes
    """
    y_values = [math_utils.error(expression, symbol, limit, val) for val in X_VALUES]
    return [[x, float(y)] for x, y in zip(X_VALUES, y_values) if type(y) in GRAPHABLE_TYPES]


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
    y_values = [-1 * math_utils.delta(expression, denominator, symbol, limit, val) for val in X_VALUES]
    return [[x, float(y)] for x, y in zip(X_VALUES, y_values) if type(y) in GRAPHABLE_TYPES]
