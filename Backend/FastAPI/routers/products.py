from fastapi import APIRouter

 # definimos el prefijo que va a ser / products, entonces cada vez que definamos "/" hace referencia a products, le damos contexto
router = APIRouter(prefix="/products", 
                   tags=["products"], # me agrupa los products en la documentacion, tenemos las apis divididas 
                   responses={404: {"message": "No encontrado"}}) #respuesta en el caso de que ocurra un error 404 con un mapeo {mensaje}


products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")      
async def products():
    return products_list

@router.get("/{id}")      
async def products(id: int):
    return products_list[id]

