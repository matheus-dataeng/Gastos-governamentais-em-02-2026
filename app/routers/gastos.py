import logging as log
from app.database import SessionLocal
from fastapi import APIRouter
from sqlalchemy import text 


router = APIRouter()
logger = log.getLogger(__name__)

@router.get("/gastos")
def get_gastos():
    db = SessionLocal()
    
    try:
        query = text(
            '''
            SELECT
                org."Nome_orgao",
                func."Nome_funcao",
                fat."Valor_pago"
            FROM fato_gastos AS fat
            JOIN dim_orgao AS org
                ON fat."Id_orgao" = org."Id_orgao" 
            JOIN dim_funcao AS func
                ON fat."Id_funcao" = func."Id_funcao"

            LIMIT 100;       
            '''    
        )
        
        result = db.execute(query)
        gastos = result.mappings().all()
        
        logger.info("Consulta aos gastos realizados com sucesso")
        return gastos
    
    except Exception as e:
        log.error(f"Erro ao consultar os dados: {e}")
        return{"erro" : "Falha ao consultar os dados"}
    
    finally:
        db.close()