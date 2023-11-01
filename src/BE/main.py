from typing import Union

from fastapi import FastAPI
from routes.index import user, projet, couleur, palette, image, pixelart, reponse
from routes.index import assopalettecouleur, assoprojetpalettereponse, assoprojetimage
from routes.index import assoprojetreponse, assoprojetpalette, assoprojetpixelart
from routes.index import assouserprojet, assouserpalette, assouserimage, assouserreponse, assouserpixelart
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(user)
app.include_router(projet)
app.include_router(couleur)
app.include_router(palette)
app.include_router(image)
app.include_router(pixelart)
app.include_router(reponse)

app.include_router(assopalettecouleur)

app.include_router(assoprojetpalettereponse)
app.include_router(assoprojetimage)
app.include_router(assoprojetreponse)
app.include_router(assoprojetpalette)
app.include_router(assoprojetpixelart)

app.include_router(assouserprojet)
app.include_router(assouserpalette)
app.include_router(assouserimage)
app.include_router(assouserreponse)
app.include_router(assouserpixelart)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost/"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],

)