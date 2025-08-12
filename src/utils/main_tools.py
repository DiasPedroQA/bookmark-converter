"""
main_tools.py
---------------
Funções utilitárias para metadados comuns de arquivos e pastas.

Fornece:
    - Identificação única (UUID)
    - Nome e caminhos
    - Tamanho total
    - Datas de criação, modificação e acesso
    - Permissões (leitura, escrita, execução)
    - Visibilidade (oculto ou não)
"""

import os
import uuid
from datetime import datetime
from pathlib import Path

# ---------------------
# Funções privadas
# ---------------------


def _get_absolute_path(path_neutral: str | Path) -> Path:
    """Retorna o caminho absoluto normalizado."""
    return Path(path_neutral).resolve()


def _scan_directory(directory: Path, max_depth: int, current_depth: int = 1) -> int:
    """
    Soma recursivamente o tamanho dos arquivos em um diretório.
    Ignora links simbólicos e erros de acesso.
    """
    if current_depth > max_depth:
        return 0
    total_bytes = 0
    try:
        for item in directory.iterdir():
            try:
                if item.is_symlink():
                    continue
                if item.is_file():
                    total_bytes += item.stat().st_size
                elif item.is_dir():
                    total_bytes += _scan_directory(directory=item, max_depth=max_depth, current_depth=current_depth + 1)
            except (FileNotFoundError, PermissionError, OSError):
                continue
    except (FileNotFoundError, PermissionError, OSError):
        pass
    return total_bytes


# ---------------------
# Funções públicas
# ---------------------


def validate_path(path_neutral: str | Path) -> Path:
    """Valida se o caminho existe no sistema de arquivos."""
    abs_path: Path = _get_absolute_path(path_neutral=path_neutral)
    if not abs_path.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {abs_path}")
    return abs_path


def get_id_path(path_neutral: str | Path) -> str:
    """Gera um identificador único (UUID5) com base no caminho absoluto."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, str(_get_absolute_path(path_neutral))))


def get_name_path(path_neutral: str | Path) -> str:
    """Retorna o nome do arquivo ou pasta."""
    return Path(path_neutral).name


def get_size_path(path_neutral: str | Path, max_depth: int = 30) -> int:
    """Retorna o tamanho total em bytes de um arquivo ou pasta."""
    p = Path(path_neutral)
    if p.is_file():
        try:
            return p.stat().st_size
        except (FileNotFoundError, PermissionError, OSError):
            return 0
    if p.is_dir():
        return _scan_directory(directory=p, max_depth=max_depth)
    return 0


def get_dates_path(path_neutral: str | Path) -> dict[str, datetime]:
    """Retorna as datas de criação, modificação e último acesso."""
    st: os.stat_result = Path(path_neutral).stat()
    return {
        "creation": datetime.fromtimestamp(st.st_ctime),
        "modification": datetime.fromtimestamp(st.st_mtime),
        "access": datetime.fromtimestamp(st.st_atime),
    }


def get_permissions_path(path_neutral: str | Path) -> dict[str, bool]:
    """Retorna permissões de leitura, escrita e execução."""
    p = Path(path_neutral)
    return {
        "read": os.access(p, os.R_OK),
        "write": os.access(p, os.W_OK),
        "execute": os.access(p, os.X_OK),
    }


def is_hidden_path(path_neutral: str | Path) -> bool:
    """Verifica se o arquivo ou pasta é oculto."""
    return Path(path_neutral).name.startswith(".")
