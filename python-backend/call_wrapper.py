import logging

import grpc
import lirec_pb2
import sympy.core.numbers
import lirec_pb2_grpc
from ramanujantools.pcf import PCF
import signal
from constants import EXTERNAL_PROCESS_TIMEOUT

logger = logging.getLogger('rm_web_app')


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def pcf_limit(a, b, n) -> str:
    """
    Invokes ResearchTools limit computation
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(EXTERNAL_PROCESS_TIMEOUT)

    try:
        pcf = PCF(a, b)
        lim = pcf.limit(n)
        return lim.as_rounded_number()
    except TimeoutException:
        print(f"PCF limit query exceeded timeout.")
        return None
    except Exception as e:
        logger.error(f"Exception: {e}")
    finally:
        signal.alarm(0)


def lirec_identify(limit) -> [list[sympy.core.numbers.Number], list[sympy.core.numbers.Number]]:
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
            return [response.closed_forms, response.see_also]
    except TimeoutException:
        print(f"PCF limit query exceeded timeout.")
        return None
    except Exception as e:
        logger.error(f"Exception: {e}")
    finally:
        signal.alarm(0)
