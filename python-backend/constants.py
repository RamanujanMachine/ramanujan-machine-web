"""
A centralized listing of constants that are used as settings for the API
"""
DEFAULT_PRECISION = 30
HOSTS = ['localhost', '127.0.0.1']
PORTS = ['5173', '80']
# how many lines of a series to print for debugging purposes
DEBUG_LINES = 10
# evalf allows for verbose output via param universally set to this:
VERBOSE_EVAL = False
# chunk size to send to front end via web socket when computing coordinate pairs
BATCH_SIZE = 500
