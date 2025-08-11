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

from pathlib import Path

from src.utils.main_tools import is_hidden_path, validate_path

PathLike = str | Path

# ---------------------
# Funções privadas
# ---------------------


def _safe_iterdir(directory: Path, ignore_hidden: bool) -> list[Path]:
    """Itera sobre itens de diretório, ignorando ocultos se pedido, tratando exceções."""
    try:
        return [item for item in directory.iterdir() if not (ignore_hidden and is_hidden_path(path_neutral=item))]
    except PermissionError:
        return []


# ---------------------
# Funções públicas
# ---------------------


def list_all_children(base_folder: PathLike, ignore_hidden: bool = True) -> list[Path]:
    """
    Lista arquivos e pastas dentro de um diretório.

    Args:
        base_folder (PathLike): Diretório base para listagem.
        ignore_hidden (bool): Se True, ignora itens ocultos (nomes começando com '.').

    Returns:
        list[Path]: Caminhos filhos válidos.
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return []

    return _safe_iterdir(directory=base_folder, ignore_hidden=ignore_hidden)


def filter_for_folders(items: list[Path]) -> list[Path]:
    """
    Filtra e retorna apenas os diretórios da lista.

    Args:
        items (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas diretórios.
    """
    return [item for item in items if item.is_dir()]


def filter_for_files(items: list[Path]) -> list[Path]:
    """
    Filtra e retorna apenas os arquivos da lista.

    Args:
        items (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas arquivos.
    """
    return [item for item in items if item.is_file()]


def list_empty_folders(base_folder: PathLike) -> list[Path]:
    """
    Lista pastas sem conteúdo dentro de um diretório.

    Args:
        base_folder (PathLike): Diretório base para busca.

    Returns:
        list[Path]: Pastas vazias.
    """
    children: list[Path] = list_all_children(base_folder=base_folder)
    folders: list[Path] = filter_for_folders(items=children)
    return [folder for folder in folders if not any(folder.iterdir())]


def calculate_depth(base_folder: PathLike) -> int:
    """
    Calcula a profundidade máxima da árvore de diretórios.

    Args:
        base_folder (PathLike): Diretório base.

    Returns:
        int: Profundidade máxima (0 se inválida).
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return 0

    max_depth = 0
    base_parts: int = len(base_folder.parts)

    try:
        for path in base_folder.rglob(pattern="*"):
            if path.is_dir():
                depth: int = len(path.parts) - base_parts
                if depth > max_depth:
                    max_depth: int = depth
    except PermissionError:
        pass

    return max_depth


def search_by_extension(base_folder: PathLike, extension: str) -> list[Path]:
    """
    Busca arquivos na pasta base com a extensão especificada (case-insensitive).
    Suporta extensões compostas como '.tar.gz'.

    Args:
        base_folder (PathLike): Diretório base para busca.
        extension (str): Extensão, ex: '.txt' ou '.tar.gz'.

    Returns:
        list[Path]: Arquivos correspondentes.
    """
    base_folder = validate_path(path_neutral=base_folder)
    if not base_folder.is_dir():
        return []

    ext_lower: str = extension.lower().lstrip(".")
    ext_parts: list[str] = ext_lower.split(".")

    results: list[Path] = []
    try:
        for file in base_folder.iterdir():
            if file.is_file():
                suffixes: list[str] = [s.lstrip(".").lower() for s in file.suffixes]
                if suffixes[-len(ext_parts) :] == ext_parts:
                    results.append(file)
    except PermissionError:
        pass

    return results
