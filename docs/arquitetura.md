# 🏗️ Arquitetura do Bookmark Converter

Este documento detalha a arquitetura do Bookmark Converter, explicando os principais componentes, padrões adotados e como tudo se conecta para garantir escalabilidade, manutenibilidade e qualidade.

---

## 📦 Visão Geral da Arquitetura

O Bookmark Converter foi projetado com foco em modularidade e clareza, usando boas práticas modernas em Python e integração com frontends. A arquitetura se divide em camadas bem definidas para facilitar o desenvolvimento, testes e expansão.

```bash
bookmark-converter/
├── src/
│   ├── core/
│   │   ├── models/         # Schemas Pydantic (validação e serialização)
│   │   └── converters/     # Lógica de conversão entre formatos (HTML ⇄ JSON)
│   └── interfaces/
│       ├── cli/            # CLI para interação via linha de comando
│       └── api/            # API REST construída com FastAPI
├── tests/                  # Testes unitários, de integração e end-to-end
├── docs/                   # Documentação técnica
├── .github/                # Automação (CI/CD, workflows, templates)
└── scripts/                # Scripts auxiliares para setup e deploy
```

---

## 🔑 Componentes Principais

### 1. Core

- **models/**  
  Define os modelos de dados usando Pydantic. Garante validação, coerência e conversão fácil entre formatos.

- **converters/**  
  Implementa a lógica de transformação entre arquivos HTML e JSON, usando BeautifulSoup para parsing HTML e métodos robustos para serialização JSON.

### 2. Interfaces

- **cli/**  
  Interface de linha de comando. Permite ao usuário executar comandos simples e diretos para exportar e importar bookmarks.

- **api/**  
  API REST construída com FastAPI. Expõe endpoints para operações CRUD e conversão via HTTP, com documentação automática via Swagger/OpenAPI.

### 3. Testes

- Testes unitários, integração e end-to-end para garantir qualidade e evitar regressões. Suportados por pytest e integrações com Codecov para monitoramento de cobertura.

### 4. Automação & CI/CD

- Workflows GitHub Actions para lint, testes, análise estática (bandit, pylint), cobertura de testes e alertas automáticos de falhas.

---

## ⚙️ Fluxo de Conversão

1. **Leitura do arquivo fonte** (HTML ou JSON)
2. **Parsing e validação** dos dados via modelos Pydantic
3. **Conversão interna** entre formatos (usando `converters/`)
4. **Geração do arquivo de saída** com formato correto
5. **Validação final** e report de erros

---

## 📐 Padrões e Boas Práticas

- **TDD (Test Driven Development):** Todo novo recurso vem acompanhado de testes.
- **CI/CD:** Pipeline automatizado garante qualidade contínua.
- **Modularidade:** Separação clara entre lógica de negócio e interfaces.
- **Documentação:** MkDocs para documentação técnica sempre atualizada.
- **Segurança:** Análise estática com Bandit para detectar vulnerabilidades.
- **Versionamento semântico:** Facilita controle de releases e compatibilidade.

---

## 🚀 Escalabilidade e Extensibilidade

- Suporte fácil para adicionar novos formatos (ex.: Markdown, XML).
- Estrutura para integrar interface GUI no futuro (Tkinter).
- API preparada para autenticação, cache e balanceamento.
- Código pronto para execução em containers Docker e ambientes cloud.

---

## 📖 Referências e Tecnologias

- **Python 3.12**
- **FastAPI** para backend e API REST
- **Pydantic** para schemas e validação
- **BeautifulSoup** para parsing HTML
- **pytest, Codecov** para testes e cobertura
- **GitHub Actions** para CI/CD
- **MkDocs** para documentação técnica

---

## 🔮 Considerações Finais

Este projeto é uma base sólida para manipulação e conversão de bookmarks, com arquitetura preparada para crescimento e adaptação. O foco é produtividade e qualidade, garantindo entregas rápidas sem perder o controle da qualidade.

---

Quer aprofundar mais? Explore os códigos na pasta `src/core` e os testes em `tests/` para entender o funcionamento detalhado.

---
