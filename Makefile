# =====================================================
#                      VARIÁVEIS
# =====================================================
PROJECT_NAME := REBORN
VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
PIP_COMPILE := $(VENV_PATH)/bin/pip-compile
PYTEST := $(VENV_PATH)/bin/pytest
RUFF := $(VENV_PATH)/bin/ruff
ISORT := $(VENV_PATH)/bin/isort
BLACK := $(VENV_PATH)/bin/black

SRC := app
TESTS := tests
HOST := 127.0.0.1
PORT := 8000
APP_MODULE := $(SRC).main:app

# =====================================================
#                      AJUDA
# =====================================================
.PHONY: help
help:
	@echo "📘 Comandos disponíveis:"
	@echo "  make venv           - Criar ambiente virtual"
	@echo "  make install        - Instalar dependências"
	@echo "  make compile        - Gerar requirements*.txt com pip-compile"
	@echo "  make lint           - Verificar lint (ruff, isort)"
	@echo "  make format         - Formatar código (black, isort)"
	@echo "  make test           - Executar testes com pytest"
	@echo "  make coverage       - Gerar relatório cobertura (terminal + XML)"
	@echo "  make coverage-html  - Gerar relatório cobertura em HTML"
	@echo "  make tdd            - Pipeline TDD completa"
	@echo "  make run            - Executar API (uvicorn)"
	@echo "  make clean          - Limpar arquivos temporários"
	@echo "  make freeze         - Gerar freeze do ambiente atual"
	@echo "  make check-updates  - Listar pacotes desatualizados"
	@echo "  make pre-commit     - Rodar hooks pre-commit"
	@echo "  make ci             - Pipeline simplificada para CI/CD"

# =====================================================
#           AMBIENTE VIRTUAL E DEPENDÊNCIAS
# =====================================================
.PHONY: venv
venv:
	@echo "🛠️ Criando ambiente virtual em '$(VENV_PATH)'..."
	@python3 -m venv $(VENV_PATH)
	@echo "✅ Ambiente criado. Ative com:"
	@echo "   source $(VENV_PATH)/bin/activate"

.PHONY: install
install:
	@echo "🔧 Instalando dependências..."
	$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; fi

.PHONY: compile
compile:
	@$(PIP) install pip-tools
	@$(PIP_COMPILE) requirements.in --output-file=requirements.txt
	@$(PIP_COMPILE) requirements-dev.in --output-file=requirements-dev.txt

.PHONY: freeze
freeze:
	@$(PIP) freeze --all > requirements-lock.txt
	@echo "Freeze salvo em requirements-lock.txt"

.PHONY: check-updates
check-updates:
	@$(PIP) list --outdated

.PHONY: pre-commit
pre-commit:
	@pre-commit run --all-files

# =====================================================
#                  LINT E FORMATAÇÃO
# =====================================================
.PHONY: lint
lint:
	@$(RUFF) check .
	@$(ISORT) . --check-only --profile black

.PHONY: format
format:
	@$(BLACK) .
	@$(ISORT) . --profile black

# =====================================================
#                   TESTES E COBERTURA
# =====================================================
.PHONY: test
test:
	@PYTHONPATH=$(SRC) $(PYTEST) $(TESTS) --maxfail=1 --disable-warnings -v

.PHONY: coverage
coverage:
	@PYTHONPATH=$(SRC) $(PYTEST) --cov=$(SRC) $(TESTS) --cov-report=term-missing --cov-report=xml

.PHONY: coverage-html
coverage-html:
	@PYTHONPATH=$(SRC) $(PYTEST) --cov=$(SRC) $(TESTS) --cov-report=html

.PHONY: tdd
tdd: lint test coverage

# =====================================================
#                  EXECUÇÃO DA APLICAÇÃO
# =====================================================
.PHONY: run
run:
	@echo "🚀 Iniciando API..."
	@uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

.PHONY: setup

setup:
	@echo "🚀 Executando setup.py..."
	python3 scripts/setup.py

# =====================================================
#                    LIMPEZA
# =====================================================
.PHONY: clean
clean:
	@echo "🧹 Limpando arquivos temporários..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -delete
	@rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml .coverage *.egg-info dist build site

# =====================================================
#                      PIPELINE CI/CD
# =====================================================
.PHONY: ci
ci: lint test coverage
