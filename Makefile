.PHONY: help install seed test up down logs status clean

# Detecção dinâmica entre Docker e Podman
DOCKER_BIN := $(shell which docker 2>/dev/null)
PODMAN_BIN := $(shell which podman 2>/dev/null)

ifneq ($(DOCKER_BIN),)
    COMPOSE ?= docker compose
else ifneq ($(PODMAN_BIN),)
    COMPOSE ?= podman compose
else
    COMPOSE ?= docker compose
endif

PYTHON ?= $(shell test -f .venv/bin/python && echo .venv/bin/python || which python3 || echo python)

help:
	@echo "Comandos disponíveis (Container Engine detectado: $(COMPOSE)):"
	@echo "  make install  - Instala dependências Python locais"
	@echo "  make seed     - Gera dados sintéticos e arquivos parquet de seed"
	@echo "  make test     - Executa o parser semântico e inicialização do DuckDB localmente"
	@echo "  make up       - Inicia a stack de containers (MinIO, Polaris, llama.cpp, Agent, Open WebUI)"
	@echo "  make down     - Para a stack de containers"
	@echo "  make status   - Verifica status dos containers"
	@echo "  make clean    - Remove arquivos temporários e cache"

install:
	pip install -r requirements.txt

seed:
	$(PYTHON) -m data.seed.seed_iceberg

test:
	$(PYTHON) -m semantic.parser
	$(PYTHON) -m core.engine

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

status:
	$(COMPOSE) ps

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -f data/seed/*.parquet
