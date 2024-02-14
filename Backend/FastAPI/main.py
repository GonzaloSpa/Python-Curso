from fastapi import FastAPI

app = FastAPI()

@app.get("/")        ##entrando al contexto de fastApi con el @app
async def root():
    return "¡Hola FastAPI!"


@app.get("/url")        
async def url():
    return {"url_curso" : "https://mouredev.com/python"}


# iniciar el server: uvicorn main:app --reload
# C + ctrl 