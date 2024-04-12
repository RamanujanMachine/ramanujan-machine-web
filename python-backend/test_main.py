"""
Unit tests
"""
import mpmath
import pytest
from pytest_check import check
from sympy import sympify, simplify, SympifyError, Symbol

import custom_exceptions
from input import Input, parse, reformat
from math_utils import generalized_computed_values, simple_computed_values, laurent, assess_convergence
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
SYMBOL = Symbol('x', Integer=True)
P = "4*x**2"
Q = "5*x**3-6*x**2+2"
TEST_INPUT_9 = "(1 + 2 n) (5 + 17 n (1 + n))"
CONVERSION_10 = "(1+2*n)*(5+17*n*(1+n))"


def test_format() -> None:
    assert reformat("") == ""
    assert reformat(TEST_INPUT_1) == CONVERSION_1
    assert reformat(TEST_INPUT_2) == CONVERSION_2
    assert reformat(TEST_INPUT_3) == CONVERSION_3
    assert reformat(TEST_INPUT_4) == CONVERSION_4
    assert reformat(TEST_INPUT_9) == CONVERSION_10


def test_reformat_sympify() -> None:
    assert sympify(reformat(TEST_INPUT_1))
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_2)
    assert sympify(reformat(TEST_INPUT_2)).__str__().replace(' ', '') == reformat(TEST_INPUT_2)
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_3)
    assert sympify(reformat(TEST_INPUT_3)).__str__().replace(' ', '') == SYMPY_3
    with pytest.raises(SympifyError):
        sympify(TEST_INPUT_4)
    assert sympify(reformat(TEST_INPUT_4)).__str__().replace(' ', '') == SYMPY_4


def test_reformat_simplify() -> None:
    assert simplify(sympify(reformat
                            (TEST_INPUT_1)))
    assert simplify(sympify(reformat
                            (TEST_INPUT_2)))
    assert simplify(sympify(reformat
                            (TEST_INPUT_3)))
    assert simplify(sympify(reformat
                            (TEST_INPUT_4)))
    assert simplify(sympify(reformat
                            (TEST_INPUT_5)) / sympify(reformat
                                                      (TEST_INPUT_6))).__str__() == SIMPLIFIED_5_6
    assert simplify(sympify(reformat
                            (TEST_INPUT_7)) / sympify(reformat
                                                      (TEST_INPUT_8))).__str__() == SIMPLIFIED_7_8


def test_api_failure() -> None:
    with pytest.raises(custom_exceptions.APIError):
        WolframClient.ask("")


def test_api_success() -> None:
    assert type(WolframClient.ask("time in Iceland")) is dict


def test_generalized_compute_values() -> None:
    # start at n = 1 keeping in mind that the actual series starts at n=-1
    values = [mpmath.mpf(584) / mpmath.mpf(117), mpmath.mpf(312120) / mpmath.mpf(62531),
              mpmath.mpf(456205824) / mpmath.mpf(91397560),
              mpmath.mpf(1415240640000) / mpmath.mpf(283533296824),
              mpmath.mpf(8010210009600000) / mpmath.mpf(1604788039632960)]
    data = Input(a="(1 + 2 n) (5 + 17 n (1 + n))", b="-n^6", symbol="n", i=100)
    (a, _, b, _, symbol, _) = parse(data)
    (convergents, numerators, denominators) = generalized_computed_values(a=a, b=b, iterations=10)
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


@check.check_func
def test_generalized_compute_values_with_simple_input() -> None:
    # start at n = 1 keeping in mind that the actual series starts at n=-1
    values = [1, mpmath.fdiv(2, 3), mpmath.fdiv(7, 10), mpmath.fdiv(30, 43), mpmath.fdiv(157, 225),
              mpmath.fdiv(972, 1393),
              mpmath.fdiv(6961, 9976), mpmath.fdiv(56660, 81201)]
    data = Input(a="n", b="1", symbol="n", i=100)
    (a, _, b, _, symbol, _) = parse(data)
    (convergents, numerators, denominators) = generalized_computed_values(a=a, b=b, iterations=10)
    assert (numerators[2] == mpmath.mpf(2))
    assert (numerators[3] == mpmath.mpf(7))
    assert (numerators[4] == mpmath.mpf(30))
    assert (numerators[5] == mpmath.mpf(157))
    assert (numerators[6] == mpmath.mpf(972))
    assert (numerators[7] == mpmath.mpf(6961))
    assert (numerators[8] == mpmath.mpf(56660))
    assert (denominators[2] == mpmath.mpf(3))
    assert (denominators[3] == mpmath.mpf(10))
    assert (denominators[4] == mpmath.mpf(43))
    assert (denominators[5] == mpmath.mpf(225))
    assert (denominators[6] == mpmath.mpf(1393))
    assert (denominators[7] == mpmath.mpf(9976))
    assert (denominators[8] == mpmath.mpf(81201))
    assert (convergents[2] == values[1])
    assert (convergents[3] == values[2])
    assert (convergents[4] == values[3])
    assert (convergents[5] == values[4])
    assert (convergents[6] == values[5])
    assert (convergents[7] == values[6])
    assert (convergents[8] == values[7])


def test_simple_compute_values() -> None:
    # start at n = 1 keeping in mind that the actual series starts at n=-2
    values = [1, mpmath.fdiv(2, 3), mpmath.fdiv(7, 10), mpmath.fdiv(30, 43), mpmath.fdiv(157, 225),
              mpmath.fdiv(972, 1393),
              mpmath.fdiv(6961, 9976), mpmath.fdiv(56660, 81201)]
    data = Input(a="n", b="1", symbol="n", i=100, precision=30)
    (a, _, b, _, symbol, _) = parse(data)
    (convergents, numerators, denominators) = simple_computed_values(a=a, iterations=10)
    assert (numerators[2] == mpmath.mpf(2))
    assert (numerators[3] == mpmath.mpf(7))
    assert (numerators[4] == mpmath.mpf(30))
    assert (numerators[5] == mpmath.mpf(157))
    assert (numerators[6] == mpmath.mpf(972))
    assert (numerators[7] == mpmath.mpf(6961))
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


@check.check_func
def laurent_wrapper(a: str, b: str, output: str) -> None:
    v = Symbol('n', integer=True)
    assert (laurent(sympify(a, {'n': v}, rational=True), sympify(b, {'n': v}, rational=True), v) == output)


def test_laurent_cases() -> None:
    laurent_wrapper('2', 'n', 'n + 1')
    laurent_wrapper('2*n + 1', '-n**2', '-1/(4*n**2) - 1/(16*n**4) + o(1/n**4)')
    laurent_wrapper('2*n + 5', '-n', '1 - 1/n + o(1/n)')
    laurent_wrapper('4*n + 2', '-n**2', '3/4 - 1/(16*n**2) + o(1/n**2)')
    laurent_wrapper('1', '1', '5')
    laurent_wrapper('2', '-1', '0')
    laurent_wrapper('1', '-(n**2)', '1 - 4*n**2')
    laurent_wrapper('1', 'n**3', '4*n**3 + 1')


@check.check_func
def test_convergence_test() -> None:
    v = Symbol('n', integer=True)
    assert assess_convergence('-1/(4*n**2) - 1/(16*n**4) + o(1/n**4)', v) is True
    assert assess_convergence('1 - 1/n + o(1/n)', v) is True
    assert assess_convergence('3/4 - 1/(16*n**2) + o(1/n**2)', v) is True
    assert assess_convergence('5', v) is True
    assert assess_convergence('4*n**3 + 1', v) is False
