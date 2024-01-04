"""Entrypoint for the application and REST API handlers"""
import json
import uuid

import mpmath
import sympy
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy import simplify, sympify, oo, Symbol, Mul, Add
from sympy.core.numbers import Infinity

import constants
import logger
from graph_utils import error_coordinates, delta_coordinates
from input import Input, convert, Expression
from wolfram_client import WolframClient

app = FastAPI()

logger = logger.config()

mpmath.mp.dps = constants.PRECISION

origins = ["http://localhost:5173", "127.0.0.1:5173"]

# Only allow traffic from localhost and restrict methods to those we intend to use
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_credentials=True,
                   allow_headers=["*"])


def parse(data: Input) -> tuple[Mul, Add, Symbol]:
    """
    Process user inputs into math expressions
    :param data: User form inputs
    :return: tuple including p/q, simplified q and the symbol/variable used in these expressions
    """
    x = Symbol(data.symbol, real=True)
    p = sympify(convert(data.p), {data.symbol: x})
    q = sympify(convert(data.q), {data.symbol: x})
    simple_q = simplify(q)
    expression = p / simple_q
    simple = simplify(expression)
    return simple, simple_q, x


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
        (expression, denominator, symbol) = parse(data)

        limit = sympy.limit(expression, symbol, oo)

        body = {
            "expression": json.dumps(str(expression)),
            "limit": json.dumps("Infinity" if type(limit) is Infinity else str(limit)),
            "log_error": json.dumps(error_coordinates(expression, symbol, limit)),
            "delta": json.dumps(delta_coordinates(expression, denominator, symbol, limit)),
            "computed_value": 0  # @TODO: replace with actual computation to i
        }
        logger.debug(f"Response: {body}")
        response = JSONResponse(content=body)
        response.set_cookie(key="trm", value=str(uuid.uuid4()))
        return response

    except Exception as e:
        logger.warning(e)
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
