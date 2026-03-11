# Nome do ambiente virtual
VENV_NAME=gov-env

# Caminho para o executável do Python dentro do ambiente virtual
PYTHON=$(VENV_NAME)/bin/python

# Caminho para o executável do pip dentro do ambiente virtual
PIP=$(VENV_NAME)/bin/pip

# Cria o ambiente virtual Python
venv:
	python3 -m venv $(VENV_NAME)

# Instala as dependências listadas no requirements.txt
install:
	$(PIP) install -r requirements.txt


# Atualiza o requirements.txt com as dependências atualmente instaladas
freeze:
	$(PIP) freeze > requirements.txt


# Executa o pipeline de dados (ex: geração de métricas na camada gold)
pipeline:
	$(PYTHON) src/gold/build_metrics.py


# Inicia a API localmente usando Uvicorn com hot reload
run:
	uvicorn app.main:app --reload

# Executa os testes do projeto usando pytest
test:
	PYTHONPATH=. pytest -v

# Faz o build da aplicação para deploy usando AWS SAM
build:
	sam build

# Faz o deploy da aplicação na AWS Lambda usando SAM
deploy:
	sam deploy

# Executa a API localmente simulando o ambiente AWS Lambda
local:
	sam local start-api

# Remove arquivos temporários do Python (__pycache__ e .pyc)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Rodar serviço da api
run-api:
	uvicorn app.main:app --reload --port 8001