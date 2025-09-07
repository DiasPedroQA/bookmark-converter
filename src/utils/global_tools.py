"""
global_tools.py
---------------

Módulo utilitário global para manipulação de arquivos e pastas.

Fornece funções organizadas em categorias:
- Validação e verificação
- Obtenção de metadados e informações
- Formatação e conversão
- Operações de arquivo e pasta

Organização por seções:
    - [CHECKERS]: Funções de validação e verificação
    - [GETTERS]: Funções para obtenção de informações
    - [FORMATTERS]: Funções de formatação e conversão
"""

import os
import stat
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal

# ============================================================
# [CHECKERS] - Funções de validação e verificação
# ============================================================


def check_valid_path(caminho_generico: str | Path) -> Path:
    """
    Valida se um caminho existe e possui permissões adequadas.

    Args:
        caminho_generico: Caminho para validar (str ou Path)

    Returns:
        Path: Objeto Path válido e resolvido

    Raises:
        FileNotFoundError: Se o caminho não existir
        PermissionError: Se não houver permissões adequadas
    """
    caminho: Path = Path(caminho_generico).resolve()

    if not caminho.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {caminho}")

    # Verificar permissões de leitura
    if not os.access(caminho, os.R_OK):
        raise PermissionError(f"Sem permissão de leitura: {caminho}")

    return caminho


def check_path_is_hidden(caminho_generico: str | Path) -> bool:
    """
    Verifica se um caminho é oculto.

    Args:
        caminho_generico: Caminho para verificar

    Returns:
        bool: True se o caminho for oculto, False caso contrário
    """
    caminho = check_valid_path(caminho_generico)
    return caminho.name.startswith(".") or any(part.startswith(".") for part in caminho.parts)


# ============================================================
# [GETTERS] - Funções para obtenção de informações
# ============================================================


def obter_id_caminho(caminho_generico: str | Path) -> str:
    """
    Gera um UUID5 único baseado no caminho absoluto.

    Args:
        caminho_generico: Caminho para gerar ID

    Returns:
        str: UUID5 baseado no caminho
    """
    caminho = check_valid_path(caminho_generico)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, str(caminho.absolute())))


def obter_nome_caminho(caminho_generico: str | Path) -> str:
    """
    Retorna o nome do arquivo ou pasta a partir do caminho.

    Args:
        caminho_generico: Caminho para obter nome

    Returns:
        str: Nome do arquivo ou pasta
    """
    return check_valid_path(caminho_generico).name


def obter_tamanho_caminho(caminho_generico: str | Path) -> int:
    """
    Retorna o tamanho total em bytes de um caminho (arquivo ou pasta).

    Args:
        caminho_generico: Caminho para obter tamanho

    Returns:
        int: Tamanho em bytes
    """
    caminho: Path = check_valid_path(caminho_generico=caminho_generico)

    if caminho.is_file():
        return caminho.stat().st_size

    if caminho.is_dir():
        total_size = 0
        for arquivo in caminho.rglob("*"):
            if arquivo.is_file():
                total_size += arquivo.stat().st_size
        return total_size

    return 0


def obter_datas_caminho(caminho_generico: str | Path) -> dict[str, datetime]:
    """
    Retorna datas de criação, modificação e acesso de um caminho.

    Args:
        caminho_generico: Caminho para obter datas

    Returns:
        dict[str, datetime]: Dicionário com datas
    """
    caminho: Path = check_valid_path(caminho_generico=caminho_generico)
    estatisticas = caminho.stat()

    return {
        "criacao": datetime.fromtimestamp(estatisticas.st_ctime),
        "modificacao": datetime.fromtimestamp(estatisticas.st_mtime),
        "acesso": datetime.fromtimestamp(estatisticas.st_atime),
    }


def obter_permissoes_caminho(caminho_generico: str | Path) -> dict[str, bool]:
    """
    Retorna permissões de leitura, escrita e execução de um caminho.

    Args:
        caminho_generico: Caminho para obter permissões

    Returns:
        dict[str, bool]: Dicionário com permissões
    """
    caminho = check_valid_path(caminho_generico)
    modo = caminho.stat().st_mode

    return {
        "leitura": bool(modo & stat.S_IRUSR),
        "escrita": bool(modo & stat.S_IWUSR),
        "execucao": bool(modo & stat.S_IXUSR),
    }


