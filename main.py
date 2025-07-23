from invoice_reader import analyze_invoice_url
from fastapi import FastAPI, HTTPException, Query
from db import *
from invoice_reader import save_invoice_to_db
from fastapi import File, UploadFile
from aws_file_utils import upload_and_get_presigned_url
from invoice_reader import analyze_invoice_url

'''
FastAPI app with endpoints:
/: returns a hello message.
/read-invoice-by-url: invokes analyze_invoice_url() using image URL as a query param.
Calls init_db() on startup.
'''

app = FastAPI()
init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# To run the app, use the command:
# uvicorn main:app --host localhost --port 8000

@app.get("/read-invoice-by-url")
def read_invoice_by_url(url: str = Query(..., description="Direct image URL")):
    try:
        data = analyze_invoice_url(url)
        save_invoice_to_db(data)
        return {"status": "saved", "invoice": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-invoice-file")
def upload_invoice_file(file: UploadFile = File(...)):
    try:
        file_bytes = file.file.read()
        key, url = upload_and_get_presigned_url(file_bytes, file.filename, file.content_type)
        print (f"Presigned s3 url: {url}")
        data = analyze_invoice_url(url)
        data["file_key"] = key
        save_invoice_to_db(data)
        return {"status": "success", "invoice": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

