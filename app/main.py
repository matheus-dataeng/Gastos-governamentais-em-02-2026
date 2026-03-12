from fastapi import FastAPI
from app.log import logger_setup
import logging as log 
from app.routers.orgaos import router as orgaos_router
from app.routers.funcoes import router as funcoes_router
from app.routers.gastos import router as gastos_router

logger_setup()
logger = log.getLogger(__name__)

app = FastAPI(
    title= "API de Gastos governamentais durante Fevereiro de 2026",
    description="API para consulta de gastos públicos tratados em pipeline de dados",
    version="1.0.0"
)

@app.get("/")
def home():
    logger.info()
    logger.info("Endpoit raiz")
    return{"message" : "API de Gastos governamentais"}

app.include_router(orgaos_router, tags= ["Orgãos"])
app.include_router(funcoes_router, tags=["Funções"])
app.include_router(gastos_router, tags=["Gastos"])

