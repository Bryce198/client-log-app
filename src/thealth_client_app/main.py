from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()





@app.get("/")
def get_home():
    return {"Message": "Hello Home Page"}


@app.get("/clients")
def get_clients():
    return {"Clients": "Client Data"}

