"""Entrypoint for the application and REST API handlers"""
import json
import secrets
import sys
from pathlib import Path
from typing import Annotated

import mpmath
from fastapi import Depends, FastAPI, HTTPException, Request, status, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from ramanujantools import pcf
from sympy import sympify
from sympy.core.numbers import Infinity

import call_wrapper
import constants
import logger
from custom_secrets import CustomSecrets
from graph_utils import (chart_coordinates)
from input import Input, Expression, parse
from math_utils import laurent, assess_convergence
from wolfram_client import WolframClient

sys.set_int_max_str_digits(0)

security = HTTPBasic()

app = FastAPI()

logger = logger.config(True)

mpmath.mp.dps = constants.DEFAULT_PRECISION

app.mount("/form", StaticFiles(directory="build"), name="react")


def auth(creds: Annotated[HTTPBasicCredentials, Depends(security)]):
    """

    Parameters
    ----------
    creds : HTTPBasicCredentials username and password

    Returns
    -------
    True if the credentials are valid, raises HTTPException with 401 Unauthorized otherwise
    """
    input_user = creds.username.encode("utf8")
    correct_user = CustomSecrets.BasicUser.encode("utf8")
    input_pass = creds.password.encode("utf8")
    correct_pass = CustomSecrets.BasicPassword.encode("utf8")
    if not (secrets.compare_digest(input_user, correct_user) and secrets.compare_digest(input_pass, correct_pass)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    logger.info("user authenticated")
    return True


@app.get("/")
def default(authenticated=Depends(auth)) -> RedirectResponse:
    """
    Make sure to redirect bare IP/url to form landing page
    """
    if authenticated:
        return RedirectResponse(url='/form')


@app.get("/form")
def serve_frontend(authenticated=Depends(auth)) -> FileResponse:
    """
    Serves static React UI - facilitates embedding as iframe
    """
    if authenticated:
        project_path = Path(__file__).parent.resolve()
        response = FileResponse(str(project_path / "build/index.html"), media_type="text/html")
        response.headers["X-Frame-Options"] = "ALLOW-FROM https://www.ramanujanmachine.com"
        return response


@app.post("/verify")
async def analyze(request: Request) -> JSONResponse:
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
            iterations = data.i
            (a_func, a, b_func, b, symbol, precision) = parse(data)

            with mpmath.workdps(precision):
                if len(data.symbol) > 0:
                    logger.debug('checking for convergence...')
                    is_convergent = assess_convergence(laurent(a, b, symbol), symbol)
                    logger.debug('convergence result: {}'.format(is_convergent))
                    # short circuit if the preliminary test fails
                    await websocket.send_json({"is_convergent": is_convergent})

                    if is_convergent is False:
                        logger.debug(f"values do not converge. closing socket.")
                        await websocket.close()

                limit = call_wrapper.pcf_limit(sympify(data.a), sympify(data.b), iterations)
                logger.debug(f"limit: {limit}")
                await websocket.send_json({"limit": "Infinity" if type(limit) is Infinity else str(limit)})

                [computed_values, see_also] = call_wrapper.lirec_identify(limit)

                json_computed_values = []
                for m in computed_values:
                    logger.debug(f"identify returned: {m}")
                    json_computed_values.append(str(m))

                await websocket.send_json(
                    {"converges_to": json.dumps(json_computed_values)}
                )

                json_see_also = []
                for m in see_also:
                    logger.debug(f"identify returned see_also: {m}")
                    json_see_also.append(str(m))

                await websocket.send_json(
                    {"see_also": json.dumps(json_see_also)}
                )

                await chart_coordinates(pcf=pcf.PCF(sympify(data.a), sympify(data.b)),
                                        limit=mpmath.mpf(limit),
                                        iterations=iterations,
                                        websocket=websocket)

        except WebSocketDisconnect:
            logger.debug("Websocket disconnected")
            break
        except WebSocketException as e:
            logger.debug(f"Websocket exception {e}")
            break

    await websocket.close()
