"""A place to keep secrets"""
import logging
import os
import traceback
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger('rm_web_app')

try:
    logger.debug(f"dotenv location {find_dotenv('.env')}")
    load_dotenv(find_dotenv('.env', raise_error_if_not_found=True), verbose=True)
except Exception as e:
    logger.warning(traceback.format_exc())


@dataclass(frozen=True)
class CustomSecrets:
    """
    Secrets container
    """
    WolframAppId: str = os.getenv('WOLFRAM_APP_ID')
    BasicUser: str = os.getenv('BASIC_USER')
    BasicPassword: str = os.getenv('BASIC_PASSWORD')
