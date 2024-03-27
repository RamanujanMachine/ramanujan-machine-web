""" Processing of the post body from the frontend """
import logging
import re
from typing import Callable

from mpmath import mpf
from pydantic import BaseModel
from sympy.core import sympify
from sympy.core.numbers import Number
from sympy.core.symbol import Symbol

import constants
from constants import PRECISION

logger = logging.getLogger('rm_web_app')


class Input(BaseModel):
    """Structure of user form data"""
    a: str
    b: str
    i: int
    symbol: str
    debug: bool = False


class Expression(BaseModel):
    """Structure of user form data"""
    expression: str


def parse(data: Input) -> tuple[Callable, Number, Callable, Number, Symbol]:
    """
    Process user inputs into math expressions
    :param data: User form inputs
    :return: tuple comprising sympified a_n, a_n_minus_1, b and the Symbol used
    """
    variable = Symbol(data.symbol, integer=True)

    # parse out any problem characters in the input string expressions for a and b
    a_formatted = reformat(data.a)
    b_formatted = reformat(data.b)

    # sympify input expressions
    a_symp = sympify(a_formatted, {data.symbol: variable}, rational=True) if (len(data.symbol) == 1) \
        else sympify(a_formatted, rational=True)
    b_symp = sympify(b_formatted, {data.symbol: variable}, rational=True) if (len(data.symbol) == 1) \
        else sympify(b_formatted, rational=True)

    # define functions for input expressions
    def a(x: Number):
        """
        Function representation of a
        """
        return mpf(a_symp.evalf(subs={variable: x}, n=PRECISION, strict=True, verbose=constants.VERBOSE_EVAL))

    def b(x: Number):
        """
        Function representation of b
        """
        return mpf(b_symp.evalf(subs={variable: x}, n=PRECISION, strict=True, verbose=constants.VERBOSE_EVAL))

    logger.debug(
        f"PARSED INPUTS symbol is [{variable}], a is [{a_symp}], b is [{b_symp}]")
    return a, a_symp, b, b_symp, variable


def reformat(polynomial: str) -> str:
    """
    Take an acceptable math polynomial entered by a user and convert to one that Python can parse
    :param polynomial: incoming polynomial entered by user in web frontend
    :return: python parse-able polynomial
    """
    expression = re.sub(r'([0-9]+)([a-zA-Z])', '\\1*\\2',
                        polynomial.replace('^', '**').replace(' ', '').replace(')(', ')*('))
    expression = re.sub(r'([0-9a-zA-Z])(\()', '\\1*\\2', expression)
    logger.debug(f"input: {polynomial} output: {expression}")
    return expression
