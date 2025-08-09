"""
utils_arquivos.py
-----------------
Funções utilitárias para manipulação e análise de arquivos individuais.

Objetivos:
    - Fornecer acesso seguro e validado a propriedades de arquivos.
    - Evitar duplicação de código para formatos, permissões e dados.
    - Integrar com utils_comuns e utils_so para normalização e validação.

Objetos principais que utilizam:
    - SistemaArquivo
    - SistemaOperacional (para validações)
"""

from collections.abc import Iterable
from os import stat_result
from pathlib import Path

from .sistema_operacional import validar_caminho, verificar_permissoes
from .utils_comuns import coletar_datas_aprimoradas, normalizar_caminho


def obter_tamanho_arquivo(caminho: str | Path) -> int | None:
    """
    Retorna o tamanho do arquivo em bytes, se o arquivo existir e for acessível.

    Args:
        caminho (str | Path): Caminho do arquivo.

    Returns:
        int | None: Tamanho em bytes ou None se inacessível.
    """
    caminho_norm: Path = normalizar_caminho(caminho=caminho)
    if not validar_caminho(caminho=caminho_norm):
        return None
    try:
        if caminho_norm.is_file():
            return caminho_norm.stat().st_size
    except (OSError, PermissionError) as e:
        print(f"Erro -> {e}")

    return None


def obter_extensao_arquivo(caminho: str | Path) -> str | None:
    """
    Retorna a extensão do arquivo em minúsculas, incluindo o ponto.

    Args:
        caminho (str | Path): Caminho do arquivo.

    Returns:
        str | None: Extensão do arquivo ou None se inválido.
    """
    caminho_norm: Path = normalizar_caminho(caminho=caminho)
    if not validar_caminho(caminho=caminho_norm) or not caminho_norm.is_file():
        return None
    return caminho_norm.suffix.lower()


def obter_datas_arquivo(caminho: str | Path) -> None | dict[str, dict[str, float | str]]:
    """
    Retorna os timestamps do arquivo formatados via utils_comuns.

    Args:
        caminho (str | Path): Caminho do arquivo.

    Returns:
        None | dict[str, dict[str, float | str]]: Dicionário com timestamps ou None se inacessível.
    """
    caminho_norm: Path = normalizar_caminho(caminho=caminho)
    if not validar_caminho(caminho=caminho_norm) or not caminho_norm.is_file():
        return None
    try:
        stats: stat_result = caminho_norm.stat()
        return {
            "modificacao": coletar_datas_aprimoradas(timestamp=stats.st_mtime),
            "acesso": coletar_datas_aprimoradas(timestamp=stats.st_atime),
            "criado": coletar_datas_aprimoradas(timestamp=stats.st_ctime),
        }
    except (OSError, PermissionError) as e:
        print(f"Erro -> {e}")
    return None


def tem_permissao_leitura_arquivo(caminho: str | Path) -> bool:
    """
    Verifica se o arquivo tem permissão de leitura pelo usuário atual.

    Args:
        caminho (str | Path): Caminho do arquivo.

    Returns:
        bool: True se pode ler, False caso contrário.
    """
    caminho_norm: Path = normalizar_caminho(caminho=caminho)
    return verificar_permissoes(caminho=caminho_norm).get("ler", False)


def filtrar_apenas_arquivos(paths: Iterable[Path]) -> list[Path]:
    """
    Recebe um iterável de Paths e retorna apenas os que são arquivos.
    """
    return [p for p in paths if p.is_file()]


def buscar_por_extensao(pasta: Path, extensao: str) -> list[Path]:
    """
    Retorna arquivos dentro da pasta com a extensão especificada.
    """
    extensao = extensao.lower()
    return [f for f in pasta.iterdir() if f.is_file() and f.suffix.lower() == extensao]
