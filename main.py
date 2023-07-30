from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Assuming you want to save the uploaded file to a specific location
    with open(f"uploaded_{file.filename}", "wb") as f:
        f.write(await file.read())
    
    return {"message": f"File {file.filename} has been uploaded."}