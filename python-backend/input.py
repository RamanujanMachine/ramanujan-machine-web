""" Processing of the post body from the frontend """
import logging
import re

from pydantic import BaseModel

logger = logging.getLogger('rm_web_app')


class Input(BaseModel):
    """Structure of user form data"""
    a: str
    b: str
    i: int
    symbol: str


def convert(polynomial: str) -> str:
    """
    Take an acceptable math polynomial entered by a user and convert to one that Python can parse
    :param polynomial: incoming polynomial entered by user in web frontend
    :return: python parse-able polynomial
    """
    expression = re.sub(r'([0-9]+)([a-zA-Z])', '\\1*\\2',
                        polynomial.replace('^', '**').replace(' ', '').replace(')(', ')*('))
    expression = re.sub(r'([0-9a-zA-Z])(\()', '\\1*\\2', expression)
    logger.debug(f"input: {polynomial} output: {expression}")
    return expression


class Expression(BaseModel):
    """Structure of user form data"""
    expression: str
