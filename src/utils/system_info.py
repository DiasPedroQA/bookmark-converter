"""
system_info.py

Detecta o ambiente do sistema operacional local, incluindo:
- Caminho da home do usuário
- Nome do sistema operacional
- Padrões de arquivos e pastas comuns, via regex
"""

import os
import platform
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def _detectar_regex_por_so(sistema_operacional: str) -> list[str]:
    """Retorna uma lista de padrões regex típicos por SO."""
    so = sistema_operacional.lower()

    match so:
        case "windows":
            return [
                r".*\\.exe$",
                r".*\\.bat$",
                r".*\\Documents\\.*",
                r".*\\AppData\\.*",
            ]
        case "linux":
            return [
                r".*\.sh$",
                r"/etc/.*",
                r"/home/[^/]+/?$",
                r"/home/[^/]+/.*",
                r"/usr/(bin|lib|share)/.*",
            ]
        case "darwin":
            return [
                r".*\.app$",
                r"/Users/[^/]+/Library/.*",
                r"/Applications/.*",
                r"/System/.*",
            ]
        case _:
            return [r".*"]


def verificar_caminho_so(
    caminho: str | Path
) -> dict[str, bool]:
    """
    Verifica se um caminho é válido e/ou reconhecido com base no SO atual.

    Args:
        caminho: Caminho a ser verificado.

    Returns:
        Dicionário com status das validações.
    """
    caminho_str = str(Path(caminho).expanduser())
    so: str = platform.system().lower()

    regex_formato: str = {
        "linux": r"^/([a-zA-Z0-9_\-\.]+/?)*$",
        "darwin": r"^/Users/[a-zA-Z0-9_\-\.]+(/.*)?$",
        "windows": r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)*$",
    }.get(so, r"^/([a-zA-Z0-9_\-\.]+/?)*$")

    padroes: list[str] = _detectar_regex_por_so(sistema_operacional=so)

    resultado: dict[str, bool] = {
        "formato_valido": bool(re.match(regex_formato, caminho_str)),
        "padrao_reconhecido": any(re.match(p, caminho_str) for p in padroes),
    }

    return resultado


def formatar_data(timestamp: float) -> str:
    """Converte um timestamp para string legível."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def bytes_para_legivel(tamanho: int | float) -> str:
    """Converte tamanho em bytes para unidade legível (KB, MB, etc)."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if tamanho < 1024:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024
    return f"{tamanho:.2f} PB"


def tem_permissao_leitura(caminho: Path) -> bool:
    """Verifica se o caminho possui permissão de leitura."""
    return os.access(caminho, os.R_OK)


def obter_pasta_raiz_usuario(**kwargs: Any) -> Path:
    """Retorna a pasta base do usuário logado ou a definida em kwargs."""
    base: Any | None = kwargs.get("caminho_base")
    return Path(base or Path.home()).expanduser().resolve()


def filtrar_arquivos_e_pastas(itens: list[Path]) -> tuple[list[Path], list[Path]]:
    """Separa uma lista de Paths entre arquivos e pastas."""
    pastas: list[Path] = [item for item in itens if item.is_dir()]
    arquivos: list[Path] = [item for item in itens if item.is_file()]
    return pastas, arquivos


def listar_subcaminhos(pasta_base: Path) -> list[Path]:
    """Lista subcaminhos visíveis (não ocultos) da pasta base."""
    if not pasta_base.exists() or not pasta_base.is_dir():
        return []
    try:
        return [item for item in pasta_base.iterdir() if not item.name.startswith(".")]
    except PermissionError:
        return []
