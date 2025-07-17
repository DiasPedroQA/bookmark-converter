<<<<<<< HEAD
# bookmark-converter
O Bookmark Converter é uma ferramenta de linha de comando e biblioteca modular em Python para converter arquivos de favoritos (bookmarks) entre diferentes navegadores de desktop. Compatível com formatos como HTML (padrão do Chrome/Firefox), JSON (Brave, Vivaldi) e outros. Ideal para backup, migração entre navegadores e análise de favoritos.
=======
# 📚 Bookmark Converter

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-yellow)
![Coverage](https://codecov.io/gh/SeuUsuario/bookmark-converter/branch/main/graph/badge.svg)

---

## ⚙️ Funcionalidades

- ✅ Leitura e parsing de arquivos HTML (ex.: exportados do Chrome ou Firefox)
- ✅ Conversão para JSON estruturado (ex.: Brave, Vivaldi)
- ✅ Interfaces:
  - CLI (linha de comando com subcomandos)
  - API REST (FastAPI + Swagger)
  - GUI (futuramente com Tkinter)
- ✅ Arquitetura modular com FastAPI, Pydantic e BeautifulSoup
- ✅ Pronto para TDD, CI, Docker e ambientes profissionais

---

## 🚀 Demonstração (CLI)

```bash
$ bookmark-converter exportar favoritos.html favoritos.json
✔ Exportado `favoritos.html` → `favoritos.json`

$ bookmark-converter importar favoritos.json favoritos.html
✔ Importado `favoritos.json` → `favoritos.html`

$ bookmark-converter --help
usage: bookmark-converter [subcommand] [options]

Positional arguments:
  subcommand
    exportar       Converte HTML → JSON
    importar       Converte JSON → HTML

Options:
  -h, --help       Exibe a ajuda
````

---

## 🛠️ Instalação

> **Pré-requisitos**: Python ≥ 3.10

### Clonando o repositório

```bash
git clone https://github.com/DiasPedroQA/bookmark-converter.git
cd bookmark-converter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Ou instale via `pip`

```bash
pip install bookmark-converter
```

### Rodar a API REST (FastAPI)

```bash
uvicorn src.interfaces.api.main_api:app --reload
# Acesse http://127.0.0.1:8000/docs
```

---

## 📂 Estrutura do Projeto

```text
bookmark-converter/
├── src/
│   ├── core/
│   │   ├── models/         # Schemas Pydantic
│   │   └── converters/     # Lógica de conversão entre formatos
│   └── interfaces/
│       ├── cli/            # Interface CLI
│       └── api/            # Interface REST
├── tests/                  # Testes automatizados (pytest)
├── .github/                # Actions, workflows e configs
├── Makefile                # Comandos: test, lint, format, run
├── requirements.in/.txt    # Gerência de dependências (pip-tools)
├── pyproject.toml          # Configurações de build, lint, format
├── .pre-commit-config.yaml # Hooks de qualidade de código
├── mkdocs.yml              # Documentação técnica com MkDocs
└── README.md               # Este arquivo
```

---

## ✅ Como contribuir

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nome`)
3. Adicione sua funcionalidade com testes
4. Rode os comandos de qualidade:

```bash
make test
make lint
make format
```

```text
Submeta um Pull Request com descrição clara e exemplos de uso
```

---

## 📌 Roadmap

- ✅ Conversão HTML ↔ JSON
- ☐ Suporte a novos formatos (Markdown, XML, Netscape Bookmark File)
- ☐ Interface gráfica com Tkinter
- ☐ Publicação no PyPI + automação CI/CD via GitHub Actions
- ☐ Suporte a leitura direta de favoritos do navegador

---

## 📖 Documentação

Acesse a documentação gerada com MkDocs (em construção):

```bash
mkdocs serve
# Acesse http://127.0.0.1:8000
```

---

## 📝 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais informações.

---

### ℹ️ Justificativas de Design

- Seções claras e organizadas para facilitar onboarding
- Exemplos de uso real e argumentos CLI para fácil compreensão
- Estrutura modular pronta para expansão
- Suporte total a testes, lint, formatação e documentação

---
>>>>>>> 9028aa7 (feat: add shared-setup workflow template for common CI steps)
