from typing import Union

from fastapi import FastAPI
from routes.index import user, projet, couleur, palette, image
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(user)
app.include_router(projet)
app.include_router(couleur)
app.include_router(palette)
app.include_router(image)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost/"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],

)