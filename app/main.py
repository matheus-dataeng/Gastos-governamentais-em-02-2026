from fastapi import FastAPI
from app.routers.orgaos import router as orgaos_router
from app.routers.funcoes import router as funcoes_router
from app.routers.gastos import router as gastos_router


app = FastAPI()

@app.get("/")
def home():
    return{"message" : "API de Gastos governamentais"}

app.include_router(orgaos_router)
app.include_router(funcoes_router)
app.include_router(gastos_router)

