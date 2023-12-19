""" Processing of the post body from the frontend """
import re

from pydantic import BaseModel


class Input(BaseModel):
    """Structure of user form data"""
    p: str
    q: str
    i: int
    symbol: str


def convert(polynomial: str) -> str:
    """
    Take an acceptable math polynomial entered by a user and convert to one that Python can parse
    :param polynomial: incoming polynomial entered by user in web frontend
    :return: python parse-able polynomial
    """
    return re.sub(r'([0-9])+([a-zA-Z])', '\\1*\\2', polynomial.replace('^', '**'))
