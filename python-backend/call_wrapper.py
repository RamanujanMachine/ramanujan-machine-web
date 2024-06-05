import logging
import signal

import grpc
import lirec_pb2
import sympy.core.numbers
from constants import EXTERNAL_PROCESS_TIMEOUT
import lirec_pb2_grpc
from ramanujantools.pcf import PCF

logger = logging.getLogger('rm_web_app')


class TimeoutError(Exception):
    pass


def timeout_handler(signum: object, frame: object) -> None:
    """
    Simple handler when execution of functions exceeds time limit specified as EXTERNAL_PROCESS_TIMEOUT
    """
    raise TimeoutError("Function execution timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(EXTERNAL_PROCESS_TIMEOUT)


def pcf_limit(a, b, n) -> str:
    """
    Invokes ResearchTools limit computation
    """
    try:
        pcf = PCF(a, b)
        lim = pcf.limit(n)
        return lim.as_rounded_number()

    except TimeoutError:
        logger.error("Function execution timed out after {} seconds".format(EXTERNAL_PROCESS_TIMEOUT))
    finally:
        signal.alarm(0)


def lirec_identify(limit) -> list[sympy.core.numbers.Number]:
    """
    Invokes LIReC pslq algorithm
    """
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = lirec_pb2_grpc.LIReCStub(channel)
            request = lirec_pb2.IdentifyRequest(limit=limit)
            response = stub.Identify(request)
            return response.closed_forms
    except TimeoutError:
        logger.error("Function execution timed out after {} seconds".format(EXTERNAL_PROCESS_TIMEOUT))
    finally:
        signal.alarm(0)
