"""Entrypoint for the application and REST API handlers"""
import json
import sys

import mpmath
from LIReC.db.access import db
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sympy.core.numbers import Infinity

import constants
import logger
from graph_utils import (chart_coordinates)
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


@app.websocket("/data")
async def data_socket(websocket: WebSocket):
    """
    Web socket to provide stream of data as it is computed
    Take user form inputs and parse them into mathematical expressions, then assess them in various ways and return
    chart coordinates to be rendered by the frontend
    """
    await websocket.accept()
    while True:
        try:
            data = Input(**(await websocket.receive_json()))
            logger.debug('received data. parsing...')
            iterations = data.i
            (a_func, a, b_func, b, symbol) = parse(data)

            if len(data.symbol) > 0:
                logger.debug('checking for convergence...')
                is_convergent = assess_convergence(laurent(a, b, symbol), symbol)
                logger.debug('convergence result: {}'.format(is_convergent))
                # short circuit if the preliminary test fails
                await websocket.send_json({"is_convergent": is_convergent})

                if is_convergent is False:
                    logger.debug(f"values do not converge. closing socket.")
                    await websocket.close()

            # per the link below, "when bi = 1 (the partial numerator) for all i the expression is called a
            # simple continued fraction" b here is the partial numerator (a and b are often used interchangeably
            # which may lead to confusion when there is no associated image of the continued fraction)
            # https://en.wikipedia.org/wiki/Continued_fraction#Basic_formula
            if data.b == "1":
                (values, num_values, denom_values) = simple_computed_values(a_func, iterations=iterations)
            else:
                # generalized continued fractions, where the partial numerator has its own formula and is not
                # equal to 1 https://en.wikipedia.org/wiki/Generalized_continued_fraction
                (values, num_values, denom_values) = generalized_computed_values(a_func, b_func,
                                                                                 iterations=iterations)

            limit = values[next(reversed(values))]
            logger.debug(f"last convergent / limit: {limit}")
            await websocket.send_json({"limit": "Infinity" if type(limit) is Infinity else str(limit)})

            computed_values = db.identify(values=[str(limit)], wide_search=True)
            for m in computed_values:
                logger.debug(f"identify returned: {m}")

            await websocket.send_json(
                {"converges_to": json.dumps(str(computed_values[0] if len(computed_values) > 0 else None))})

            await chart_coordinates(values,
                                    num_values,
                                    denom_values,
                                    limit,
                                    iterations=iterations,
                                    websocket=websocket)

        except WebSocketDisconnect:
            logger.debug("Websocket disconnected")
            break
        except WebSocketException:
            logger.debug("Websocket exception")
            break

        await websocket.close()
