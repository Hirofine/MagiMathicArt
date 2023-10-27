from typing import Union

from fastapi import FastAPI
from routes.index import user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(user)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost/"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],

)