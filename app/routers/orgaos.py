from fastapi import APIRouter
from sqlalchemy import text
from app.db.database import SessionLocal
import logging as log 

router = APIRouter()
logger = log.getLogger(__name__)

@router.get("/orgaos")
def get_orgaos():
    db = SessionLocal()
    
    try:
        query = text(
            '''
            SELECT * FROM dim_orgao
            LIMIT 100;
            
            '''        
        )
        result = db.execute(query)
        orgaos = result.mappings().all()
        
        logger.info("Consulta realizada na tabela dim_orgao")
        
        return orgaos
    
    except Exception as e:
        logger.error(f"Erro ao consultar tabela dim_orgao: {e}")
        return {"erro" : "Falha ao consultar dados"}
    
    finally:
        db.close()
    