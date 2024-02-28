from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}) 



users_list = []

@router.get("/", response_model=list[User])       
async def users():
    return users_schema(db_client.local.users.find()) 

#Path
@router.get("/{id}", status_code=status.HTTP_200_OK)       
async def user(id: str):
    return search_user("_id", ObjectId(id))
 
 
#Query
@router.get("/")       
async def user(id: int):
    return search_user("_id", ObjectId(id))
# http://127.0.0.1:8000/user/?id=1 el id="int" lleva el valor de la id del user  

# crendo un POST

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)  
async def user(user: User):
    if type(search_user("email", user.email)) == User:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error el usuario ya existe")   
   
    user_dict = dict(user)
    del user_dict["id"]
    print (user_dict)
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    
    return User(**new_user)
    

# creando un PUT (actualiza)

@router.put("/", response_model= User)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        
    except:
        return {"error": "No se ha podido actualizar el usuario"}    

    return search_user("_id", ObjectId(user.id))
    
 
# creando un DELETE

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)        # por PATH el id es obligatorio
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "No se ha podido eliminar el usuario"}      
 
 
def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user)) 
    except:
        return {"error": "No se ha podido encontrar el usuario"}
    

def search_users(id: int):
    return ""