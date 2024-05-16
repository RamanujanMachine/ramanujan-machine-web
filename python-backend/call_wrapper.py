import logging
import signal

import grpc
import lirec_pb2
import sympy.core.numbers
from constants import EXTERNAL_PROCESS_TIMEOUT
import lirec_pb2_grpc
from ramanujan.pcf import PCF

logger = logging.getLogger('rm_web_app')


class TimeoutError(Exception):
    pass


def timeout_handler(signum: object, frame: object) -> None:
    """
    Simple handler when execution of functions exceeds time limit specified as EXTERNAL_PROCESS_TIMEOUT
    """
    raise TimeoutError("Function execution timed out")


def pcf_limit(a, b, n) -> str:
    """
    Invokes ResearchTools limit computation
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(EXTERNAL_PROCESS_TIMEOUT)
    try:
        pcf = PCF(a, b)
        lim = pcf.limit(n)
        logger.debug(f"${lim}  ${type(lim)}")
        return lim.as_rounded_number()

    except TimeoutError:
        print("Function execution timed out after {} seconds".format(EXTERNAL_PROCESS_TIMEOUT))
    finally:
        signal.alarm(0)


def lirec_identify(limit) -> list[sympy.core.numbers.Number]:
    """
    Invokes LIReC pslq algorithm
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(EXTERNAL_PROCESS_TIMEOUT)
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = lirec_pb2_grpc.LIReCStub(channel)
            request = lirec_pb2.IdentifyRequest(limit=limit)
            response = stub.Identify(request)
            logger.debug(f"gRPC client received: <{type(response)}> {str(response)}")
            logger.debug(f"gRPC client received: <{type(response.closed_forms)}> {str(response.closed_forms)}")
            return response.closed_forms
    except TimeoutError:
        print("Function execution timed out after {} seconds".format(EXTERNAL_PROCESS_TIMEOUT))
    finally:
        signal.alarm(0)
