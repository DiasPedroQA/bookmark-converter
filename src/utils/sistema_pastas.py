"""
utils_pastas.py
---------------
Funções utilitárias para manipulação e análise de diretórios.

Objetivos:
    - Listar conteúdo de pastas com filtros e detalhes.
    - Calcular tamanho, profundidade, e estatísticas de diretórios.
    - Garantir segurança e consistência via normalização e validação.

Objetos principais que utilizam:
    - SistemaPasta
    - SistemaOperacional (para validação)
"""

from collections.abc import Iterable
from os import stat_result
from pathlib import Path

from .sistema_operacional import validar_caminho
from .utils_comuns import (
    coletar_datas_aprimoradas,
    formatar_tamanho,
    normalizar_caminho,
)


def listar_subcaminhos(pasta_base: Path, ignorar_ocultos: bool = True) -> list[Path]:
    """
    Lista arquivos e pastas dentro de `pasta_base`.

    Args:
        pasta_base (Path): Diretório base para listagem.
        ignorar_ocultos (bool): Ignora itens que começam com '.' se True.

    Returns:
        list[Path]: Lista de caminhos filhos válidos.
    """
    pasta_norm: Path = normalizar_caminho(caminho=pasta_base)
    if not validar_caminho(caminho=pasta_norm) or not pasta_norm.is_dir():
        return []

    try:
        itens: list[Path] = [
            item for item in pasta_norm.iterdir() if not (ignorar_ocultos and item.name.startswith("."))
        ]
    except PermissionError:
        return []
    return itens


def filtrar_apenas_pastas(paths: Iterable[Path]) -> list[Path]:
    """
    Recebe um iterável de Paths e retorna apenas os que são diretórios (pastas).
    """
    return [p for p in paths if p.is_dir()]


def filtrar_pastas(itens: list[Path]) -> list[Path]:
    """
    Filtra e retorna apenas as pastas da lista fornecida.

    Args:
        itens (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas os diretórios.
    """
    return [item for item in itens if item.is_dir()]


def filtrar_arquivos(itens: list[Path]) -> list[Path]:
    """
    Filtra e retorna apenas os arquivos da lista fornecida.

    Args:
        itens (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas arquivos.
    """
    return [item for item in itens if item.is_file()]


def listar_pastas_vazias(pasta_base: Path) -> list[Path]:
    """
    Retorna lista de pastas vazias dentro de `pasta_base`.

    Args:
        pasta_base (Path): Diretório para análise.

    Returns:
        list[Path]: Pastas sem conteúdo.
    """
    itens: list[Path] = listar_subcaminhos(pasta_base=pasta_base)
    pastas: list[Path] = filtrar_pastas(itens=itens)
    vazias: list[Path] = [pasta for pasta in pastas if not any(pasta.iterdir())]
    return vazias


def calcular_profundidade(pasta_base: Path) -> int:
    """
    Calcula a profundidade máxima da árvore de diretórios a partir de `pasta_base`.

    Args:
        pasta_base (Path): Diretório base.

    Returns:
        int: Profundidade máxima encontrada (0 se pasta vazia).
    """
    pasta_norm: Path = normalizar_caminho(caminho=pasta_base)
    if not validar_caminho(caminho=pasta_norm) or not pasta_norm.is_dir():
        return 0

    max_depth = 0
    base_parts: int = len(pasta_norm.parts)

    for path in pasta_norm.rglob("*"):
        if path.is_dir():
            depth: int = len(path.parts) - base_parts
            if depth > max_depth:
                max_depth: int = depth
    return max_depth


def calcular_tamanho_pasta(pasta_base: Path, limite_nivel: int = 10) -> tuple[int, int, bool]:
    """
    Calcula o tamanho total da pasta, número de itens e se limite de nível foi atingido.

    Args:
        pasta_base (Path): Diretório base.
        limite_nivel (int): Profundidade máxima para escanear.

    Returns:
        tuple[int, int, bool]: (tamanho_bytes, total_itens, limite_atingido)
    """
    pasta_norm: Path = normalizar_caminho(caminho=pasta_base)
    if not validar_caminho(caminho=pasta_norm) or not pasta_norm.is_dir():
        return 0, 0, False

    total_bytes = 0
    total_itens = 0
    limite_atingido = False

    def scan(dir_path: Path, nivel_atual: int) -> None:
        nonlocal total_bytes, total_itens, limite_atingido
        if nivel_atual > limite_nivel:
            limite_atingido = True
            return
        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    total_bytes += item.stat().st_size
                    total_itens += 1
                elif item.is_dir():
                    total_itens += 1
                    scan(dir_path=item, nivel_atual=nivel_atual + 1)
        except PermissionError:
            pass

    scan(dir_path=pasta_norm, nivel_atual=1)
    return total_bytes, total_itens, limite_atingido


def listar_conteudo_detalhado(pasta_base: Path) -> dict[str, dict | list | str]:
    """
    Lista arquivos e pastas com detalhes e estatísticas na pasta.

    Args:
        pasta_base (Path): Diretório para listar.

    Returns:
        dict[str, dict | list | str]: Dicionário com:
            - arquivos: lista de dicts com nome, tamanho legível, modificação formatada e extensão
            - pastas: lista de dicts com nome e modificação formatada
            - resumo: totais de arquivos e pastas
    """
    pasta_norm: Path = normalizar_caminho(caminho=pasta_base)
    if not validar_caminho(caminho=pasta_norm) or not pasta_norm.is_dir():
        return {"arquivos": [], "pastas": [], "resumo": {"total_arquivos": 0, "total_pastas": 0}}

    arquivos: list[dict[str, str | dict[str, float | str]]] = []
    pastas: list[dict[str, str | dict[str, float | str]]] = []
    try:
        for item in pasta_norm.iterdir():
            try:
                stat: stat_result = item.stat()
                if item.is_file():
                    arquivos.append(
                        {
                            "nome": item.name,
                            "tamanho": formatar_tamanho(bytesize=stat.st_size),
                            "modificacao": coletar_datas_aprimoradas(timestamp=stat.st_mtime),
                            "extensao": item.suffix.lower(),
                        }
                    )
                elif item.is_dir():
                    pastas.append(
                        {"nome": item.name, "modificacao": coletar_datas_aprimoradas(timestamp=stat.st_mtime)}
                    )
            except PermissionError:
                continue
    except PermissionError:
        pass

    return {
        "arquivos": arquivos,
        "pastas": pastas,
        "resumo": {"total_arquivos": len(arquivos), "total_pastas": len(pastas)},
    }
