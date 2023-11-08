from config.db import Session
from fastapi import Request
from fastapi.responses import JSONResponse
from models.index import Users
from schemas.index import User, UserCreate, UserUpdate
from crud.users import create_user, get_user, update_user, delete_user  # Importez les fonctions spécifiques
import json
import bcrypt
from datetime import datetime, timedelta

TOKEN_VALIDE = 0
TOKEN_EXPIRE = 1
TOKEN_INVALIDE = 2
TOKEN_NOT_SENT = 3
USER_NOT_EXISTANT = 4

def verify_token(request: Request, db: Session):
    session = request.cookies.get("session")

    if not session:
        return JSONResponse(content={"message": "Session non valide", "data" : False})
    
    session = json.loads(session.replace("'", "\""))
    user_id = session["id"]
    user_pseudo = session["pseudo"]
    token = session["token"]
    #find user in database
    db_user = get_user(db, user_id)
    if db_user is None:
        return JSONResponse(content={"message": "Cet utilisateur n'existe pas", "data" : False})
    
    #extract data from user in the db
    db_token_hash = db_user.token
    db_token_expi = db_user.tokenExpi
    db_token_salt = db_user.tokenSalt

    # if user found, add salt
    token_salted = token + db_token_salt

    #compare hash to db stored hash
    if (bcrypt.checkpw(token_salted.encode("utf-8"), db_token_hash.encode("utf-8"))):
        #check token time validity
        date_format = "%Y-%m-%d %H:%M:%S"
        #date_obj = datetime.strptime(db_token_expi, date_format)
        print(db_token_expi)
        if (db_token_expi > datetime.now()):
            return TOKEN_VALIDE   #token valide    
        return TOKEN_EXPIRE    #token expiré
    return TOKEN_INVALIDE    #token non valide / token non existant
