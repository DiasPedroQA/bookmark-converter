"""
folder_utils.py
----------------

Funções utilitárias de manipulação de pastas e arquivos:
- Filtragem por tipo, nome, extensão e tamanho
- Montagem de árvore hierárquica
- Leitura e escrita de arquivos de texto
- Geração de slugs
"""

import re
from pathlib import Path

from .global_tools import buscar_filhos, check_valid_path

# ============================================================
# [ARQUIVOS]
# ============================================================


def gerar_slug(texto: str) -> str:
    """Converte texto em slug (URL-friendly)."""
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def ler_conteudo_texto(caminho_arquivo: str | Path, codificacao: str = "utf-8") -> str:
    """Lê conteúdo de um arquivo de texto."""
    arquivo_validado: Path = check_valid_path(caminho_arquivo)
    if not arquivo_validado.is_file():
        raise FileNotFoundError(f"Nao é um arquivo válido: {arquivo_validado}")
    return arquivo_validado.read_text(encoding=codificacao)


def escrever_conteudo_texto(caminho_arquivo: str | Path, conteudo: str, codificacao: str = "utf-8") -> None:
    """Escreve conteúdo em um arquivo de texto."""
    Path(caminho_arquivo).write_text(conteudo, encoding=codificacao)


# ============================================================
# [PASTAS]
# ============================================================


def buscar_apenas_pastas(itens: list[Path]) -> list[Path]:
    return [i for i in itens if i.is_dir()]


def buscar_apenas_arquivos(itens: list[Path]) -> list[Path]:
    return [i for i in itens if i.is_file()]


def buscar_por_nome(
    pasta_base: str | Path,
    prefixo: str | None = None,
    sufixo: str | None = None,
    case_sensitive: bool = False,
) -> list[Path]:
    """Busca itens pelo prefixo ou sufixo do nome."""
    pasta_validada: Path = check_valid_path(caminho_generico=pasta_base)
    resultados: list[Path] = []
    for item in buscar_filhos(caminho_de_pasta=pasta_validada):
        nome: str = item.name if case_sensitive else item.name.lower()
        pre: str | None = prefixo if (case_sensitive or prefixo is None) else (prefixo.lower() if prefixo else None)
        suf: str | None = sufixo if (case_sensitive or sufixo is None) else (sufixo.lower() if sufixo else None)
        if (pre and nome.startswith(pre)) or (suf and nome.endswith(suf)):
            resultados.append(item)
    return resultados


def buscar_por_extensoes(pasta_base: str | Path, extensoes: list[str]) -> list[Path]:
    pasta_validada: Path = check_valid_path(caminho_generico=pasta_base)
    exts: set[str] = {ext.lower().lstrip(".") for ext in extensoes}
    return [
        f
        for f in buscar_filhos(caminho_de_pasta=pasta_validada)
        if f.is_file() and f.suffix.lower().lstrip(".") in exts
    ]


def buscar_por_tamanho(pasta_base: str | Path, tamanho_min: int = 0, tamanho_max: int | None = None) -> list[Path]:
    pasta_validada: Path = check_valid_path(caminho_generico=pasta_base)
    resultados: list[Path] = []
    for f in buscar_filhos(caminho_de_pasta=pasta_validada):
        if f.is_file():
            t: int = f.stat().st_size
            if t >= tamanho_min and (tamanho_max is None or t <= tamanho_max):
                resultados.append(f)
    return resultados


# ============================================================
# [ÁRVORE DE PASTAS]
# ============================================================


def montar_arvore(
    pasta_base: str | Path,
    profundidade_maxima: int = 10,
    limite_pastas: int = 50,
) -> dict:
    """Gera representação hierárquica de pasta em dicionário."""
    pasta_validada: Path = check_valid_path(caminho_generico=pasta_base)
    contador: list[int] = [0]

    return {
        "name": pasta_validada.name,
        "type": "folder",
        "children": _explorar(
            pasta=pasta_validada,
            profundidade_maxima=profundidade_maxima,
            limite_pastas=limite_pastas,
            nivel_atual=0,
            contador=contador,
        ),
    }


def _explorar(
    pasta: Path, profundidade_maxima: int, limite_pastas: int, nivel_atual: int, contador: list[int]
) -> list[dict]:
    """Função recursiva interna para montar árvore."""
    children: list[dict] = []
    if nivel_atual > profundidade_maxima or contador[0] >= limite_pastas:
        return children

    contador[0] += 1
    try:
        for item in pasta.iterdir():
            if item.is_dir():
                children.append(
                    {
                        "name": item.name,
                        "type": "folder",
                        "children": _explorar(
                            pasta=item,
                            profundidade_maxima=profundidade_maxima,
                            limite_pastas=limite_pastas,
                            nivel_atual=nivel_atual + 1,
                            contador=contador,
                        ),
                    }
                )
            else:
                children.append({"name": item.name, "type": "file", "children": []})
    except PermissionError:
        children.append({"name": f"PERMISSION_DENIED ({pasta})", "type": "error", "children": []})

    return children
