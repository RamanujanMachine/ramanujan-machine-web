import json
import re
import uuid

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sympy import simplify, sympify
from sympy.abc import _clash1

from secrets import Secrets
from wolfram_client import WolframClient

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

# Only allow traffic from localhost and restrict methods to those we intend to use
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_credentials=True,
                   allow_headers=["*"])


# The structure of the post body from the frontend
class Input(BaseModel):
    p: str
    q: str
    i: int


def convert(polynomial: str):
    """
    Take an acceptable math polynomial entered by a user and convert to one that Python can parse
    :param polynomial: incoming polynomial entered by user in web frontend
    :return: python parse-able polynomial
    """
    return re.sub(r'([0-9.-])+([a-zA-Z])', '\\1*\\2', polynomial.replace('^', '**'))


@app.post("/analyze")
async def analyze(request: Request):
    """

    :param request: HTTP request
    :return: HTTP response indicating success of parsing inputs with a 200 or a 500 to indicate failure parsing inputs
    """
    # parse posted body as Input
    data = Input(**(await request.json()))

    # convert to math expression
    try:
        expression = sympify(convert(data.p), _clash1) / sympify(convert(data.q), _clash1)
        simple = str(simplify(expression))
        response = JSONResponse(content=WolframClient.limit(simple))
        response.set_cookie(key="trm", value=str(uuid.uuid4()))
        return response
    except Exception as e:
        print("p/q error", e)
        response = JSONResponse(status_code=500, content={"error": "Failed to parse p / q"})
        return response
