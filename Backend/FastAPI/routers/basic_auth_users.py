from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
                

app = FastAPI()

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
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@moredev.com",
        "disable": True,
        "password": "654321"
    } 
}

# mecanismo que busca en la base de datos si esta el usuario

def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])
    
# operacion que es capaz de autenticarnos 
