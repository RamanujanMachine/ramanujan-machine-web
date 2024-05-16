"""A place to keep secrets"""
import logging
import os
import traceback
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger('rm_web_app')

try:
    logger.debug(f"dotenv location {find_dotenv()}")
    load_dotenv(find_dotenv())
except Exception as e:
    logger.warning(traceback.format_exc())


@dataclass(frozen=True)
class Secrets:
    """
    Secrets container
    """
    WolframAppId: str = os.getenv('WOLFRAM_APP_ID')
