"""
system_tools.py
---------------------
Funções utilitárias para manipulação do sistema operacional,
validação e normalização de caminhos, verificação de permissões
e detecção de sistema de arquivos.
"""

import platform
import re
from pathlib import Path

import psutil

from utils.main_tools import validate_path

# Regex padrão por SO para validar caminhos
_REGEX_PATHS: dict[str, re.Pattern[str]] = {
    "windows": re.compile(r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)*$"),
    "linux": re.compile(r"^(/[^/\0]+)+/?$"),
    "darwin": re.compile(r"^(/[^/\0]+)+/?$"),
}

# Padrões típicos por SO para reconhecer caminhos especiais
_PATH_PATTERNS: dict[str, list[re.Pattern]] = {
    "windows": [
        re.compile(r".*\.exe$", re.IGNORECASE),
        re.compile(r".*\.bat$", re.IGNORECASE),
        re.compile(r".*\\Documents\\.*", re.IGNORECASE),
        re.compile(r".*\\AppData\\.*", re.IGNORECASE),
    ],
    "linux": [
        re.compile(r".*\.sh$", re.IGNORECASE),
        re.compile(r"/etc/.*"),
        re.compile(r"/home/[^/]+/?$"),
        re.compile(r"/usr/(bin|lib|share)/.*"),
        re.compile(r"/proc/.*"),
        re.compile(r"/sys/.*"),
        re.compile(r"/var/.*"),
    ],
    "darwin": [
        re.compile(r".*\.app$", re.IGNORECASE),
        re.compile(r"/Users/[^/]+/Library/.*"),
        re.compile(r"/Applications/.*"),
        re.compile(r"/System/.*"),
    ],
}


def _get_os_name_lower() -> str:
    """Retorna o nome do sistema operacional em minúsculas."""
    return platform.system().lower()


def _get_regex_for_os(os_name_lower: str) -> re.Pattern:
    """Retorna a regex compilada para validação de caminho do SO especificado."""
    return _REGEX_PATHS.get(os_name_lower, _REGEX_PATHS["linux"])


def detect_system() -> str:
    """Retorna o nome do sistema operacional atual."""
    return platform.system()


def system_path_regex() -> re.Pattern:
    """Retorna a regex compilada para validação de caminhos do sistema atual."""
    os_name_lower: str = _get_os_name_lower()
    return _get_regex_for_os(os_name_lower=os_name_lower)


def validate_os_path(path: str | Path, validate_existence: bool = True) -> dict[str, bool]:
    """
    Valida caminho conforme SO e padrões específicos.

    Args:
        path: caminho (str ou Path)
        validate_existence: se True, exige caminho existente

    Returns:
        dict com flags 'formato_valido' e 'padrao_reconhecido'
    """
    path_str = str(path)
    if validate_existence:
        path_str = str(validate_path(path_neutral=path))

    os_name: str = _get_os_name_lower()

    base_regex: re.Pattern[str] = _REGEX_PATHS.get(os_name, _REGEX_PATHS["linux"])
    pattern_list: list[re.Pattern] = _PATH_PATTERNS.get(os_name, [re.compile(r".*")])

    formato_valido = bool(base_regex.fullmatch(path_str))
    padrao_reconhecido: bool = any(pat.match(path_str) for pat in pattern_list)

    return {"formato_valido": formato_valido, "padrao_reconhecido": padrao_reconhecido}


def get_user_root_folder(base_path: str | None = None) -> Path:
    """Retorna a pasta raiz do usuário ou o caminho base informado."""
    base: Path = Path(base_path) if base_path else Path.home()
    return base.expanduser().resolve()


def detect_filesystem(path: Path) -> dict[str, str]:
    """
    Detecta sistema de arquivos e ponto de montagem via psutil.

    Args:
        path: caminho para analisar

    Returns:
        dict com 'tipo', 'ponto_montagem' e 'opcoes'
    """
    try:
        resolved_path: Path = path.resolve()
    except (OSError, PermissionError):
        return {"tipo": "UNKNOWN", "ponto_montagem": "", "opcoes": ""}

    for part in psutil.disk_partitions():
        try:
            mountpoint: Path = Path(part.mountpoint).resolve()
            mount_str = str(mountpoint)
            path_str = str(resolved_path)
            if not mount_str.endswith("/"):
                mount_str += "/"
            if not path_str.endswith("/"):
                path_str += "/"

            if path_str.startswith(mount_str):
                return {
                    "tipo": part.fstype,
                    "ponto_montagem": part.mountpoint,
                    "opcoes": part.opts,
                }
        except (OSError, PermissionError):
            continue

    return {"tipo": "UNKNOWN", "ponto_montagem": "", "opcoes": ""}
