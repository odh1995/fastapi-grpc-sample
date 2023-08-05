import grpc
from concurrent import futures
import time

import send_text_pb2
import send_text_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class SendTextServicer(send_text_pb2_grpc.SendTextServicer):
    def Send(self, request, context):
        print(request)
        return send_text_pb2.SendResponse(sucess=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    send_text_pb2_grpc.add_SendTextServicer_to_server(SendTextServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("gRPC server started on port 50052")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
