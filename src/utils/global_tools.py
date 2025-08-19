"""
global_tools.py
---------------

Funções utilitárias globais para manipulação de:
    - Sistema operacional
    - Arquivos e pastas
    - Metadados
    - Funções auxiliares

Organização por blocos:
    - [SYSTEM]
    - [FILES]
    - [FOLDERS]
    - [METADATA]
    - [UTILS]
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

# ============================================================
# [TYPES]
# ============================================================


class DatasCaminho(TypedDict):
    """Datas relevantes de um caminho no sistema de arquivos."""

    criacao: datetime
    modificacao: datetime
    acesso: datetime


class PermissoesCaminho(TypedDict):
    """Permissões de acesso a um caminho."""

    leitura: bool
    escrita: bool
    execucao: bool


class InfosCaminho(TypedDict):
    """Informações detalhadas sobre um caminho (arquivo, pasta ou outro)."""

    nome: str
    caminho: str
    tamanho_bytes: int
    datas: DatasCaminho
    permissoes: PermissoesCaminho
    tipo: Literal["arquivo", "pasta", "outro"]


class InfosCaminhoFormatado(TypedDict):
    """Informações de um caminho formatadas para leitura humana."""

    nome: str
    caminho: str
    tipo: Literal["arquivo", "pasta", "outro"]
    tamanho: str
    datas: dict[str, str]
    permissoes: str


# ============================================================
# [CHECKERS]
# ============================================================


def global_method_check_valid_path(caminho_generico: str | Path) -> Path:
    """
    Valida se um caminho pode ser usado:
    - Deve existir
    - Não pode ser oculto
    - Deve ter permissão de leitura (sempre)
    - Pode ter escrita OU só leitura
    """
    caminho: Path = Path(caminho_generico).resolve()

    if not caminho.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {caminho}")

    if caminho.name.startswith("."):
        raise ValueError(f"Caminho oculto não permitido: {caminho}")

    if not os.access(caminho, os.R_OK):
        raise PermissionError(f"Sem permissão de leitura: {caminho}")

    # Se não tiver escrita mas tiver leitura, passa
    if not (os.access(caminho, os.R_OK) or os.access(caminho, os.W_OK)):
        raise PermissionError(f"Sem permissões adequadas: {caminho}")

    return caminho


def global_method_buscar_filhos(caminho_de_pasta: str | Path) -> list[Path]:
    """Lista todos os arquivos e pastas recursivamente dentro de uma pasta."""
    p: Path = global_method_check_valid_path(caminho_generico=caminho_de_pasta)
    return list(p.rglob("*"))


# ============================================================
# [GETTERS]
# ============================================================


def global_method_obter_id_caminho(caminho_generico: str | Path) -> str:
    """Gera um UUID5 baseado no caminho absoluto."""
    caminho = str(global_method_check_valid_path(caminho_generico=caminho_generico))
    return str(uuid.uuid5(uuid.NAMESPACE_URL, caminho))


def global_method_obter_nome_caminho(caminho_generico: str | Path) -> str:
    """Retorna o nome do arquivo ou da pasta a partir do caminho."""
    return global_method_check_valid_path(caminho_generico=caminho_generico).name


def global_method_obter_tamanho_caminho(caminho_generico: str | Path) -> int:
    """Retorna o tamanho total em bytes de um caminho (arquivo ou pasta)."""
    p: Path = global_method_check_valid_path(caminho_generico=caminho_generico)
    if p.is_file():
        return p.stat().st_size
    if p.is_dir():
        return sum(f.stat().st_size for f in global_method_buscar_filhos(caminho_de_pasta=p) if f.is_file())
    return 0


def global_method_obter_datas_caminho(caminho_generico: str | Path) -> DatasCaminho:
    """Retorna datas de criação, modificação e acesso de um caminho."""
    p: Path = global_method_check_valid_path(caminho_generico=caminho_generico)
    st: os.stat_result = p.stat()
    return {
        "criacao": datetime.fromtimestamp(st.st_ctime),
        "modificacao": datetime.fromtimestamp(st.st_mtime),
        "acesso": datetime.fromtimestamp(st.st_atime),
    }


def global_method_obter_permissoes_caminho(caminho_generico: str | Path) -> PermissoesCaminho:
    """Retorna permissões de leitura, escrita e execução de um caminho."""
    p = global_method_check_valid_path(caminho_generico=caminho_generico)
    return {
        "leitura": os.access(p, os.R_OK),
        "escrita": os.access(p, os.W_OK),
        "execucao": os.access(p, os.X_OK),
    }


# ============================================================
# [FORMATTERS]
# ============================================================


def global_method_formatar_tamanho_caminho(tamanho_bytes: int | float) -> str:
    """Formata o tamanho em bytes para uma representação legível."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024
    return f"{tamanho_bytes:.2f} PB"


def global_method_formatar_data(data: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
    """Formata um objeto datetime para string."""
    return data.strftime(formato)


def global_method_infos_caminho(caminho_generico: str | Path) -> InfosCaminho:
    """
    Retorna um dicionário com infos do caminho:
    - tamanho em bytes
    - datas de criação, modificação e acesso (datetime)
    - permissões (dict bools)
    - tipo (arquivo/pasta/outro)
    """
    p: Path = global_method_check_valid_path(caminho_generico=caminho_generico)
    return {
        "nome": p.name,
        "caminho": str(p),
        "tamanho_bytes": global_method_obter_tamanho_caminho(caminho_generico=p),
        "datas": global_method_obter_datas_caminho(caminho_generico=p),
        "permissoes": global_method_obter_permissoes_caminho(caminho_generico=p),
        "tipo": "pasta" if p.is_dir() else "arquivo" if p.is_file() else "outro",
    }


def global_method_formatar_infos_caminho(infos: InfosCaminho) -> InfosCaminhoFormatado:
    """
    Formata um dicionário de infos de caminho para leitura humana:
    - tamanho em unidades (KB, MB, etc.)
    - datas formatadas em string
    - permissões como string rwx
    """
    perms: PermissoesCaminho = infos["permissoes"]
    perms_str: str = "".join(
        [
            "r" if perms["leitura"] else "-",
            "w" if perms["escrita"] else "-",
            "x" if perms["execucao"] else "-",
        ]
    )

    datas_formatadas: dict[str, str] = {
        k: global_method_formatar_data(v) for k, v in infos["datas"].items() if isinstance(v, datetime)
    }

    return {
        "nome": infos["nome"],
        "caminho": infos["caminho"],
        "tipo": infos["tipo"],
        "tamanho": global_method_formatar_tamanho_caminho(tamanho_bytes=infos["tamanho_bytes"]),
        "datas": datas_formatadas,
        "permissoes": perms_str,
    }
