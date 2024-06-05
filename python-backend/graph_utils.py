"""Utility functions that generate graphable coordinate pairs for the frontend"""
import json
import logging
from typing import TypedDict

import mpmath
import sympy
from fastapi import WebSocket
from ramanujantools import pcf as pcf_module

GRAPHABLE_TYPES = (int, float, sympy.core.numbers.Integer, sympy.core.numbers.Float)

logger = logging.getLogger('rm_web_app')


class Point2D(TypedDict):
    """
    a type used to store coordinate pairs
    """
    x: int
    y: str


async def chart_coordinates(pcf: pcf_module.PCF, limit: mpmath.mpf,
                            iterations: int, websocket: WebSocket) -> None:
    """
    graph coords for the error of an expression: |expression - L|
    :param pcf: PCF instance
    :param limit: the computed approximate limit of the expression
    :param iterations: the number of values expected, n max
    :param websocket: the websocket instance to return incremental data
    :return: tuple of arrays of [x,y] pairs for graphing purposes
    """
    y_values = pcf.delta_sequence(limit=limit, depth=iterations)
    logger.debug(f'y_values: {y_values}')
    delta_x_y_pairs = [Point2D(x=n, y=str(y_values[n - 1])) for n in range(1, iterations)]

    await websocket.send_json({"delta": json.dumps(delta_x_y_pairs)})
