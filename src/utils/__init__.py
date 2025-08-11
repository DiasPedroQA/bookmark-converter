"""
Módulo utilitário de acesso unificado às funções de manipulação
de arquivos, pastas e sistema operacional.

Este módulo agrega funções importadas de outros submódulos
(`file_tools`, `folder_tools`, `main_tools` e `system_tools`)
em um único ponto de acesso, facilitando a importação e a
organização do código.

Funcionalidades abrangem:
- Manipulação de arquivos e pastas
- Leitura e escrita de conteúdo
- Filtragem e busca por critérios
- Validação e análise de caminhos
- Detecção e informações sobre o sistema operacional
"""

from src.utils.file_tools import escrever_conteudo_texto, ler_conteudo_texto
from src.utils.folder_tools import (
    buscar_por_extensao,
    calcular_profundidade,
    filtrar_arquivos,
    filtrar_pastas,
    listar_pastas_vazias,
    listar_subcaminhos,
)
from src.utils.main_tools import (
    get_caminho_relativo,
    get_datas,
    get_id,
    get_montagem_origem,
    get_nome,
    get_permissoes,
    is_hidden_path,
    obter_tamanho,
    validar_caminho,
)

from .system_tools import (
    detectar_sistema,
    detectar_sistema_arquivos,
    obter_pasta_raiz_usuario,
    regex_caminho_sistema,
    verificar_caminho_so,
)

__all__: list[str] = [
    "buscar_por_extensao",
    "calcular_profundidade",
    "detectar_sistema",
    "detectar_sistema_arquivos",
    "escrever_conteudo_texto",
    "filtrar_arquivos",
    "filtrar_pastas",
    "get_caminho_relativo",
    "get_datas",
    "get_id",
    "get_montagem_origem",
    "get_nome",
    "get_permissoes",
    "ler_conteudo_texto",
    "listar_pastas_vazias",
    "listar_subcaminhos",
    "obter_pasta_raiz_usuario",
    "obter_tamanho",
    "regex_caminho_sistema",
    "validar_caminho",
    "verificar_caminho_so",
    "is_hidden_path",
]
