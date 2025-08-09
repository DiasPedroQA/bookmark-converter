"""
Docstring para utils
"""

from .sistema_arquivos import (
    buscar_por_extensao,
    filtrar_apenas_arquivos,
    obter_datas_arquivo,
    obter_extensao_arquivo,
    obter_tamanho_arquivo,
    tem_permissao_leitura_arquivo,
)

from .sistema_operacional import (
    detectar_sistema,
    detectar_sistema_arquivos,
    filtrar_arquivos_e_pastas,
    listar_subcaminhos,
    obter_pasta_raiz_usuario,
    regex_caminho_sistema,
    tem_permissao_leitura,
    validar_caminho,
    verificar_caminho_so,
    verificar_permissoes,
)

from .sistema_pastas import (
    calcular_profundidade,
    filtrar_apenas_pastas,
    filtrar_arquivos,
    filtrar_pastas,
    listar_conteudo_detalhado,
    listar_pastas_vazias,
)

from .utils_comuns import (
    coletar_datas_aprimoradas,
    formatar_tamanho,
    normalizar_caminho,
)

__all__: list[str] = [
    "obter_tamanho_arquivo",
    "obter_extensao_arquivo",
    "obter_datas_arquivo",
    "tem_permissao_leitura_arquivo",
    "filtrar_apenas_arquivos",
    "buscar_por_extensao",
    "coletar_datas_aprimoradas",
    "detectar_sistema",
    "detectar_sistema_arquivos",
    "filtrar_arquivos_e_pastas",
    "listar_subcaminhos",
    "obter_pasta_raiz_usuario",
    "regex_caminho_sistema",
    "tem_permissao_leitura",
    "validar_caminho",
    "verificar_caminho_so",
    "verificar_permissoes",
    "normalizar_caminho",
    "coletar_datas_aprimoradas",
    "formatar_tamanho",
    "listar_subcaminhos",
    "filtrar_apenas_pastas",
    "filtrar_pastas",
    "filtrar_arquivos",
    "listar_pastas_vazias",
    "calcular_profundidade",
    "listar_conteudo_detalhado",
]
