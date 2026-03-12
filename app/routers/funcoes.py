from sqlalchemy import text
import logging as log 
from app.db.database import SessionLocal
from fastapi import APIRouter

router = APIRouter()
logger = log.getLogger(__name__)

@router.get("/funcoes")
def get_funcoes():
    db = SessionLocal()
    
    try:
        query = text(
            '''
            SELECT * FROM dim_funcao
            LIMIT 100;  
            '''   
        )
        result = db.execute(query)
        funcoes = result.mappings().all()
        
        logger.info("Consulta da tabela dim_funcao realizada")
        
        return funcoes
    
    except Exception as e:
        logger.error(f"Erro ao consultar dim_funcoes: {e}")
        return {"erro" : "Falha ao consultar os dados"}
    
    finally:
        db.close()
    