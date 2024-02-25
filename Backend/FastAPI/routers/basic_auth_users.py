from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
 # OAuth2PasswordBearer = se encarga de gestionar la autenticacion del usuario y contraseña
 # OAuth2PasswordRequestForm = la forma en la que se va a enviar desde el cliente el usuario y contraseña 
 #  y la forma en la que el backend captura el usuario y contraseña para comprobar si es un usuario de nuestro sistema

router = APIRouter()
# instancia de sistema de oauth2 (un standar de como tenemos que trabajar con nuesto api)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")



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
def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

  
# criterio de dependecia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


# operacion que es capaz de autenticarnos 

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
        
    user = search_user_db(form.username)
    if not form.password == user.password:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
          
          
    return {"access_token": user.username , "token_type": "beared"} #el tipo de token es beared esto es dentro de un standar 
# el access token es el token de autenticacion, como backend puede decirle siempre que me pases algo que para mi es correcto (token) yo te voy a mostrar los datos. Sino deberiamos 
# darle al  backend todo el tiempo el usuario y contraseña.  # en realidad en casi todos los casos se usa un access_token cifrado


@router.get("/users/me")
async def me(user: User = Depends(current_user)): # depende de que el usario este autenticado
    return user
