import os
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@dataclass(frozen=True)
class Secrets:
    """
    A place to consolidate secrets
    """
    WolframAppId: str = os.getenv('WOLFRAM_APP_ID')
