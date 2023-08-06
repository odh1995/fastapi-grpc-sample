from fastapi import FastAPI, File, UploadFile
import time
import grpc
import requests

import file_transfer_pb2
import file_transfer_pb2_grpc
import send_text_pb2
import send_text_pb2_grpc

app = FastAPI()

def upload_file_with_grpc(file_content):
    with grpc.insecure_channel("localhost:50051") as channel:  # Connect to the gRPC server
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        response = stub.UploadFile(iter([file_transfer_pb2.FileChunk(content=file_content)]))
        return response.success

def send_text_with_grpc(text):
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = send_text_pb2_grpc.SendTextStub(channel)  # Use the correct stub class
        request = send_text_pb2.Text(text=text)    # Create the request message
        response = stub.Send(request)              # Send the request message
        return response.sucess
    
@app.post("/upload_grpc/")
async def upload_file_grpc(file: UploadFile = File(...)):
    content = await file.read()
    start_time = time.time()
    success = upload_file_with_grpc(content)
    if success:
        print(f"Sending file using gRPC speed: {time.time() - start_time}")
        return {"message": f"File {file.filename} has been uploaded."}
    else:
        return {"message": "Failed to upload the file."}

@app.post("/upload_rest")
async def upload_file_rest(file: UploadFile = File(...)):
    server_url = "http://localhost:8001/upload/"
    headers = {"accept": "application/json"}  # Set the Content-Type header for file upload
    files = {"file": (file.filename, await file.read())}
    start_time = time.time()
    response = requests.post(server_url, files=files, headers=headers)
    if response.status_code == 200:
        print(f"Sending file using Rest speed: {time.time() - start_time}")
        return response.json()
    else:
        print(response)
        return {"message": "Failed to upload the file."}

@app.post("/send_text_grpc")
async def send_text_grpc(text: str):
    start_time = time.time()
    success = send_text_with_grpc(text)
    if success:
        print(f"Sending text using gRPC speed:{time.time() - start_time}")
        return {"message": f"Text received!"} 
    else:
        return {"message": f"Failed to send text"} 
@app.post("/send_text_rest")
async def send_text_rest(text: str):
    server_url = "http://localhost:8001/send_text/"
    headers = {"accept": "application/json"}  # Set the Content-Type header for file upload
    start_time = time.time()
    response = requests.post(server_url, params={"text": text}, headers=headers)
    if response.status_code == 200:
        print(f"Sending text using Rest speed: {time.time() - start_time}")
        return response.json()
    else:
        print(response)
        return {"message": "Failed to upload the file."}
