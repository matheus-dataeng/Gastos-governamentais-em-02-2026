import pandas as pd
import logging as log

logger = log.getLogger(__name__)

def correcao_nomes_colunas(df: pd.DataFrame) -> pd.DataFrame:

    df = df[[
       "Código Órgão Superior",
        "Nome Órgão Superior",
        "Código Órgão Subordinado",
        "Nome Órgão Subordinado",
        "Código Unidade Gestora",
        "Nome Unidade Gestora",
        "Código Função",
        "Nome Função",
        "Código Subfução",
        "Nome Subfunção",
        "Código Programa Orçamentário",
        "Nome Programa Orçamentário",
        "Código Ação",
        "Nome Ação",
        "UF",
        "Município",
        "Nome Categoria Econômica",
        "Nome Grupo de Despesa",
        "Nome Elemento de Despesa",
        "Valor Empenhado (R$)",
        "Valor Liquidado (R$)",
        "Valor Pago (R$)" 
    ]]
    
    colunas_renomeadas = {
        "Código Órgão Superior" : "Codigo_orgao",
        "Nome Órgão Superior" : "Nome_orgao",
        "Código Órgão Subordinado" : "Codigo_subordinado",
        "Nome Órgão Subordinado" : "Nome_subordinado",
        "Código Unidade Gestora" : "Codigo_gestora",
        "Nome Unidade Gestora" : "Nome_gestora",
        "Código Função" : "Codigo_funcao",
        "Nome Função" : "Nome_funcao",
        "Código Subfução" : "Codigo_subfuncao",
        "Nome Subfunção" : "Nome_subfuncao",
        "Código Programa Orçamentário" : "Codigo_orcamentario",
        "Nome Programa Orçamentário" : "Nome_orcamentario",
        "Código Ação" : "Codigo_acao",
        "Nome Ação" : "Nome_acao",
        "Município" : "Municipio",
        "Nome Categoria Econômica" : "Nome_categoria",
        "Nome Grupo de Despesa" : "Nome_grupo_despesa",
        "Nome Elemento de Despesa" : "Nome_elemento_despesa",
        "Valor Empenhado (R$)" : "Valor_empenhado",
        "Valor Liquidado (R$)" : "Valor_liquidado",
        "Valor Pago (R$)"  : "Valor_pago"
    }
    
    df.columns = df.columns.str.strip()
    df.rename(columns= colunas_renomeadas, inplace= True)
    logger.info("Colunas selecionadas e renomeadas com sucesso / Colunas: %s, Linhas: %s", df.shape[1], len(df))
    return df

def convertendo_valores(df: pd.DataFrame) -> pd.DataFrame: 
    
    colunas_preco = ["Valor_empenhado", "Valor_liquidado",	"Valor_pago"]
    
    for col_preco in colunas_preco :
        df[col_preco] = (
            df[col_preco].str.replace(",", ".", regex=False).str.replace(",", "", regex= False).astype(float)
        )
        df[col_preco] = pd.to_numeric(df[col_preco], errors= "coerce")
    
    for col_preco_validacao in colunas_preco:
        precos_invalidos = int(df[col_preco_validacao].isna().sum())
        precos_zerados = int((df[col_preco_validacao] == 0).sum())
        
        if precos_invalidos:
            logger.warning("Preços invalidos: %s", precos_invalidos)
        
        if precos_zerados:
            logger.warning("Preços zerados: %s", precos_zerados)    
        
    return df

def normalizacao_dados(df: pd.DataFrame) -> pd.DataFrame:
    
    colunas = [
        "Nome_orgao", "Nome_subordinado", "Nome_gestora", "Nome_acao", 
        "Nome_categoria", "Nome_grupo_despesa", "Nome_elemento_despesa"
    ]
    
    entes_federativos = ["UF", "Municipio"]
    
    for col in colunas:
          df[col] = df[col].astype(str).str.title()
    
    for col_federativos in entes_federativos:
        colunas_invalidas = int(df[col_federativos].isna().sum())
        
        if colunas_invalidas:
            logger.warning("Entidades federativas invalidas: %s", colunas_invalidas)
        
        df["UF"] = df["UF"].str.upper()    
        df["UF"] = df["UF"].fillna("Nacional")
        df["Municipio"] = df["Municipio"].fillna("Nao informado")
    
    return df 

def validar_financeiro(df: pd.DataFrame) -> pd.DataFrame:
        
    erro_liquidado = (df["Valor_liquidado"] > df["Valor_empenhado"]).sum()
    erro_pago = (df["Valor_pago"] > df["Valor_liquidado"]).sum()
    
    if erro_liquidado:
        log.warning("Liquidação maior que desempenho: %s linhas", erro_liquidado)
    
    if erro_pago:
        log.warning("Pagamento maior que liquidação: %s linhas", erro_pago)
     
    return df 
    
def transform(**context) -> pd.DataFrame:
    ti = context["ti"]
    df = ti.xcom_pull(task_ids = "extract")
 
    logger.info("Iniciando Transformações")
    
    df = correcao_nomes_colunas(df)
    df = convertendo_valores(df)
    df = normalizacao_dados(df)
    df = validar_financeiro(df)
    
    logger.info("Transformações realizadas com sucesso / Colunas: %s, Linhas: %s", df.shape[1], len(df))
    
    return df 
    
    
    
    
    