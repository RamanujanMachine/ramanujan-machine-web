from concurrent import futures

import grpc
from LIReC.db.access import db

import constants
import lirec_pb2
import lirec_pb2_grpc
import logger

logger = logger.config(True)


class LIReCServicer(lirec_pb2_grpc.LIReCServicer):
    def Identify(self, request: lirec_pb2.IdentifyRequest, context: object) -> lirec_pb2.IdentifyResponse:
        logger.debug(f"Received request: <{type(request)}> {request}")
        closed_forms = db.identify(values=[request.limit], wide_search=[1], min_prec=constants.DEFAULT_PRECISION)
        logger.debug(f"Received response: <{type(closed_forms)}> {[str(item) for item in closed_forms]}")
        return lirec_pb2.IdentifyResponse(closed_forms=[str(item) for item in closed_forms])


def serve() -> None:
    """
    Start up the gRPC server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lirec_pb2_grpc.add_LIReCServicer_to_server(LIReCServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


serve()
