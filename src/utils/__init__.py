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

from utils.file_tools import read_text_content, write_text_content
from utils.folder_tools import (
    calculate_depth,
    filter_for_files,
    filter_for_folders,
    list_all_non_empty_children,
    list_empty_folders,
    search_by_extension,
)
from utils.main_tools import (
    get_dates_path,
    get_id_path,
    get_name_path,
    get_permissions_path,
    get_size_path,
    is_hidden_path,
    validate_path,
)

from .system_tools import (
    detect_filesystem,
    detect_system,
    get_user_root_folder,
    system_path_regex,
    validate_os_path,
)

__all__: list[str] = [
    "list_all_non_empty_children",
    "filter_for_folders",
    "filter_for_files",
    "list_empty_folders",
    "calculate_depth",
    "search_by_extension",
    "detect_system",
    "detect_filesystem",
    "get_user_root_folder",
    "get_dates_path",
    "get_id_path",
    "get_name_path",
    "get_permissions_path",
    "get_size_path",
    "system_path_regex",
    "validate_os_path",
    "read_text_content",
    "validate_path",
    "write_text_content",
    "is_hidden_path",
    "list_all_non_empty_children",
    "filter_for_files",
    "list_all_non_empty_children",
    "list_all_non_empty_children",
]
