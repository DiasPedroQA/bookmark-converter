# 📖 Documentação Oficial - Bookmark Converter

Bem-vindo à documentação oficial do **Bookmark Converter**! Aqui você encontrará tudo para usar, entender e contribuir com o projeto.

---

## 🔍 Visão Geral

O Bookmark Converter é uma ferramenta para conversão de arquivos de favoritos (bookmarks) entre HTML e JSON. Suporta múltiplas interfaces e possui arquitetura modular, pronta para expansão.

---

## 📚 Conteúdo da Documentação

- [Arquitetura](arquitetura.md)  
- [Contribuição](#-contribuição)  
- [Roadmap](#-roadmap)  
- [Licença](#-licença)  

---

## 🛠️ Instalação

> **Pré-requisitos**: Python ≥ 3.10

Clone o repositório:

```bash
git clone https://github.com/DiasPedroQA/bookmark-converter.git
cd bookmark-converter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
````

Ou instale via pip:

```bash
pip install bookmark-converter
```

---

## 🚀 Uso Básico

### CLI

Exportar HTML para JSON:

```bash
bookmark-converter exportar favoritos.html favoritos.json
```

Importar JSON para HTML:

```bash
bookmark-converter importar favoritos.json favoritos.html
```

Para ajuda:

```bash
bookmark-converter --help
```

### API REST

Executar servidor local:

```bash
uvicorn src.interfaces.api.main_api:app --reload
```

Acesse a documentação Swagger em:

```bash
http://127.0.0.1:8000/docs
```

---

## 🤝 Contribuição

Quer contribuir? Siga o guia no [README.md](../README.md#-como-contribuir).

---

## 📌 Roadmap

Veja as funcionalidades planejadas no [README.md](../README.md#-roadmap).

---

## 📝 Licença

Projeto distribuído sob a licença **MIT**. Veja [LICENSE](../LICENSE).

---
