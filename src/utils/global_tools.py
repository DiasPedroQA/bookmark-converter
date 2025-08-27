"""
global_tools.py
---------------

Funções utilitárias globais para manipulação de arquivos e pastas:
- Sistema operacional
- Arquivos e pastas
- Metadados
- Funções auxiliares

Organização por blocos:
    - [TYPES]
    - [CHECKERS]
    - [GETTERS]
    - [FORMATTERS]
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import TypedDict

# ============================================================
# [TYPES]
# ============================================================


class SystemInfo(TypedDict):
    os_name: str
    hostname: str
    username: str
    home: str
    ip: str | None
    kernel_version: str
    platform: str
    disk_free: str | None


class RawFileInfo(TypedDict):
    """Informações brutas de um arquivo/pasta (direto do sistema)."""

    nome: str
    caminho: str
    tamanho_bytes: int
    datas: dict[str, datetime]
    permissoes: dict[str, bool]
    tipo: str  # "arquivo" | "pasta" | "outro"


class FileInfo(TypedDict):
    """Informações formatadas para leitura humana."""

    nome: str
    caminho: str
    tipo: str
    tamanho: str
    datas: dict[str, str]
    permissoes: str


# ============================================================
# [CHECKERS]
# ============================================================


def check_valid_path(caminho_generico: str | Path) -> Path:
    """Valida se um caminho existe, não é oculto e possui permissões adequadas."""
    caminho: Path = Path(caminho_generico).resolve()

    if not caminho.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {caminho}")
    if caminho.name.startswith("."):
        raise ValueError(f"Caminho oculto não permitido: {caminho}")
    if not os.access(caminho, os.R_OK):
        raise PermissionError(f"Sem permissão de leitura: {caminho}")
    if not (os.access(caminho, os.R_OK) or os.access(caminho, os.W_OK)):
        raise PermissionError(f"Sem permissões adequadas: {caminho}")
    return caminho


def buscar_filhos(caminho_de_pasta: str | Path) -> list[Path]:
    """Lista todos os arquivos e pastas recursivamente dentro de uma pasta."""
    p: Path = check_valid_path(caminho_de_pasta)
    return list(p.rglob("*"))


# ============================================================
# [GETTERS]
# ============================================================


def obter_id_caminho(caminho_generico: str | Path) -> str:
    """Gera um UUID5 baseado no caminho absoluto."""
    caminho = str(check_valid_path(caminho_generico))
    return str(uuid.uuid5(uuid.NAMESPACE_URL, caminho))


def obter_nome_caminho(caminho_generico: str | Path) -> str:
    """Retorna o nome do arquivo ou da pasta a partir do caminho."""
    return check_valid_path(caminho_generico).name


def obter_tamanho_caminho(caminho_generico: str | Path) -> int:
    """Retorna o tamanho total em bytes de um caminho (arquivo ou pasta)."""
    p: Path = check_valid_path(caminho_generico)
    if p.is_file():
        return p.stat().st_size
    if p.is_dir():
        return sum(f.stat().st_size for f in buscar_filhos(p) if f.is_file())
    return 0


def obter_datas_caminho(caminho_generico: str | Path) -> dict[str, datetime]:
    """Retorna datas de criação, modificação e acesso de um caminho."""
    p: Path = check_valid_path(caminho_generico)
    st: os.stat_result = p.stat()
    return {
        "criacao": datetime.fromtimestamp(st.st_ctime),
        "modificacao": datetime.fromtimestamp(st.st_mtime),
        "acesso": datetime.fromtimestamp(st.st_atime),
    }


def obter_permissoes_caminho(caminho_generico: str | Path) -> dict[str, bool]:
    """Retorna permissões de leitura, escrita e execução de um caminho."""
    p: Path = check_valid_path(caminho_generico)
    return {
        "leitura": os.access(p, os.R_OK),
        "escrita": os.access(p, os.W_OK),
        "execucao": os.access(p, os.X_OK),
    }


# ============================================================
# [FORMATTERS]
# ============================================================


def formatar_tamanho(tamanho_bytes: int | float) -> str:
    """Formata o tamanho em bytes para uma representação legível."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024
    return f"{tamanho_bytes:.2f} PB"


def formatar_data(data: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
    """Formata um objeto datetime para string."""
    return data.strftime(formato)


def infos_caminho(infos: RawFileInfo) -> FileInfo:
    """Formata informações brutas para leitura humana."""
    perms: dict[str, bool] = infos["permissoes"]
    perms_str = "".join(
        [
            "r" if perms["leitura"] else "-",
            "w" if perms["escrita"] else "-",
            "x" if perms["execucao"] else "-",
        ]
    )
    datas_formatadas = {k: formatar_data(v) for k, v in infos["datas"].items()}
    return {
        "nome": infos["nome"],
        "caminho": infos["caminho"],
        "tipo": infos["tipo"],
        "tamanho": formatar_tamanho(infos["tamanho_bytes"]),
        "datas": datas_formatadas,
        "permissoes": perms_str,
    }


def infos_caminho_raw(caminho_generico: str | Path) -> RawFileInfo:
    """Retorna informações brutas de um caminho."""
    p: Path = check_valid_path(caminho_generico)
    return {
        "nome": p.name,
        "caminho": str(p),
        "tamanho_bytes": obter_tamanho_caminho(p),
        "datas": obter_datas_caminho(p),
        "permissoes": obter_permissoes_caminho(p),
        "tipo": "pasta" if p.is_dir() else "arquivo" if p.is_file() else "outro",
    }
