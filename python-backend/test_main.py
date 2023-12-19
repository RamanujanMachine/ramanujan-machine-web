"""
Unit tests
"""
import pytest
import sympy
from sympy import sympify, simplify, SympifyError, Symbol, oo

import custom_exceptions
from main import convert
from math_utils import error, delta, log
from wolfram_client import WolframClient

TEST_INPUT_1 = "4^x"
CONVERSION_1 = "4**x"
TEST_INPUT_2 = "4x^2+3"
CONVERSION_2 = "4*x**2+3"
TEST_INPUT_3 = "4x^2+3x^5-1"
CONVERSION_3 = "4*x**2+3*x**5-1"
SYMPY_3 = "3*x**5+4*x**2-1"
TEST_INPUT_4 = "4x^2 + 3x^5 - 1"
CONVERSION_4 = "4*x**2 + 3*x**5 - 1"
SYMPY_4 = "3*x**5+4*x**2-1"
TEST_INPUT_5 = "2x^2"
TEST_INPUT_6 = "x"
SIMPLIFIED_5_6 = "2*x"
TEST_INPUT_7 = "6x^2 - 2 - 4x"
TEST_INPUT_8 = "x - 1"
SIMPLIFIED_7_8 = "6*x + 2"
SYMBOL = Symbol('x', real=True)
P = "4*x**2"
Q = "5*x**3-6*x**2+2"


def test_convert() -> None:
    assert convert("") == ""
    assert convert(TEST_INPUT_1) == CONVERSION_1
    assert convert(TEST_INPUT_2) == CONVERSION_2
    assert convert(TEST_INPUT_3) == CONVERSION_3
    assert convert(TEST_INPUT_4) == CONVERSION_4


def test_sympify() -> None:
    assert sympify(convert(TEST_INPUT_1))
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_2)
    assert sympify(convert(TEST_INPUT_2)).__str__().replace(' ', '') == convert(TEST_INPUT_2)
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_3)
    assert sympify(convert(TEST_INPUT_3)).__str__().replace(' ', '') == SYMPY_3
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_4)
    assert sympify(convert(TEST_INPUT_4)).__str__().replace(' ', '') == SYMPY_4


def test_simplify() -> None:
    assert simplify(sympify(convert(TEST_INPUT_1)))
    assert simplify(sympify(convert(TEST_INPUT_2)))
    assert simplify(sympify(convert(TEST_INPUT_3)))
    assert simplify(sympify(convert(TEST_INPUT_4)))
    assert simplify(sympify(convert(TEST_INPUT_5)) / sympify(convert(TEST_INPUT_6))).__str__() == SIMPLIFIED_5_6
    assert simplify(sympify(convert(TEST_INPUT_7)) / sympify(convert(TEST_INPUT_8))).__str__() == SIMPLIFIED_7_8


def test_api_failure() -> None:
    with pytest.raises(custom_exceptions.APIError):
        WolframClient.ask("")


def test_api_success() -> None:
    assert type(WolframClient.ask("time in Iceland")) is dict


def test_error() -> None:
    limit = sympy.limit(sympify(P) / sympify(Q), SYMBOL, oo)
    assert type(error(sympify(P) / sympify(Q), SYMBOL, limit, val=1)) in (
        sympy.core.numbers.ComplexInfinity, sympy.core.mul.Mul, sympy.core.add.Add)


def test_delta() -> None:
    limit = sympy.limit(sympify(P) / sympify(Q), SYMBOL, oo)
    assert type(
        delta(sympify(P) / sympify(Q), sympify(Q), SYMBOL, limit, val=1)) in (
               sympy.core.numbers.ComplexInfinity, sympy.core.mul.Mul, sympy.core.add.Add)


def test_log() -> None:
    assert type(log(sympify(P) / sympify(Q), SYMBOL, val=1)) in (
        sympy.core.numbers.ComplexInfinity, sympy.core.mul.Mul, sympy.core.add.Add)
