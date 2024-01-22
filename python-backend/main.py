"""Entrypoint for the application and REST API handlers"""
import json
import traceback

import LIReC.db.access
import mpmath
import ramanujan
import sympy
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy import simplify, sympify, Symbol
from sympy.core.numbers import Infinity

import constants
import logger
from graph_utils import error_coordinates, delta_coordinates
from input import Input, convert, Expression
from wolfram_client import WolframClient

app = FastAPI()

logger = logger.config(True)

mpmath.mp.dps = constants.PRECISION

origins = ([item for sublist in
            [[f"localhost:{port}", f"http://localhost:{port}", f"127.0.0.1:{port}"] for port in constants.PORTS] for
            item
            in sublist])
origins.append("http://localhost")
origins.append("http://localhost/")
origins.append("http://174.129.252.235")
origins.append("http://174.129.252.235/")

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
    p = sympify(convert(data.p), {data.symbol: x})
    q = sympify(convert(data.q), {data.symbol: x})
    expression = p / simplify(q)
    simple = simplify(expression)
    return simple, p, simplify(q), x


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
        (expression, numerator, denominator, symbol) = parse(data)
        pcf = ramanujan.pcf.PCF(str(numerator), str(denominator))
        limit = pcf.limit(depth=data.i)
        computed_value = LIReC.db.access.identify(limit)
        body = {
            "expression": json.dumps(str(expression)),
            "limit": json.dumps("Infinity" if type(limit) is Infinity else str(limit)),
            "log_error": json.dumps(error_coordinates(expression, symbol, limit)),
            "delta": json.dumps(delta_coordinates(expression, denominator, symbol, limit)),
            "converges_to": json.dumps(computed_value)
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
        body = {
            "wolfram_says": WolframClient.raw(expression.expression.replace('**', '^'))
        }

        response = JSONResponse(content=body)
        return response

    except Exception as e:
        logger.warning(e)
        response = JSONResponse(status_code=500, content={"error": "Failed to parse inputs"})
        return response
