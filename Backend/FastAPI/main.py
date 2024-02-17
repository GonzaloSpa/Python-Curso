from fastapi import FastAPI
from routers import products, users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")        ##entrando al contexto de fastApi con el @app
async def root():
    return "¡Hola FastAPI!"


@app.get("/url")        
async def url():
    return {"url_curso" : "https://mouredev.com/python"}


# iniciar el server: uvicorn main:app --reload
# C + ctrl 