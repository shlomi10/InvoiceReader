from invoice_reader import analyze_invoice_url
from fastapi import FastAPI, HTTPException, Query
from db import *

'''
FastAPI app with two endpoints:
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
        return analyze_invoice_url(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from invoice_reader import save_invoice_to_db
@app.get("/read-invoice-by-url")
def read_invoice_by_url(url: str = Query(..., description="Direct image URL")):
    try:
        data = analyze_invoice_url(url)
        save_invoice_to_db(data)
        return {"status": "saved", "invoice": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

