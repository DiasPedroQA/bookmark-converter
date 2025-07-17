# Arquitetura do Projeto

## Camadas

- `app/`: camada de domínio e lógica da aplicação
- `views/`: camada de entrada (API, CLI, GUI)
- `tests/`: testes unitários, funcionais e e2e

## Fluxo

1. `views/api` inicia o FastAPI
2. `app/routes` define endpoints
3. `app/controllers` orquestra a lógica
4. `app/services` executa operações
5. `app/models` define os dados
