# 📚 Bookmark Converter

Ferramenta modular para converter bookmarks entre HTML e JSON, com suporte a CLI, API REST (FastAPI) e futura GUI.  
Focada em TDD, CI/CD e ambientes profissionais.

[![Coverage](https://codecov.io/gh/DiasPedroQA/bookmark-converter/branch/main/graph/badge.svg?flag=backend)](https://codecov.io/gh/DiasPedroQA/bookmark-converter)
[![Coverage](https://codecov.io/gh/DiasPedroQA/bookmark-converter/branch/main/graph/badge.svg?flag=frontend)](https://codecov.io/gh/DiasPedroQA/bookmark-converter)
[![Coverage](https://codecov.io/gh/DiasPedroQA/bookmark-converter/branch/main/graph/badge.svg?flag=integration)](https://codecov.io/gh/DiasPedroQA/bookmark-converter)

---

## ⚙️ Funcionalidades

- Leitura e parsing de bookmarks em HTML (Chrome, Firefox)
- Conversão para JSON estruturado (ex.: Brave, Vivaldi)
- Interfaces:
  - CLI com subcomandos intuitivos
  - API REST com FastAPI + Swagger
  - GUI planejada com Tkinter
- Arquitetura modular e escalável
- Pronto para TDD, CI/CD, Docker e ambientes profissionais

---

## 🚀 Uso rápido (CLI)

```bash
# Exporta HTML → JSON
bookmark-converter exportar favoritos.html favoritos.json

# Importa JSON → HTML
bookmark-converter importar favoritos.json favoritos.html

# Ajuda geral
bookmark-converter --help
````

---

## 🛠️ Instalação

### Clone + virtualenv + dependências

```bash
git clone https://github.com/DiasPedroQA/bookmark-converter.git
cd bookmark-converter
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### Ou via pip (se publicado)

```bash
pip install bookmark-converter
```

### Rodar API REST (FastAPI)

```bash
uvicorn src.interfaces.api.main_api:app --reload
# Acesse: http://127.0.0.1:8000/docs
```

---

## 📂 Estrutura do projeto

```text
bookmark-converter/
├── src/
│   ├── core/             # Models e lógica de conversão
│   └── interfaces/       # CLI, API REST, GUI futura
├── tests/                # Testes (pytest)
├── .github/              # Workflows, templates, ações
├── Makefile              # Comandos úteis (test, lint, run)
├── requirements*.txt     # Dependências
├── pyproject.toml        # Configs de build e lint
└── README.md             # Documentação principal
```

---

## ✅ Como contribuir

1. Faça fork e branch (`feature/nome`)
2. Implemente com testes
3. Rode qualidade e testes:

```bash
make lint
make test
make format
```

## Abra Pull Request com descrição clara e exemplos

---

## 📌 Roadmap

- ✅ Conversão HTML ↔ JSON
- ☐ GUI Tkinter
- ☐ Publicação PyPI + CI/CD completo
- ☐ Leitura direta dos bookmarks do navegador
- ☐ Suporte a novos formatos (Markdown, XML, Netscape)

---

## 📖 Documentação

Gerada com MkDocs (em construção):

```bash
mkdocs serve
# Acesse http://127.0.0.1:8000
```

---

## 📝 Licença

MIT — veja [LICENSE](LICENSE)

---
