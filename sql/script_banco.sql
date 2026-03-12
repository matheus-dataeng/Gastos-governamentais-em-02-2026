-- CRIAÇÃO DAS TABELAS NO BANCO

CREATE TABLE "dim_orgao" (
    "Id_orgao" SERIAL PRIMARY KEY,
    "Codigo_orgao" TEXT,
    "Nome_orgao" TEXT,
    "Codigo_subordinado" TEXT,
    "Nome_subordinado" TEXT
);

CREATE TABLE "dim_unidade_gestora" (
    "Id_unidade" SERIAL PRIMARY KEY,
    "Codigo_gestora" TEXT,
    "Nome_gestora" TEXT
);

CREATE TABLE "dim_funcao" (
    "Id_funcao" SERIAL PRIMARY KEY,
    "Codigo_funcao" TEXT,
    "Nome_funcao" TEXT,
    "Codigo_subfuncao" TEXT,
    "Nome_subfuncao" TEXT
);

CREATE TABLE "dim_programa" (
    "Id_programa" SERIAL PRIMARY KEY,
    "Codigo_orcamentario" TEXT,
    "Nome_orcamentario" TEXT
);

CREATE TABLE "dim_acao" (
    "Id_acao" SERIAL PRIMARY KEY,
    "Codigo_acao" TEXT,
    "Nome_acao" TEXT
);

CREATE TABLE "dim_despesas" (
    "Id_despesas" SERIAL PRIMARY KEY,
    "Nome_categoria" TEXT,
    "Nome_grupo_despesa" TEXT,
    "Nome_elemento_despesa" TEXT
);

CREATE TABLE "dim_localizacao" (
    "Id_localizacao" SERIAL PRIMARY KEY,
    "Municipio" TEXT,
    "UF" TEXT
);


CREATE TABLE "fato_gastos" (
    "Id_orgao" INTEGER REFERENCES "dim_orgao"("Id_orgao"),
    "Id_unidade" INTEGER REFERENCES "dim_unidade_gestora"("Id_unidade"),
    "Id_funcao" INTEGER REFERENCES "dim_funcao"("Id_funcao"),
    "Id_programa" INTEGER REFERENCES "dim_programa"("Id_programa"),
    "Id_acao" INTEGER REFERENCES "dim_acao"("Id_acao"),
    "Id_despesas" INTEGER REFERENCES "dim_despesas"("Id_despesas"),
    "Id_localizacao" INTEGER REFERENCES "dim_localizacao"("Id_localizacao"),
    "Valor_empenhado" NUMERIC,
    "Valor_liquidado" NUMERIC,
    "Valor_pago" NUMERIC
);
