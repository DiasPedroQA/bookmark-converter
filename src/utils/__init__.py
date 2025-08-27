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
#     global_method_buscar_filhos,
#     global_method_check_valid_path,
#     global_method_formatar_data,
#     global_method_formatar_infos_caminho,
#     global_method_formatar_tamanho_caminho,
#     global_method_infos_caminho,
#     global_method_obter_datas_caminho,
#     global_method_obter_id_caminho,
#     global_method_obter_nome_caminho,
#     global_method_obter_permissoes_caminho,
#     global_method_obter_tamanho_caminho,
# )
# from utils.system_tools import (
#     file_method_escrever_conteudo_texto,
#     file_method_gerar_slug,
#     file_method_ler_conteudo_texto,
#     folder_method_buscar_apenas_arquivos,
#     folder_method_buscar_apenas_pastas,
#     folder_method_buscar_arquivos_por_extensoes,
#     folder_method_buscar_arquivos_por_tamanho,
#     folder_method_buscar_filhos,
#     folder_method_buscar_por_nome,
#     folder_method_montar_arvore,
# )

# __all__: list[str] = [
#     "global_method_buscar_filhos",
#     "global_method_formatar_tamanho_caminho",
#     "global_method_obter_tamanho_caminho",
#     "global_method_obter_datas_caminho",
#     "global_method_obter_permissoes_caminho",
#     "file_method_gerar_slug",
#     "file_method_ler_conteudo_texto",
#     "file_method_escrever_conteudo_texto",
#     "folder_method_buscar_apenas_pastas",
#     "folder_method_buscar_apenas_arquivos",
#     "folder_method_buscar_filhos",
#     "folder_method_buscar_por_nome",
#     "folder_method_buscar_arquivos_por_extensoes",
#     "folder_method_buscar_arquivos_por_tamanho",
#     "folder_method_montar_arvore",
#     "global_method_obter_id_caminho",
#     "global_method_obter_nome_caminho",
#     "global_method_formatar_infos_caminho",
#     "global_method_infos_caminho",
#     "global_method_formatar_data",
#     "global_method_check_valid_path",
# ]
