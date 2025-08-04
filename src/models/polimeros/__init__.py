### 📦 Arquivo: `__init__.py`

"""
monomeros
=========

Módulo de validações unitárias (monômeros) para atributos de itens
de sistemas de arquivos.

Cada classe Resultado* representa uma validação individual e isolada
de um campo (nome, caminho, tipo, permissões, datas etc.), com
estrutura padronizada:

- `valor_entrada`: valor recebido para validação
- `status`: indica sucesso ou falha
- `mensagem`: descrição do resultado

Este módulo não executa a validação de um item completo. Para isso,
utilize uma função agregadora que combine os monômeros conforme
necessário.

"""

from .monomeros import (
    ResultadoCaminhoAbsoluto,
    ResultadoDataAcesso,
    ResultadoDataCriacao,
    ResultadoDataModificacao,
    ResultadoIdentificador,
    ResultadoNome,
    ResultadoPastaMae,
    ResultadoPermissao,
    ResultadoTamanhoBytes,
    ResultadoTipoItem,
)

__all__: list[str] = [
    "ResultadoIdentificador",
    "ResultadoNome",
    "ResultadoPastaMae",
    "ResultadoCaminhoAbsoluto",
    "ResultadoTipoItem",
    "ResultadoTamanhoBytes",
    "ResultadoDataCriacao",
    "ResultadoDataModificacao",
    "ResultadoDataAcesso",
    "ResultadoPermissao",
]
