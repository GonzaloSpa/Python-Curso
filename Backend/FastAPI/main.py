from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users,users_db
from fastapi.staticfiles import StaticFiles
app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name=("static")) # metodo para montar y exponer  http://127.0.0.1:8000/static/images/gonzalo.JPG


@app.get("/")        ##entrando al contexto de fastApi con el @app
async def root():
    return "¡Hola FastAPI!"


@app.get("/url")        
async def url():
    return {"url_curso" : "https://mouredev.com/python"}


# iniciar el server: uvicorn main:app --reload
# C + ctrl 