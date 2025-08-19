"""
Módulo utilitário de acesso unificado às funções de manipulação
de arquivos, pastas e sistema operacional.

Este módulo agrega funções importadas de outros submódulos
(`file_tools`, `folder_tools`, `global_tools` e `system_tools`)
em um único ponto de acesso, facilitando a importação e a
organização do código.

Funcionalidades abrangem:
- Manipulação de arquivos e pastas
- Leitura e escrita de conteúdo
- Filtragem e busca por critérios
- Validação e análise de caminhos
- Detecção e informações sobre o sistema operacional
"""

# from utils.global_tools import (
#     file_method_buscar_arquivos_por_extensoes,
#     file_method_buscar_arquivos_por_tamanho,
#     file_method_buscar_por_extensoes,
#     file_method_escrever_conteudo_texto,
#     file_method_formatar_data,
#     file_method_gerar_slug,
#     file_method_ler_conteudo_texto,
#     folder_method_calcular_profundidade,
#     folder_method_contar_filhos,
#     folder_method_buscar_apenas_arquivos,
#     folder_method_buscar_apenas_pastas,
#     global_method_buscar_filhos,
#     folder_method_buscar_pastas_visiveis,
#     folder_method_resumir_pasta,
#     folder_method_visualizacao_arvore,
#     global_method_debug_print,
#     global_method_formatar_tamanho_caminho,
#     global_method_obter_datas_caminho,
#     global_method_obter_id_caminho,
#     global_method_obter_nome_caminho,
#     global_method_obter_permissoes_caminho,
#     global_method_obter_tamanho_caminho,
#     global_method_check_valid_path,
#     system_method_obter_caminho_usuario,
#     system_method_obter_endereco_ip,
#     system_method_obter_espaco_disco_livre,
#     system_method_obter_nome_sistema_operacional,
# )

# __all__: list[str] = [
#     "file_method_buscar_arquivos_por_extensoes",
#     "file_method_buscar_por_extensoes",
#     "file_method_escrever_conteudo_texto",
#     "file_method_buscar_arquivos_por_tamanho",
#     "file_method_formatar_data",
#     "file_method_gerar_slug",
#     "file_method_ler_conteudo_texto",
#     "folder_method_calcular_profundidade",
#     "folder_method_contar_filhos",
#     "folder_method_buscar_apenas_arquivos",
#     "folder_method_buscar_apenas_pastas",
#     "folder_method_buscar_pastas_visiveis",
#     "global_method_buscar_filhos",
#     "folder_method_resumir_pasta",
#     "folder_method_visualizacao_arvore",
#     "global_method_formatar_tamanho_caminho",
#     "global_method_debug_print",
#     "global_method_obter_datas_caminho",
#     "global_method_obter_id_caminho",
#     "global_method_obter_nome_caminho",
#     "global_method_obter_permissoes_caminho",
#     "global_method_obter_tamanho_caminho",
#     "global_method_check_valid_path",
#     "system_method_obter_caminho_usuario",
#     "system_method_obter_endereco_ip",
#     "system_method_obter_espaco_disco_livre",
#     "system_method_obter_nome_sistema_operacional",
#     "global_method_buscar_filhos",
#     "global_method_formatar_tamanho_caminho",
# ]
