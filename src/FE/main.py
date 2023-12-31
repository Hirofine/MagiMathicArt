from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse
from os import path

app = FastAPI()

# Configuration de CORS
origins = ["https://magimathicart.hirofine.fr","https://be.magimathicart.hirofine.fr", "http://localhost:8001", "http://localhost:7801"] # permettre l'accès à partir de n'importe quelle origine
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

origins = ["*"]
methods = ["*"]
headers = ["*"]

# Montage du dossier contenant les fichiers statiques (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/game", StaticFiles(directory="game"), name="game")
#app.mount("/admin", StaticFiles(directory="admin"), name="admin")
#app.mount("/icone", StaticFiles(directory="icone"), name="icone")



# Réponse de l'application pour le favicon.ico
@app.get('/favicon.ico')
async def get_favicon():
    return FileResponse('static/favicon.ico')

# Réponse de l'application en renvoyant le fichier "index.html" situé dans le dossier racine
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(path.join("static", "index.html"), "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/account_creation")
async def read_root():
    with open(path.join("static", "pages/account_creation.html"), "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/account_login")
async def read_root():
    with open(path.join("static", "pages/account_login.html"), "r") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/my_account")
async def read_root():
    with open(path.join("static", "pages/my_account.html"), "r") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/color_picker")
async def read_root():
    with open(path.join("static", "pages/color_picker.html"), "r") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/palette_editor")
async def read_root():
    with open(path.join("static", "pages/palette_editor.html"), "r") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/reponse_editeur")
async def read_root():
    with open(path.join("static", "pages/reponse_editor.html"), "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/editeur")
async def read_root():
    with open(path.join("static", "pages/editeur.html"), "r") as f:
        return HTMLResponse(content=f.read())
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7801)