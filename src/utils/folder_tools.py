"""
folder_tools.py
---------------------
Funções utilitárias para manipulação e análise de diretórios.

Objetivos:
- Listar conteúdo de pastas com filtros.
- Calcular profundidade e encontrar pastas vazias.
- Buscar arquivos por extensão.

Depende de utils_common para:
- Validação de caminho
- Detecção de ocultos
"""

from collections.abc import Iterator
from pathlib import Path

from utils.main_tools import is_hidden_path, validate_path

# ---------------------
# Funções privadas
# ---------------------


def _safe_iterdir(directory: Path, ignore_hidden: bool) -> Iterator[Path]:
    """
    Itera sobre itens de diretório, ignorando ocultos se pedido e tratando
    exceções de permissão.

    Retorna um iterador para evitar carregar tudo na memória logo de cara.
    """
    try:
        for item in directory.iterdir():
            if ignore_hidden and is_hidden_path(path_neutral=item):
                continue
            yield item
    except PermissionError:
        pass  # não faz nada, termina a iteração silenciosamente


# ---------------------
# Funções públicas
# ---------------------


def filter_for_folders(items: list[Path]) -> list[Path]:
    """Retorna apenas diretórios."""
    return [item for item in items if item.is_dir()]


def filter_for_files(items: list[Path]) -> list[Path]:
    """Retorna apenas arquivos."""
    return [item for item in items if item.is_file()]


def list_all_non_empty_children(
    base_folder: str | Path, ignore_hidden: bool = True
) -> list[Path]:
    """
    Lista arquivos e pastas não vazias dentro do diretório base.

    Pastas vazias são excluídas da lista. Itens ocultos são ignorados se
    ignore_hidden=True.
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return []

    children: list[Path] = []
    for item in _safe_iterdir(directory=base_folder, ignore_hidden=ignore_hidden):
        if item.is_dir():
            try:
                # Usar next() para verificar se existe pelo menos 1 item
                # Evita carregar toda lista na memória
                if next(_safe_iterdir(directory=item, ignore_hidden=ignore_hidden), None) is not None:
                    children.append(item)
            except PermissionError:
                # Ignora pastas inacessíveis
                continue
        else:
            children.append(item)

    return children


def list_empty_folders(base_folder: str | Path, ignore_hidden: bool = True) -> list[Path]:
    """
    Lista pastas vazias dentro do diretório base.

    Pastas que não possuem nenhum item (excluindo ocultos se ignore_hidden=True).
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return []

    empty_folders: list[Path] = []
    for folder in filter_for_folders(items=list_all_non_empty_children(base_folder=base_folder, ignore_hidden=False)):
        try:
            # Verifica se pasta está vazia, ignorando ocultos conforme flag
            if next(_safe_iterdir(directory=folder, ignore_hidden=ignore_hidden), None) is None:
                empty_folders.append(folder)
        except PermissionError:
            continue

    return empty_folders


def calculate_depth(base_folder: str | Path) -> int:
    """
    Calcula a profundidade máxima da árvore de diretórios.

    Retorna 0 se o caminho não for uma pasta válida.
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return 0

    base_parts: int = len(base_folder.parts)
    max_depth = 0

    try:
        for path in base_folder.rglob("*"):
            if path.is_dir():
                depth: int = len(path.parts) - base_parts
                if depth > max_depth:
                    max_depth: int = depth
    except PermissionError:
        pass

    return max_depth


def search_by_extension(base_folder: str | Path, extension: str) -> list[Path]:
    """
    Busca arquivos na pasta base que terminam com a extensão especificada.

    Suporta extensões compostas (ex: '.tar.gz') e ignora case.
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return []

    ext_parts: list[str] = extension.lower().lstrip(".").split(".")
    results: list[Path] = []

    try:
        for file in base_folder.iterdir():
            if file.is_file():
                suffixes: list[str] = [s.lstrip(".").lower() for s in file.suffixes]
                if suffixes[-len(ext_parts):] == ext_parts:
                    results.append(file)
    except PermissionError:
        pass

    return results
