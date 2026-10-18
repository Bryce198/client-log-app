from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from thealth_client_app.routes import clients, employees, auth

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



@app.get("/", status_code=status.HTTP_200_OK)
def get_home():
    return {"Message": "Hello Home Page"}

app.include_router(clients.router)
app.include_router(employees.router)
app.include_router(auth.router)