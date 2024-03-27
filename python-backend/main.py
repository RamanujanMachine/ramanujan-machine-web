"""Entrypoint for the application and REST API handlers"""
import json
import sys
import traceback

import mpmath
from LIReC.db.access import db
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy.core.numbers import Infinity

import constants
import logger
from graph_utils import (delta_coordinates, slope_of_error_coordinates, error_coordinates,
                         Point2D, reduced_delta_coordinates, error_log_coordinates)
from input import Input, Expression, parse
from math_utils import generalized_computed_values, simple_computed_values, laurent, assess_convergence
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
        iterations = data.i
        (a_func, a, b_func, b, symbol) = parse(data)

        if len(data.symbol) > 0:
            is_convergent = assess_convergence(laurent(a, b, symbol), symbol)
            # short circuit if the preliminary test fails
            if is_convergent is False:
                response = JSONResponse(content={"is_convergent": is_convergent}, status_code=200)
                return response

        # per the link below, "when bi = 1 (the partial numerator) for all i the expression is called a simple continued
        # fraction"
        # b here is the partial numerator (a and b are often used interchangeably which may lead to confusion when there
        # is no associated image of the continued fraction)
        # https://en.wikipedia.org/wiki/Continued_fraction#Basic_formula
        if data.b == "1":
            (values, num_values, denom_values) = simple_computed_values(a_func, iterations=iterations)
        else:
            # generalized continued fractions, where the partial numerator has its own formula and is not equal to 1
            # https://en.wikipedia.org/wiki/Generalized_continued_fraction
            (values, num_values, denom_values) = generalized_computed_values(a_func, b_func, iterations=iterations)

        limit = values[next(reversed(values))]
        logger.debug(f"last convergent / limit: {limit}")

        computed_values = db.identify(values=[str(limit)], wide_search=True)
        for m in computed_values:
            logger.debug(f"identify returned: {m}")

        error = error_coordinates(values, limit, iterations)
        error_log = error_log_coordinates(error, values, limit, iterations)
        body = {
            "limit": json.dumps("Infinity" if type(limit) is Infinity else str(limit)),
            "error": json.dumps(error),
            "delta": json.dumps(delta_coordinates(values, denom_values, limit, iterations)),
            "converges_to": json.dumps(str(computed_values[0] if len(computed_values) > 0 else None))
        }

        if data.debug:
            body["a"] = json.dumps(
                [Point2D(x=n, y=str(
                    a.evalf(subs={symbol: n},
                            n=constants.PRECISION,
                            strict=True,
                            verbose=constants.VERBOSE_EVAL))) for n in range(0, iterations)]),
            body["b"] = json.dumps(
                [Point2D(x=n, y=str(
                    b.evalf(subs={symbol: n},
                            n=constants.PRECISION,
                            strict=True,
                            verbose=constants.VERBOSE_EVAL))) for n in range(0, iterations)]),
            body["p"] = json.dumps([Point2D(x=i, y=str(p)) for i, p in enumerate(num_values)]),
            body["q"] = json.dumps([Point2D(x=i, y=str(q)) for i, q in enumerate(denom_values)]),
            body["p_over_q"] = json.dumps([Point2D(x=i, y=str(pq)) for i, pq in enumerate(values)]),
            body["error_log"] = json.dumps(error_log),
            body["error_slope"] = json.dumps(slope_of_error_coordinates(error, iterations)),
            body["reduced_delta"] = json.dumps(
                reduced_delta_coordinates(values, num_values, denom_values, limit, iterations))

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
