"""
sistema_operacional.py.py
-----------
Utilitários para manipulação do sistema operacional, validação e normalização de caminhos,
verificação de permissões e detecção de sistema de arquivos.
"""

import platform
import re
from pathlib import Path

import psutil

from src.utils.main_tools import validar_caminho

# Regex padrão por SO para validar caminhos
_REGEX_PATHS: dict[str, re.Pattern[str]] = {
    "Windows": re.compile(pattern=r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)*$"),
    "Linux": re.compile(pattern=r"^(/[^/\0]+)+/?$"),
    "Darwin": re.compile(pattern=r"^(/[^/\0]+)+/?$"),
}


def detectar_sistema() -> str:
    """Retorna o nome do sistema operacional atual."""
    return platform.system()


def regex_caminho_sistema() -> re.Pattern:
    """Retorna regex compilada para validação de caminhos do SO atual."""
    return _REGEX_PATHS.get(detectar_sistema(), _REGEX_PATHS["Linux"])


def verificar_caminho_so(caminho: str | Path) -> dict[str, bool]:
    """
    Checa se o caminho tem formato válido e reconhece padrões típicos do SO.

    Retorna:
        dict com chaves:
            - formato_valido (bool): corresponde ao formato regex base do SO
            - padrao_reconhecido (bool): corresponde a algum padrão típico (apps, configs, etc)
    """
    caminho_str = str(validar_caminho(caminho_comum=caminho))
    so: str = detectar_sistema().lower()
    regex_base: str = {
        "windows": r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)*$",
        "linux": r"^(/[^/\0]+)+/?$",
        "darwin": r"^(/[^/\0]+)+/?$",
    }.get(so, r"^(/[^/\0]+)+/?$")

    padroes: list[str] = {
        "windows": [r".*\\.exe$", r".*\\.bat$", r".*\\Documents\\.*", r".*\\AppData\\.*"],
        "linux": [r".*\.sh$", r"/etc/.*", r"/home/[^/]+/?$", r"/usr/(bin|lib|share)/.*"],
        "darwin": [r".*\.app$", r"/Users/[^/]+/Library/.*", r"/Applications/.*", r"/System/.*"],
    }.get(so, [r".*"])

    formato_valido = bool(re.fullmatch(regex_base, caminho_str))
    padrao_reconhecido: bool = any(re.match(p, caminho_str) for p in padroes)
    return {"formato_valido": formato_valido, "padrao_reconhecido": padrao_reconhecido}


def obter_pasta_raiz_usuario(caminho_base: str | None = None) -> Path:
    """Retorna pasta raiz do usuário ou caminho base passado, normalizado."""
    base: Path = Path(caminho_base) if caminho_base else Path.home()
    return base.expanduser().resolve()


def detectar_sistema_arquivos(caminho: Path) -> dict[str, str]:
    """Detecta sistema de arquivos e ponto de montagem de um caminho (usando psutil)."""
    try:
        caminho = caminho.resolve()
        for part in psutil.disk_partitions():
            try:
                if caminho.is_relative_to(Path(part.mountpoint)):
                    return {"tipo": part.fstype, "ponto_montagem": part.mountpoint, "opcoes": part.opts}
            except (OSError, PermissionError):
                continue
    except (OSError, PermissionError):
        pass
    return {"tipo": "UNKNOWN", "ponto_montagem": "", "opcoes": ""}
