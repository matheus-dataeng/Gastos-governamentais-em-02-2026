from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
import os
import logging as log 
from dotenv import load_dotenv

logger = log.getLogger(__name__)
load_dotenv()

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
dbname = os.getenv("PG_DBNAME")

if not all([user, password, host, port, dbname]):
    logger.info("Variáveis não definidas no .env")
    raise ValueError("Variáveis de ambiente no banco não configuradas")

try:
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
    logger.info("Conexão bem sucedida")
    
except Exception as e:
    logger.error(f"Erro na conexão: {e}")
    raise

