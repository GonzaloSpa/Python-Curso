from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

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


@app.get("/users")       
async def users():
    return users_list

#Path
@app.get("/user/{id}")       
async def user(id: int):
     return search_users(id)
 
 
#Query
@app.get("/user/")       
async def user(id: int):
    return search_users(id)
# http://127.0.0.1:8000/user/?id=1 el id="int" lleva el valor de la id del user  

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha podido encontrar el usuario"}