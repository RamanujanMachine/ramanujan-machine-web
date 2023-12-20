"""Entrypoint for the application and REST API handlers"""
import json
import uuid

import mpmath
import sympy
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy import simplify, sympify, oo, Symbol

import constants
import logger
from graph_utils import error_coordinates, delta_coordinates
from input import Input, convert
from wolfram_client import WolframClient

app = FastAPI()

logger = logger.config()

PRECISION = constants.PRECISION

origins = ["http://localhost:5173", "127.0.0.1:5173"]

# Only allow traffic from localhost and restrict methods to those we intend to use
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_credentials=True,
                   allow_headers=["*"])


@app.post("/analyze")
async def analyze(request: Request):
    """
    :param request: HTTP request
    :return: HTTP response indicating success of parsing inputs with a 200 or a 500 to indicate failure parsing inputs
    """
    # parse posted body as Input

    mpmath.mp.dps = PRECISION

    try:
        data = Input(**(await request.json()))
        x = Symbol(data.symbol, real=True)
        p = sympify(convert(data.p), {data.symbol: x})
        q = sympify(convert(data.q), {data.symbol: x})
        simple_q = simplify(q)
        expression = p / simple_q
        simple = simplify(expression)

        q_limit = sympy.limit(simple_q, x, oo)
        limit = sympy.limit(simple, x, oo)

        body = {
            "wolfram_limit": WolframClient.limit(str(simple)),
            "limit": json.dumps(float(limit)),
            "denominator_limit": json.dumps(float(q_limit)),
            "log_error": json.dumps(error_coordinates(simple, x, limit)),
            "delta": json.dumps(delta_coordinates(simple, simple_q, x, limit)),
            "computed_value": json.dumps(float(limit))  # @TODO: replace with actual computation to i
        }

        response = JSONResponse(content=body)
        response.set_cookie(key="trm", value=str(uuid.uuid4()))
        return response

    except Exception as e:
        logger.warning(e)
        response = JSONResponse(status_code=500, content={"error": "Failed to parse p / q"})
        return response
