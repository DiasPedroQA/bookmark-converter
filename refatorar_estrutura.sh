#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Instalando dependências do projeto..."

python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

echo "🔧 Refatorando estrutura do projeto 'bookmark-converter'..."

# Diretórios base
ROOT_DIR="$(pwd)"
SRC_DIR="$ROOT_DIR/REBORN/src"
TESTS_DIR="$ROOT_DIR/REBORN/tests"

# Função para criar diretório se não existir
criar_diretorio() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
    echo "📁 Criado diretório: $1"
#   else
    # echo "ℹ️ Diretório já existe: $1"
  fi
}

# Função para criar arquivo se não existir
criar_arquivo() {
  if [ ! -f "$1" ]; then
    touch "$1"
    echo "📄 Criado arquivo: $1"
#   else
    # echo "ℹ️ Arquivo já existe: $1"
  fi
}

# Estrutura src (MVC)
for pasta in models views controllers routes utils; do
  criar_diretorio "$SRC_DIR/$pasta"
  criar_arquivo "$SRC_DIR/$pasta/__init__.py"
done
criar_arquivo "$SRC_DIR/__init__.py"

# Estrutura de testes (espelhando src)
for pasta in models views controllers routes utils; do
  criar_diretorio "$TESTS_DIR/unit/$pasta"
  criar_arquivo "$TESTS_DIR/unit/$pasta/__init__.py"
done
criar_diretorio "$TESTS_DIR/unit"
criar_arquivo "$TESTS_DIR/unit/__init__.py"
criar_diretorio "$TESTS_DIR/integration"
criar_arquivo "$TESTS_DIR/integration/__init__.py"
criar_arquivo "$TESTS_DIR/__init__.py"

# Scripts auxiliares
criar_diretorio "$ROOT_DIR/scripts"
criar_arquivo "$ROOT_DIR/scripts/__init__.py"

# Documentação
criar_diretorio "$ROOT_DIR/docs"
criar_arquivo "$ROOT_DIR/docs/index.md"

# Logs
criar_diretorio "$ROOT_DIR/.logs"

# VSCode
criar_diretorio "$ROOT_DIR/.vscode"

# GitHub
criar_diretorio "$ROOT_DIR/.github/workflows"
criar_diretorio "$ROOT_DIR/.github/ISSUE_TEMPLATE"
criar_arquivo "$ROOT_DIR/.github/ISSUE_TEMPLATE/bug_report.md"
criar_arquivo "$ROOT_DIR/.github/ISSUE_TEMPLATE/custom.md"
criar_arquivo "$ROOT_DIR/.github/ISSUE_TEMPLATE/feature_request.md"
criar_arquivo "$ROOT_DIR/.github/ISSUE_TEMPLATE/pipeline-failure.md"
criar_arquivo "$ROOT_DIR/.github/workflows/templates/shared-setup.yml"
criar_arquivo "$ROOT_DIR/.github/workflows/app_pipe.yml"
criar_arquivo "$ROOT_DIR/.github/dependabot.yml"

# Arquivos de configuração
for arquivo in \
  .gitignore .pre-commit-config.yaml .pylintrc .flake8 mypy.ini pytest.ini \
  pyproject.toml requirements.in requirements.txt requirements-dev.in \
  requirements-dev.txt Makefile README.md LICENSE mkdocs.yml coverage.xml \
  setup.cfg
do
  criar_arquivo "$ROOT_DIR/$arquivo"
done

echo "✅ Estrutura do projeto refatorada com sucesso!"
