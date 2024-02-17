from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(tags=["users"])

# Inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Gonzalo", surname="Spaltro", url= "https://gonzalo.com", age=25),
              User(id=2, name="Ricardo",surname= "Narain", url="https://narain.com", age= 23),
              User(id=3, name="Juliet", surname="Ranses", url="https://juliet.com", age= 21),]


@router.get("/users", status_code=200)       
async def users():
    return users_list

#Path
@router.get("/user/{id}", status_code=200)       
async def user(id: int):
     return search_users(id)
 
 
#Query
@router.get("/user/")       
async def user(id: int):
    return search_users(id)
# http://127.0.0.1:8000/user/?id=1 el id="int" lleva el valor de la id del user  



# crendo un POST

@router.post("/user/", response_model=User, status_code=201)   # definiendo un status code  / con el response_model nos indica que nos va a responder un objeto de tipo User (en la docu sale el json) 
async def user(user: User):
    if type(search_users(user.id)) == User:
       raise HTTPException(status_code=404, detail="error el usuario ya existe")   #raise propaga la exepcecion 
    else:
        users_list.append(user)
        return user
    

# creando un PUT (actualiza)

@router.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha podido actualizar el usuario"}    
    else:      
        return user  
    
 
# creando un DELETE

@router.delete("/user/{id}")        # por PATH el id es obligatorio
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
           del users_list[index]
           found =True           
    
    if not found:
        return {"error": "No se ha podido eliminar el usuario"}      
 
 
def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha podido encontrar el usuario"}
    
