"""
sistema_operacional.py.py
-----------
Utilitários para manipulação do sistema operacional, validação e normalização de caminhos,
verificação de permissões e detecção de sistema de arquivos.
"""

import os
import platform
import re
from pathlib import Path

import psutil

from .utils_comuns import normalizar_caminho

# Regex padrão por SO para validar caminhos
_REGEX_PATHS: dict[str, re.Pattern[str]] = {
    "Windows": re.compile(r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)*$"),
    "Linux": re.compile(r"^(/[^/\0]+)+/?$"),
    "Darwin": re.compile(r"^(/[^/\0]+)+/?$"),
}


def detectar_sistema() -> str:
    """Retorna o nome do sistema operacional atual."""
    return platform.system()


def regex_caminho_sistema() -> re.Pattern:
    """Retorna regex compilada para validação de caminhos do SO atual."""
    return _REGEX_PATHS.get(detectar_sistema(), _REGEX_PATHS["Linux"])


def validar_caminho(caminho: str | Path) -> bool:
    """Valida caminho conforme regex do SO atual após normalizar."""
    caminho_str = str(normalizar_caminho(caminho))
    return bool(regex_caminho_sistema().fullmatch(caminho_str))


def verificar_permissoes(caminho: str | Path) -> dict[str, bool]:
    """Verifica permissões de leitura, escrita e execução no caminho."""
    path = normalizar_caminho(caminho)
    return {
        "ler": os.access(path, os.R_OK),
        "escrever": os.access(path, os.W_OK),
        "executar": os.access(path, os.X_OK),
    }


def tem_permissao_leitura(caminho: Path) -> bool:
    """Checa se o usuário tem permissão de leitura no caminho."""
    return os.access(caminho, os.R_OK)


def verificar_caminho_so(caminho: str | Path) -> dict[str, bool]:
    """
    Checa se o caminho tem formato válido e reconhece padrões típicos do SO.

    Retorna:
        dict com chaves:
            - formato_valido (bool): corresponde ao formato regex base do SO
            - padrao_reconhecido (bool): corresponde a algum padrão típico (apps, configs, etc)
    """
    caminho_str = str(normalizar_caminho(caminho=caminho))
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


def filtrar_arquivos_e_pastas(itens: list[Path]) -> tuple[list[Path], list[Path]]:
    """Separa lista em duas: (pastas, arquivos)."""
    pastas: list[Path] = [i for i in itens if i.is_dir()]
    arquivos: list[Path] = [i for i in itens if i.is_file()]
    return pastas, arquivos


def listar_subcaminhos(pasta_base: Path, ignorar_ocultos: bool = True) -> list[Path]:
    """Lista itens não ocultos em pasta_base, ignorando erros de permissão."""
    if not pasta_base.exists() or not pasta_base.is_dir():
        return []
    try:
        return [item for item in pasta_base.iterdir() if not (ignorar_ocultos and item.name.startswith("."))]
    except PermissionError:
        return []


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
