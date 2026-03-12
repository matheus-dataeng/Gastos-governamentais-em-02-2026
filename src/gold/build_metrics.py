import pandas as pd 
import logging as log 

logger = log.getLogger(__name__)

def table_dim_orgao(df: pd.DataFrame) -> pd.DataFrame:
    dim_orgao = df[[
        "Codigo_orgao",
        "Nome_orgao",
        "Codigo_subordinado",
        "Nome_subordinado"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_orgao["Id_orgao"] = dim_orgao.index + 1
    
    dim_orgao = dim_orgao[[
    "Id_orgao",
    "Codigo_orgao",
    "Nome_orgao",
    "Codigo_subordinado",
    "Nome_subordinado"
    ]]
    
    logger.info("Dimensão orgãos / Colunas: %s, Linhas: %s", dim_orgao.shape[1], len(dim_orgao))
    return dim_orgao

def table_dim_unidade_gestora(df:pd.DataFrame) -> pd.DataFrame:
    dim_unidade_gestora = df[[
        "Codigo_gestora",
        "Nome_gestora"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_unidade_gestora["Id_unidade"] = dim_unidade_gestora.index + 1
    
    dim_unidade_gestora = dim_unidade_gestora[[
        "Id_unidade",
        "Codigo_gestora",
        "Nome_gestora"
    ]]
    
    logger.info("Dimensão unidade gestora / Colunas: %s, Linhas: %s", dim_unidade_gestora.shape[1], len(dim_unidade_gestora))
    return dim_unidade_gestora

def table_dim_funcao(df: pd.DataFrame) -> pd.DataFrame:
    dim_funcao = df[[
        "Codigo_funcao",
        "Nome_funcao",
        "Codigo_subfuncao",
        "Nome_subfuncao"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_funcao["Id_funcao"] = dim_funcao.index + 1

    dim_funcao = dim_funcao[[
        "Id_funcao",
        "Codigo_funcao",
        "Nome_funcao",
        "Codigo_subfuncao",
        "Nome_subfuncao"
    ]]

    logger.info("Dimensão função / Colunas: %s, Linhas: %s", dim_funcao.shape[1], len(dim_funcao))
    return dim_funcao

def table_dim_programa(df: pd.DataFrame) -> pd.DataFrame:
    dim_programa = df[[
        "Codigo_orcamentario",
        "Nome_orcamentario"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_programa["Id_programa"] = dim_programa.index + 1
    
    dim_programa = dim_programa[[
        "Id_programa",
        "Codigo_orcamentario",
        "Nome_orcamentario"
    ]]
    
    logger.info("Dimensão programa / Colunas: %s, Linhas: %s", dim_programa.shape[1], len(dim_programa))
    return dim_programa

def table_dim_acao(df: pd.DataFrame) -> pd.DataFrame:
    dim_acao = df[[
        "Codigo_acao",
        "Nome_acao"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_acao["Id_acao"] = dim_acao.index +1
    
    dim_acao = dim_acao[[
        "Id_acao",
        "Codigo_acao",
        "Nome_acao"
    ]]

    logger.info("Dimensão ação / Colunas: %s, Linhas: %s", dim_acao.shape[1], len(dim_acao))
    return dim_acao
    
def table_dim_despesas(df: pd.DataFrame) -> pd.DataFrame:
    dim_despesas = df[[
        "Nome_categoria",
        "Nome_grupo_despesa",
        "Nome_elemento_despesa"
    ]].drop_duplicates().reset_index(drop= True)
    
    dim_despesas["Id_despesas"] = dim_despesas.index + 1
    
    dim_despesas = dim_despesas[[
        "Id_despesas",
        "Nome_categoria",
        "Nome_grupo_despesa",
        "Nome_elemento_despesa"
    ]]
    
    logger.info("Dimensão despesa / Colunas: %s, Linhas: %s", dim_despesas.shape[1], len(dim_despesas))
    return dim_despesas
    
def table_dim_localizacao(df: pd.DataFrame) -> pd.DataFrame:
    dim_localizacao = df[[
        "Municipio",
        "UF"
    ]].drop_duplicates().reset_index(drop= True)

    dim_localizacao["Id_localizacao"] = dim_localizacao.index + 1
    
    dim_localizacao = dim_localizacao[[
        "Id_localizacao",
        "Municipio",
        "UF"
    ]]
    
    logger.info("Dimensão despesa / Colunas: %s, Linhas: %s", dim_localizacao.shape[1], len(dim_localizacao))
    return dim_localizacao

def table_fato(
    df: pd.DataFrame,
    dim_orgao: pd.DataFrame,
    dim_unidade_gestora: pd.DataFrame,
    dim_funcao: pd.DataFrame,
    dim_programa: pd.DataFrame,
    dim_acao: pd.DataFrame,
    dim_despesas: pd.DataFrame,
    dim_localizacao: pd.DataFrame
) -> pd.DataFrame:

    fato = df.merge(
        dim_orgao,
        on=["Codigo_orgao","Nome_orgao","Codigo_subordinado","Nome_subordinado"],
        how="left"
    )

    fato = fato.merge(
        dim_unidade_gestora,
        on=["Codigo_gestora","Nome_gestora"],
        how="left"
    )

    fato = fato.merge(
        dim_funcao,
        on=["Codigo_funcao","Nome_funcao","Codigo_subfuncao","Nome_subfuncao"],
        how="left"
    )

    fato = fato.merge(
        dim_programa,
        on=["Codigo_orcamentario","Nome_orcamentario"],
        how="left"
    )

    fato = fato.merge(
        dim_acao,
        on=["Codigo_acao","Nome_acao"],
        how="left"
    )

    fato = fato.merge(
        dim_despesas,
        on=["Nome_categoria","Nome_grupo_despesa","Nome_elemento_despesa"],
        how="left"
    )

    fato = fato.merge(
        dim_localizacao,
        on=["Municipio","UF"],
        how="left"
    )

    fato_gastos = fato[[
        "Id_orgao",
        "Id_unidade",
        "Id_funcao",
        "Id_programa",
        "Id_acao",
        "Id_despesas",
        "Id_localizacao",
        "Valor_empenhado",
        "Valor_liquidado",
        "Valor_pago"
    ]]

    logger.info("Tabela fato_gastos / Colunas: %s, Linhas: %s",fato_gastos.shape[1], len(fato_gastos))
    return fato_gastos

def build_metrics(**context) -> pd.DataFrame:
    ti = context["ti"]
    df = ti.xcom_pull(task_ids = "transform")
    
    logger.info("Construindo dimensão orgão")
    dim_orgao = table_dim_orgao(df)
    
    logger.info("Construindo dimensão unidade_gestora")
    dim_unidade_gestora = table_dim_unidade_gestora(df)
    
    logger.info("Construinda dimensão função")
    dim_funcao = table_dim_funcao(df)
    
    logger.info("Construindo dimensão programa")
    dim_programa = table_dim_programa(df)
    
    logger.info("Construindo dimensão ação")
    dim_acao = table_dim_acao(df)
    
    logger.info("Construindo dimensão despesas")
    dim_despesas = table_dim_despesas(df)
    
    logger.info("Construindo dimensão localização")
    dim_localizacao = table_dim_localizacao(df)
    
    logger.info("Construindo tabela fato")
    fato = table_fato(
        df,
        dim_orgao,
        dim_unidade_gestora,
        dim_funcao,
        dim_programa,
        dim_acao,
        dim_despesas,
        dim_localizacao
    )
    
    return {
        "dim_orgao" : dim_orgao,
        "dim_unidade_gestora" : dim_unidade_gestora,
        "dim_funcao" : dim_funcao,
        "dim_programa" : dim_programa,
        "dim_acao" : dim_acao,
        "dim_despesas" : dim_despesas,
        "dim_localizacao" : dim_localizacao,
        "fato_gastos" : fato 
    }




