# 🏛️ Projeto: Gastos Governamentais

## 📌 Visão Geral

Este projeto implementa **um pipeline completo de ETL** para dados de gastos governamentais, com:

* Extração de dados de arquivos CSV.
* Transformações para limpeza, normalização e validação.
* Construção de dimensões e tabela fato (star schema).
* Carregamento em **PostgreSQL**.
* Exposição de dados via **API FastAPI**.

O objetivo é fornecer dados confiáveis e estruturados para análises e aplicações, com boas práticas de **logging**, **idempotência** e **modularidade**.

---

## 🛠️ Tecnologias

* **Python 3.11+** – Desenvolvimento pipeline e API.
* **Pandas** – Manipulação de dados.
* **Airflow 2.8+** – Orquestração pipelines.
* **PostgreSQL 13+** – Data warehouse.
* **FastAPI** – API para consulta de dados.
* **SQLAlchemy** – ORM e integração com PostgreSQL.
* **Docker & Docker Compose** – Ambiente isolado e reproduzível.

---


## 🚀 Como rodar o projeto

### 1️⃣ Configuração

cp .env.example .env.docker
# preencha as variáveis do banco, caminho do CSV e nomes das tabelas

### 2️⃣ Rodando com Docker

docker-compose --env-file .env.docker up -d


### 3️⃣ Inicializando Airflow

docker exec -it airflow-webserver /bin/bash
airflow db init
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com


### 4️⃣ Rodando a API localmente

cd app
uvicorn main:app --reload

* Endpoints:

  * `/orgaos` → Consulta tabela `dim_orgao`
  * `/funcoes` → Consulta tabela `dim_funcao`
  * `/gastos` → Consulta tabela fato `fato_gastos`

---

## 🔄 ETL - Pipeline Airflow

DAG: `gastos_governamentais`

Fluxo:

extract_task --> transform_task --> build_metrics_task --> load_task


### Etapas:

1. **Extract:** Leitura do CSV e carregamento inicial.

2. **Transform:**

   * Renomeação e padronização de colunas.
   * Conversão de valores financeiros.
   * Normalização de textos e validação de entidades federativas.
   * Validação de consistência financeira.

3. **Build Metrics:**

   * Criação das dimensões (`dim_orgao`, `dim_unidade_gestora`, `dim_funcao`, `dim_programa`, `dim_acao`, `dim_despesas`, `dim_localizacao`)
   * Construção da tabela fato `fato_gastos`.
4. **Load:**

   * Carregamento das tabelas no **PostgreSQL** com idempotência (remoção de registros existentes antes do append).

---

## 📈 Boas práticas adotadas

* Logging detalhado em todas as etapas.
* Pipelines idempotentes e rastreáveis.
* Modularidade (bronze → silver → gold) para evolução futura.
* Estrutura de Data Warehouse em star schema (dimensões + fato).
* API para acesso aos dados.

---

