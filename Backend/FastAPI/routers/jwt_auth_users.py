from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "16d44d487e423d1b3b6a373ed78abfe35c3c77b3d313f4c94bdf653729a5c29f"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@moredev.com",
        "disable": False,
        "password": "$2a$12$9uzQ6qXEPPt3ixC.OTWv6uZFNCO9TZ1BrQgQOMOLxxJEr8uTMllO."
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@moredev.com",
        "disable": True,
        "password": "$2a$12$dRQDTqvjOWxy6T0jjXbDfugNOGP3CEWzv2R3TDoBBom/1HrAJFJFO"
    } 
}

def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



async def auth_user(token: str = Depends(oauth2)):
    exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
             raise exeption
         
    except JWTError:
        raise exeption
    
    return search_user(username)





async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
        
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
          
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "beared"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)): 
    return user


