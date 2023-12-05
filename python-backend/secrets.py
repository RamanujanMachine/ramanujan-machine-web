from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


@dataclass(frozen=True)
class Secrets:
    WolframAppId: str = os.getenv('WOLFRAM_APP_ID')