def obter_tipo_caminho(caminho_generico: str | Path) -> Literal["arquivo", "pasta", "outro"]:
    """
    Retorna o tipo do caminho (arquivo, pasta ou outro).

    Args:
        caminho_generico: Caminho para verificar tipo

    Returns:
        Literal['arquivo', 'pasta', 'outro']: Tipo do caminho
    """
    caminho = check_valid_path(caminho_generico)

    if caminho.is_file():
        return "arquivo"
    elif caminho.is_dir():
        return "pasta"
    else:
        return "outro"


# ============================================================
# [FORMATTERS] - Funções de formatação e conversão
# ============================================================


def formatar_tamanho_bytes(tamanho_bytes: str | float) -> str:
    """
    Formata o tamanho em bytes para uma representação legível.

    Args:
        tamanho_bytes: Tamanho em bytes para formatar

    Returns:
        str: String formatada com unidade apropriada
    """
    unidades: list[str] = ["B", "KB", "MB", "GB", "TB", "PB"]
    tamanho = float(tamanho_bytes)

    for unidade in unidades:
        if tamanho < 1024.0 or unidade == unidades[-1]:
            return f"{tamanho:.2f} {unidade}"
        tamanho /= 1024.0

    return f"{tamanho:.2f} {unidades[-1]}"


def formatar_data(data: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Formata um objeto datetime para string.

    Args:
        data: Datetime para formatar
        formato: Formato de saída (padrão: dd/mm/aaaa HH:MM:SS)

    Returns:
        str: Data formatada como string
    """
    return data.strftime(formato)


def formatar_permissoes(permissoes: dict[str, bool]) -> str:
    """
    Formata permissões para representação estilo Unix (rwx).

    Args:
        permissoes: Dicionário com permissões

    Returns:
        str: String no formato rwx
    """
    return "".join(
        [
            "r" if permissoes.get("leitura", False) else "-",
            "w" if permissoes.get("escrita", False) else "-",
            "x" if permissoes.get("execucao", False) else "-",
        ]
    )


def infos_caminho_formatadas(
    caminho_generico: str | Path,
) -> dict[str, str | int | dict[str, str] | dict[str, datetime] | bool | dict[str, bool]]:
    """
    Retorna informações formatadas para leitura humana de um caminho.

    Args:
        caminho_generico: Caminho para obter informações

    Returns:
        dict[str, str | int | dict[str, str] | dict[str, datetime] | bool | dict[str, bool]]: Dicionário com informações formatadas
    """
    caminho: Path = check_valid_path(caminho_generico=caminho_generico)
    permissoes: dict[str, bool] = obter_permissoes_caminho(caminho_generico=caminho)
    datas: dict[str, datetime] = obter_datas_caminho(caminho_generico=caminho)

    return {
        "nome": obter_nome_caminho(caminho_generico=caminho),
        "caminho": str(caminho.absolute()),
        "tipo": obter_tipo_caminho(caminho_generico=caminho),
        "tamanho": formatar_tamanho_bytes(tamanho_bytes=obter_tamanho_caminho(caminho_generico=caminho)),
        "tamanho_bytes": obter_tamanho_caminho(caminho_generico=caminho),
        "datas": {chave: formatar_data(valor) for chave, valor in datas.items()},
        "permissoes": formatar_permissoes(permissoes=permissoes),
        "permissoes_raw": permissoes,
        "datas_raw": datas,
        "oculto": check_path_is_hidden(caminho_generico=caminho),
    }


def infos_caminho_raw(
    caminho_generico: str | Path,
) -> dict[str, str | int | dict[str, datetime] | bool | dict[str, bool]]:
    """
    Retorna informações brutas de um caminho.

    Args:
        caminho_generico: Caminho para obter informações

    Returns:
        dict[str, str | int | dict[str, datetime] | bool | dict[str, bool]]: Dicionário com informações brutas
    """
    caminho: Path = check_valid_path(caminho_generico=caminho_generico)

    return {
        "nome": obter_nome_caminho(caminho_generico=caminho),
        "caminho": str(caminho.absolute()),
        "tamanho_bytes": obter_tamanho_caminho(caminho_generico=caminho),
        "datas": obter_datas_caminho(caminho_generico=caminho),
        "permissoes": obter_permissoes_caminho(caminho_generico=caminho),
        "tipo": obter_tipo_caminho(caminho_generico=caminho),
        "oculto": check_path_is_hidden(caminho_generico=caminho),
        "id": obter_id_caminho(caminho_generico=caminho),
    }
