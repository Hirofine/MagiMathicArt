import bcrypt
import secrets
from datetime import datetime, timedelta
import binascii
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
    user_data["passw"] = hash

    token = secrets.token_bytes(32)
    token_char = binascii.hexlify(token).decode()
    print(token)
    tokenExpi = datetime.now() + timedelta(hours=1)
    tokenSalt = bcrypt.gensalt()

    token_salted = token + tokenSalt
    hashed_token = bcrypt.hashpw(token_salted, bcrypt.gensalt())

    

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
    response.set_cookie("session", cookie_content, secure=True, httponly=True, max_age=36000, domain="hirofine.fr", samesite="None", path="/")
    print(response.raw_headers)
    
    return response

@user.get("/verify-session/")
def verify_session(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session")
    print(token)
    if not token:
        return JSONResponse(content={"message": "Session non valide", "data" : False})
    
    
    return JSONResponse(content={"message": "Session non valide", "data" : False})

@user.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    user_data = dict(user)  # Convertit l'objet UserCreate en dictionnaire
    password = user_data["passw"]
    user_db = db.query(Users).filter(Users.pseudo == user_data["pseudo"]).first()
    db.close()
    if user_db:
        if bcrypt.checkpw(password.encode("utf-8"), user_db.passw.encode("utf-8")):
            response_data = LoginResponse(success= True, message = "Connexion réussie")
        else :
            response_data = LoginResponse(success = False, message = "Mot de Passe invalide")
    else :
        response_data = LoginResponse(success = False, message = "Cet Utilisateur n'existe pas")
    
    return response_data


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
