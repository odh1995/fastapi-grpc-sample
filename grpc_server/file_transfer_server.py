import grpc
from concurrent import futures
import time

import file_transfer_pb2
import file_transfer_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request_iterator, context):
        with open("uploaded_file.txt", "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.content)
        return file_transfer_pb2.UploadResponse(success=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()

