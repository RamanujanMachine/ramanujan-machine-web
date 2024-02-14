"""
Unit tests
"""
import mpmath
import pytest
from sympy import sympify, simplify, SympifyError, Symbol

import custom_exceptions
from input import Input
from main import convert, parse
from math_utils import generalized_computed_values, simple_computed_values, cpython_gcd
from wolfram_client import WolframClient

TEST_INPUT_1 = "4^x"
CONVERSION_1 = "4**x"
TEST_INPUT_2 = "4x^2+3"
CONVERSION_2 = "4*x**2+3"
TEST_INPUT_3 = "4x^2+3x^5-1"
CONVERSION_3 = "4*x**2+3*x**5-1"
SYMPY_3 = "3*x**5+4*x**2-1"
TEST_INPUT_4 = "4x^2 + 3x^5 - 1"
CONVERSION_4 = "4*x**2+3*x**5-1"
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
TEST_INPUT_9 = "(1 + 2 n) (5 + 17 n (1 + n))"
CONVERSION_10 = "(1+2*n)*(5+17*n*(1+n))"


def test_convert() -> None:
    assert convert("") == ""
    assert convert(TEST_INPUT_1) == CONVERSION_1
    assert convert(TEST_INPUT_2) == CONVERSION_2
    assert convert(TEST_INPUT_3) == CONVERSION_3
    assert convert(TEST_INPUT_4) == CONVERSION_4
    assert convert(TEST_INPUT_9) == CONVERSION_10


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


def test_generalized_compute_values() -> None:
    # start at n = 1
    values = [mpmath.mpf(584) / mpmath.mpf(117), mpmath.mpf(312120) / mpmath.mpf(62531),
              mpmath.mpf(456205824) / mpmath.mpf(91397560),
              mpmath.mpf(1415240640000) / mpmath.mpf(283533296824),
              mpmath.mpf(8010210009600000) / mpmath.mpf(1604788039632960)]
    data = Input(a="(1 + 2 n) (5 + 17 n (1 + n))", b="-n^6", symbol="n", i=100)
    (expression, a, b, symbol) = parse(data)
    (convergents, numerators, denominators) = generalized_computed_values(a=a, b=b, symbol=symbol, iterations=10)
    assert (denominators[1] == mpmath.mpf(117))
    assert (denominators[2] == mpmath.mpf(62531))
    assert (denominators[3] == mpmath.mpf(91397560))
    assert (denominators[4] == mpmath.mpf(283533296824))
    assert (denominators[5] == mpmath.mpf(1604788039632960))
    assert (convergents[1] == values[0])
    assert (convergents[2] == values[1])
    assert (convergents[3] == values[2])
    assert (convergents[4] == values[3])
    assert (convergents[5] == values[4])


def test_simple_compute_values() -> None:
    # start at n = 1
    values = [1, mpmath.fdiv(2, 3), mpmath.fdiv(7, 10), mpmath.fdiv(30, 43), mpmath.fdiv(157, 225),
              mpmath.fdiv(972, 1393),
              mpmath.fdiv(6961, 9976), mpmath.fdiv(56660, 81201)]
    data = Input(a="n", b="1", symbol="n", i=100)
    (expression, a, b, symbol) = parse(data)
    (convergents, numerators, denominators) = simple_computed_values(a=a, symbol=symbol, iterations=10)
    assert (denominators[2] == mpmath.mpf(3))
    assert (denominators[3] == mpmath.mpf(10))
    assert (denominators[4] == mpmath.mpf(43))
    assert (denominators[5] == mpmath.mpf(225))
    assert (denominators[6] == mpmath.mpf(1393))
    assert (denominators[7] == mpmath.mpf(9976))
    assert (convergents[2] == values[1])
    assert (convergents[3] == values[2])
    assert (convergents[4] == values[3])
    assert (convergents[5] == values[4])
    assert (convergents[6] == values[5])
    assert (convergents[7] == values[6])


def test_cpython_gcd() -> None:
    assert (cpython_gcd(16, 64) == 16)
    assert (cpython_gcd(81, 99) == 9)
