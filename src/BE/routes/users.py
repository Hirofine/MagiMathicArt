import bcrypt
import secrets
from datetime import datetime, timedelta
import binascii
import json
from helper import verify_token, TOKEN_VALIDE, TOKEN_EXPIRE, TOKEN_INVALIDE, TOKEN_NOT_SENT, USER_NOT_EXISTANT
#from starlette.responses import JSONResponse
from config.db import get_db, Session
from sqlalchemy import text, or_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Query, Request
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from models.index import Users
from schemas.index import User, UserCreate, UserUpdate
from crud.users import create_user, get_user, update_user, delete_user  # Importez les fonctions spécifiques



class PseudoAvailabilityResponse:
    def __init__(self, available: bool, message: str):
        self.available = available
        self.message = message

class LoginResponse:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message



user = APIRouter()

@user.post("/users/", response_model=User)
def rt_create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = dict(user)  # Convertit l'objet UserCreate en dictionnaire
    return create_user(db, user_data)

@user.post("/register/")
def rt_create_user(user: UserCreate,  request: Request, db: Session = Depends(get_db)):
    user_data = dict(user)  # Convertit l'objet UserCreate en dictionnaire
    
    password = user_data["passw"]
    hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    

    token = secrets.token_hex(32)
    print("token : ", token)
    token_char = token
    token_len_hour = 10
    tokenExpi = datetime.now() + timedelta(hours=token_len_hour)
    tokenSalt = bcrypt.gensalt().decode()

    token_salted = token + tokenSalt
    hashed_token = bcrypt.hashpw(token_salted.encode("utf-8"), bcrypt.gensalt())

    
    user_data["passw"] = hash
    user_data["token"] = hashed_token
    user_data["tokenExpi"] = tokenExpi
    user_data["tokenSalt"] = tokenSalt
    try :
        new_user = create_user(db, user_data)
    except SQLAlchemyError as e:
        print(f"User creation failed due to database Error: {e}")
        return JSONResponse(content={"message": f"User creation failed due to database Error: {e}"})
    except Exception as e:
        print(f"User creation failed: {e}")
        return JSONResponse(content={"message": f"User creation failed: {e}"})
    
    cookie_content = {
        "id" : new_user.id,
        "pseudo" : new_user.pseudo,
        "token": token_char
    }

    response = JSONResponse(content={"message": "Connexion réussie"})
    #response.set_cookie("session", cookie_content, secure=True, httponly=True, max_age=3600 * token_len_hour, domain="hirofine.fr", samesite="None", path="/")
    response.set_cookie("session", cookie_content, secure=True, httponly=True, max_age=3600 * token_len_hour, domain="localhost", samesite="None", path="/")
    
    print(response.raw_headers)
    
    return response

@user.get("/verify-session/")
def verify_session(request: Request, db: Session = Depends(get_db)):
    tok = verify_token(request, db)
    if (tok == TOKEN_VALIDE):
        return JSONResponse(content={"message": "Le token est valide", "data" : True})
    elif (tok == TOKEN_EXPIRE):
        return JSONResponse(content={"message": "Session expirée", "data" : False})
    elif (tok == TOKEN_INVALIDE):
        return JSONResponse(content={"message": "Session non valide", "data" : False})
    else:
        return JSONResponse(content={"message": "Error while verifying session", "data" : False})

@user.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    user_data = dict(user)  # Convertit l'objet UserCreate en dictionnaire
    password = user_data["passw"]
    user_db = db.query(Users).filter(Users.pseudo == user_data["pseudo"]).first()
    db.close()


    if user_db:
        if bcrypt.checkpw(password.encode("utf-8"), user_db.passw.encode("utf-8")):

            token = secrets.token_hex(32)
            print("token : ", token)
            token_char = token
            token_len_hour = 10
            tokenExpi = datetime.now() + timedelta(hours=token_len_hour)
            tokenSalt = bcrypt.gensalt().decode()

            token_salted = token + tokenSalt
            hashed_token = bcrypt.hashpw(token_salted.encode("utf-8"), bcrypt.gensalt())

            user_data["token"] = hashed_token
            user_data["tokenExpi"] = tokenExpi
            user_data["tokenSalt"] = tokenSalt

            cookie_content = {
                "id" : user_db.id,
                "pseudo" : user_db.pseudo,
                "token": token_char
            }
            
            user = User(id= user_db.id,
                    pseudo= user_db.pseudo,
                    passw= user_db.passw,
                    token= hashed_token,
                    tokenExpi= tokenExpi.isoformat(),
                    tokenSalt= tokenSalt
                )
            
            updated_user = update_user(db, user_db.id, user)

            response_data = JSONResponse(content={"message": "Connexion réussie", "data": True})
            #response_data.set_cookie("session", cookie_content, secure=True, httponly=True, max_age=3600 * token_len_hour, domain="hirofine.fr", samesite="None", path="/")
            response_data.set_cookie("session", cookie_content, secure=True, httponly=True, max_age=3600 * token_len_hour, domain="localhost", samesite="None", path="/")
        else :
            response_data = LoginResponse(success = False, message = "Mot de Passe invalide")
    else :
        response_data = LoginResponse(success = False, message = "Cet Utilisateur n'existe pas")
    
    return response_data

@user.get("/disconnect")
def disconnect(request: Request, db: Session = Depends(get_db)):
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
            user = User(id= db_user.id,
                    pseudo= db_user.pseudo,
                    passw= db_user.passw,
                    token= db_user.token,
                    tokenExpi= datetime.utcfromtimestamp(0).isoformat(),
                    tokenSalt= db_user.tokenSalt
                )
            updated_user = update_user(db, db_user.id, user)
            return JSONResponse(content={"message": "Vous avez été déconnecté", "data" : True}) 

        return JSONResponse(content={"message": "Session expirée", "data" : False})
    return JSONResponse(content={"message": "Session non valide", "data" : False})
    return 0

@user.get("/check-pseudo/")
def check_pseudo(pseudo: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.pseudo == pseudo).first()
    db.close()
    if user:
        response_data = PseudoAvailabilityResponse(available = False, message = "Pseudo déjà pris")
    else :
        response_data = PseudoAvailabilityResponse(available = True, message = "Pseudo disponible")
    return response_data
 
@user.get("/users/{user_id}", response_model=User)
def rt_read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.put("/users/{user_id}", response_model=User)
def rt_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@user.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
