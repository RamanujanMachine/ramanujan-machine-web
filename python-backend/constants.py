"""
A centralized listing of constants that are used as settings for the API
"""
DEFAULT_PRECISION = 30
# evalf allows for verbose output via param universally set to this:
VERBOSE_EVAL = False
# chunk size to send to front end via web socket when computing coordinate pairs
BATCH_SIZE = 500
# when calling ResearchTools or LIReC, only way this many seconds before throwing a timeout exception
EXTERNAL_PROCESS_TIMEOUT = 10
