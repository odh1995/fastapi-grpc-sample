from fastapi import FastAPI, File, UploadFile
import grpc

import file_transfer_pb2
import file_transfer_pb2_grpc

app = FastAPI()

def upload_file_with_grpc(file_content):
    with grpc.insecure_channel("localhost:50051") as channel:  # Connect to the gRPC server
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        response = stub.UploadFile(iter([file_transfer_pb2.FileChunk(content=file_content)]))
        return response.success

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    success = upload_file_with_grpc(content)
    if success:
        return {"message": f"File {file.filename} has been uploaded."}
    else:
        return {"message": "Failed to upload the file."}
