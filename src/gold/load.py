import pandas as pd 
import os 
import logging as log 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

logger = log.getLogger(__name__)
load_dotenv()

def load(**context) -> None:
    ti = context["ti"]
    df = ti.xcom_pull(task_ids = "build_metrics")
    
    dim_orgao = pd.DataFrame(df["dim_orgao"])
    dim_unidade_gestora = pd.DataFrame(df["dim_unidade_gestora"])
    dim_funcao = pd.DataFrame(df["dim_funcao"])
    dim_programa = pd.DataFrame(df["dim_programa"])
    dim_acao = pd.DataFrame(df["dim_acao"])
    dim_despesas = pd.DataFrame(df["dim_despesas"])
    dim_localizacao = pd.DataFrame(df["dim_localizacao"])
    fato = pd.DataFrame(df["fato_gastos"])

    logger.info("Iniciando carga no Data Warehouse")

    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT")
    dbname = os.getenv("PG_DBNAME")
    
    if not all([user, password, host, port, dbname]):
        logger.error("Variaveis não definidas no .env")
        raise ValueError("Variaveis de conexão não definidas")
    
    try:
        url_banco = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        engine = create_engine(url_banco)
        
        table_fato = os.getenv("TABLE_FATO")
        table_dim_orgao = os.getenv("TABLE_DIM_ORGAO")
        table_dim_unidade_gestora = os.getenv("TABLE_DIM_UNIDADE_GESTORA")
        table_dim_funcao = os.getenv("TABLE_DIM_FUNCAO")
        table_dim_programa = os.getenv("TABLE_DIM_PROGRAMA")
        table_dim_acao = os.getenv("TABLE_DIM_ACAO")
        table_dim_despesas = os.getenv("TABLE_DIM_DESPESAS")
        table_dim_localizacao = os.getenv("TABLE_DIM_LOCALIZACAO")
        
        if not all([
            table_fato, table_dim_orgao, table_dim_unidade_gestora, table_dim_funcao, table_dim_programa, 
            table_dim_acao, table_dim_despesas,table_dim_localizacao
        ]):
            logger.error("Variaveis não definidas no env.")
            raise ValueError("Variaveis não definidas")

        
        id_fato = fato["Id_orgao"].dropna().astype(int).unique().tolist()
        id_dim_orgao = dim_orgao["Id_orgao"].dropna().astype(int).unique().tolist()
        id_dim_unidade_gestora = dim_unidade_gestora["Id_unidade"].dropna().astype(int).unique().tolist()
        id_dim_funcao = dim_funcao["Id_funcao"].dropna().astype(int).unique().tolist()
        id_dim_programa = dim_programa["Id_programa"].dropna().astype(int).unique().tolist()
        id_dim_acao = dim_acao["Id_acao"].dropna().astype(int).unique().tolist()
        id_dim_despesas = dim_despesas["Id_despesas"].dropna().astype(int).unique().tolist()
        id_dim_localizacao = dim_localizacao["Id_localizacao"].dropna().astype(int).unique().tolist()
        
        
        with engine.begin() as conn:
            
            tables = [
                (table_fato, "Id_orgao", id_fato),
                (table_dim_orgao, "Id_orgao", id_dim_orgao),
                (table_dim_unidade_gestora, "Id_unidade", id_dim_unidade_gestora),
                (table_dim_funcao, "Id_funcao", id_dim_funcao),
                (table_dim_programa, "Id_programa", id_dim_programa),
                (table_dim_acao, "Id_acao", id_dim_acao),
                (table_dim_despesas, "Id_despesas", id_dim_despesas),
                (table_dim_localizacao, "Id_localizacao", id_dim_localizacao),
                
                ]
            
            for tabelas, colunas, ids in tables:
                if ids:
                    result = conn.execute(
                        text(f'DELETE FROM {tabelas} WHERE "{colunas}" = ANY (:id)'),
                        {"id" : ids}
                    )
                    logger.info("Registros removidos da tabela %s: %s", tabelas, result.rowcount)

            dfs = [
                (dim_orgao, table_dim_orgao),
                (dim_unidade_gestora, table_dim_unidade_gestora),
                (dim_funcao, table_dim_funcao),
                (dim_programa, table_dim_programa),
                (dim_acao, table_dim_acao),
                (dim_despesas, table_dim_despesas),
                (dim_localizacao, table_dim_localizacao),
                (fato, table_fato)
            ]   
            
            for df, tabela in dfs:
                df.to_sql(con= conn, name= tabela, chunksize= 1000, index= False, if_exists= "append")
                logger.info("Tabela %s carregada com sucesso / Colunas: %s, Linhas:%s", tabela, df.shape[1], len(df))
                
    except Exception as e:
        logger.error(f"Erro no carregamento: {e}")
        raise 
            


