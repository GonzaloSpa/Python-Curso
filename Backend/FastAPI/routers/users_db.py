from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}) 



users_list = []

@router.get("/", status_code=status.HTTP_200_OK)       
async def users():
    return users_list

#Path
@router.get("/{id}", status_code=status.HTTP_200_OK)       
async def user(id: int):
     return search_users(id)
 
 
#Query
@router.get("/")       
async def user(id: int):
    return search_users(id)
# http://127.0.0.1:8000/user/?id=1 el id="int" lleva el valor de la id del user  

# crendo un POST

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)  
async def user(user: User):
    if type(search_user_by_email(user.email)) == User:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error el usuario ya existe")   
   
    user_dict = dict(user)
    del user_dict["id"]
    print (user_dict)
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    
    return User(**new_user)
    

# creando un PUT (actualiza)

@router.put("/")
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

@router.delete("/{id}")        # por PATH el id es obligatorio
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
           del users_list[index]
           found =True           
    
    if not found:
        return {"error": "No se ha podido eliminar el usuario"}      
 
 
def search_user_by_email(email: str):
    try:
        user = db_client.local.users.find_one({"email": email})
        return User(**user_schema(user)) 
    except:
        return {"error": "No se ha podido encontrar el usuario"}
    

def search_users(id: int):
    return ""