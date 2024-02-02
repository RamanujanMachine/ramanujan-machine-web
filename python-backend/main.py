"""Entrypoint for the application and REST API handlers"""
import json
import sys
import traceback

import mpmath
import ramanujan
import sympy
from LIReC.db.access import db
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy import sympify, Symbol
from sympy.core.numbers import Infinity

import constants
import logger
from graph_utils import delta_coordinates, error_coordinates, slope_of_error_coordinates
from input import Input, convert, Expression
from math_utils import generalized_computed_values, simple_computed_values
from wolfram_client import WolframClient

sys.set_int_max_str_digits(0)

app = FastAPI()

logger = logger.config(True)

mpmath.mp.dps = constants.PRECISION

# allow origin to be all possible combinations for protocol, host and port
origins = [[f"{host}",
            f"{host}:{port}",
            f"http://{host}",
            f"http://{host}:{port}"]
           for host in constants.HOSTS for port in constants.PORTS]
origins = [item for sublist in origins for item in sublist]

# Only allow traffic from localhost and restrict methods to those we intend to use
app.add_middleware(CORSMiddleware,
                   allow_credentials=False,  # must be true for cookies
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_headers=["*"])


def parse(data: Input) -> tuple[sympy.core, sympy.core, sympy.core, Symbol]:
    """
    Process user inputs into math expressions
    :param data: User form inputs
    :return: tuple including p/q, simplified q and the symbol/variable used in these expressions
    """
    x = Symbol(data.symbol, real=True)
    a = sympify(convert(data.a), {data.symbol: x})
    b = sympify(convert(data.b), {data.symbol: x})
    expression = a / b
    return expression, a, b, x


@app.post("/analyze")
async def analyze(request: Request):
    """
    Take user form inputs and parse them into mathematical expressions, then assess them in various ways and return
    chart coordinates to be rendered by the frontend
    :param request: HTTP request
    :return: HTTP response indicating success of parsing inputs with a 200 or a 500 to indicate failure parsing inputs
    """
    # parse posted body as Input

    try:
        data = Input(**(await request.json()))
        (expression, a, b, symbol) = parse(data)
        pcf = ramanujan.pcf.PCF(str(a), str(b))
        limit = mpmath.mpf(pcf.limit(depth=data.i))
        logger.debug(f"PCF limit() returned: {limit}")
        computed_values = db.identify(values=[limit], wide_search=True)
        for m in computed_values:
            logger.debug(f"identify returned: {m}")
        # per the link below, "when bi = 1 (the partial numerator) for all i the expression is called a simple continued
        # fraction"
        # b here is the partial numerator (a and b are often used interchangeably which may lead to confusion when there
        # is no associated image of the fraction)
        # https://en.wikipedia.org/wiki/Continued_fraction#Basic_formula
        if data.b == "1":
            (values, denom_values) = simple_computed_values(a, symbol)
        else:
            # generalized continued fractions, where the partial numerator has its own formula and is not equal to 1
            # https://en.wikipedia.org/wiki/Generalized_continued_fraction
            (values, denom_values) = generalized_computed_values(a, b, symbol)
        body = {
            "expression": json.dumps(str(expression)),
            "limit": json.dumps("Infinity" if type(limit) is Infinity else str(limit)),
            "error": json.dumps(error_coordinates(values, limit)),
            "error_deriv": json.dumps(slope_of_error_coordinates(values, limit)),
            "delta": json.dumps(delta_coordinates(values, denom_values, limit)),
            "converges_to": json.dumps(str(computed_values[0] if len(computed_values) > 0 else None))
        }
        logger.debug(f"Response: {body}")
        response = JSONResponse(content=body)
        return response

    except Exception as e:
        logger.warning(traceback.format_exc())
        response = JSONResponse(status_code=500, content={"error": "Failed to generate results"})
        return response


@app.post("/verify")
async def analyze(request: Request):
    """
    Take sanitized user expression and see what Wolfram Alpha has to say about it, returning the results to the frontend
    :param request: HTTP request
    :return: HTTP response indicating success of parsing inputs with a 200 or a 500 to indicate failure parsing inputs
    """
    # parse posted body as Expression

    try:
        expression = Expression(**(await request.json()))
        logger.debug(f"Sending to Wolfram API: {expression}")
        body = {
            "wolfram_says": WolframClient.closed_form(expression.expression)
        }

        response = JSONResponse(content=body)
        return response

    except Exception as e:
        logger.warning(e)
        response = JSONResponse(status_code=500, content={"error": "Failed to parse inputs"})
        return response
