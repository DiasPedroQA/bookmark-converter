"""
Módulo de manipulação e consulta de pastas.

Fornece funções utilitárias para buscar, filtrar e montar representações
hierárquicas de diretórios, incluindo:
- Listagem de arquivos e pastas.
- Busca por nome, extensão ou tamanho.
- Geração de árvore em formato JSON-like.

Dependências:
    - pathlib.Path
    - utils.global_tools.global_method_check_valid_path
"""

from __future__ import annotations

from pathlib import Path

from utils.global_tools import global_method_check_valid_path


def folder_method_buscar_apenas_pastas(itens: list[Path]) -> list[Path]:
    """Buscar apenas pastas visíveis."""
    return [i for i in itens if i.is_dir()]


def folder_method_buscar_apenas_arquivos(itens: list[Path]) -> list[Path]:
    """Buscar apenas arquivos visíveis."""
    return [i for i in itens if i.is_file()]


def folder_method_buscar_filhos(pasta: str | Path) -> list[Path]:
    """Lista todos os arquivos e pastas recursivamente dentro de uma pasta."""
    p: Path = global_method_check_valid_path(caminho_generico=pasta)
    return list(p.rglob(pattern="*"))


def folder_method_buscar_por_nome(
    pasta_base: str | Path,
    prefixo: str | None = None,
    sufixo: str | None = None,
    case_sensitive: bool = False,
) -> list[Path]:
    """Busca itens (arquivos ou pastas) por prefixo ou sufixo de nome."""
    pasta_validada: Path = global_method_check_valid_path(caminho_generico=pasta_base)

    resultados: list[Path] = []
    for item in folder_method_buscar_filhos(pasta=pasta_validada):
        nome: str = item.name if case_sensitive else item.name.lower()
        pre: str | None = prefixo if (case_sensitive or prefixo is None) else prefixo.lower()
        suf: str | None = sufixo if (case_sensitive or sufixo is None) else sufixo.lower()

        if (pre and nome.startswith(pre)) or (suf and nome.endswith(suf)):
            resultados.append(item)

    return resultados


def folder_method_buscar_arquivos_por_extensoes(pasta_base: str | Path, extensoes: list[str]) -> list[Path]:
    """Busca arquivos por extensões dentro de um diretório (recursivamente)."""
    pasta_validada: Path = global_method_check_valid_path(caminho_generico=pasta_base)
    exts: list[str] = [ext.lower().lstrip(".") for ext in extensoes]
    return [
        f
        for f in folder_method_buscar_filhos(pasta=pasta_validada)
        if f.is_file() and f.suffix.lower().lstrip(".") in exts
    ]


def folder_method_buscar_arquivos_por_tamanho(
    pasta_base: str | Path, tamanho_minimo: int = 0, tamanho_maximo: int | None = None
) -> list[Path]:
    """Filtra arquivos por tamanho em bytes."""
    pasta_base = Path(pasta_base).resolve()
    resultados: list[Path] = []
    for f in folder_method_buscar_filhos(pasta=pasta_base):
        if f.is_file():
            tamanho: int = f.stat().st_size
            if tamanho >= tamanho_minimo and (tamanho_maximo is None or tamanho <= tamanho_maximo):
                resultados.append(f)
    return resultados


def folder_method_montar_arvore(
    pasta_base: str | Path,
    profundidade_maxima: int = 10,
    limite_pastas: int = 50,
    _nivel_atual: int = 0,
    _contador: list[int] | None = None,
) -> dict[str, object]:
    """
    Monta uma árvore hierárquica da pasta em formato de dicionário.
    Limita a profundidade e quantidade de pastas listadas.

    Retorna sempre dicionários no formato:
    {
        "name": str,
        "type": "folder" | "file" | "error",
        "children": list[dict]
    }
    """
    pasta_validada: Path = global_method_check_valid_path(caminho_generico=pasta_base)
    if _contador is None:
        _contador = [0]  # usar lista para mutabilidade entre chamadas recursivas

    if _nivel_atual > profundidade_maxima or _contador[0] >= limite_pastas:
        return {"name": pasta_validada.name, "type": "folder", "children": []}

    _contador[0] += 1

    arvore: dict[str, object] = {"name": pasta_validada.name, "type": "folder", "children": []}
    childs: list = arvore["children"]

    try:
        for item in pasta_validada.iterdir():
            if item.is_dir():
                childs.append(
                    folder_method_montar_arvore(
                        pasta_base=item,
                        profundidade_maxima=profundidade_maxima,
                        limite_pastas=limite_pastas,
                        _nivel_atual=_nivel_atual + 1,
                        _contador=_contador,
                    )
                )
            else:
                childs.append({"name": item.name, "type": "file", "children": []})
    except PermissionError:
        childs.append({"name": f"PERMISSION_DENIED ({pasta_validada})", "type": "error", "children": []})

    return arvore


import json

# from utils.folders_tools import (
#     folder_method_buscar_apenas_pastas,
#     folder_method_buscar_apenas_arquivos,
#     folder_method_buscar_filhos,
#     folder_method_buscar_por_nome,
#     folder_method_buscar_arquivos_por_extensoes,
#     folder_method_buscar_arquivos_por_tamanho,
#     folder_method_montar_arvore,
# )

# Caminho base
pasta_base = Path("/home/pedro-pm-dias/Downloads/Firefox")

# 1. Buscar apenas pastas
pastas: list[Path] = folder_method_buscar_apenas_pastas(itens=list(pasta_base.iterdir()))
print("\n[Pastas na raiz]:")
for p in pastas:
    print(" -", p.name)

# 2. Buscar apenas arquivos
arquivos: list[Path] = folder_method_buscar_apenas_arquivos(itens=list(pasta_base.iterdir()))
print("\n[Arquivos na raiz]:")
for a in arquivos:
    print(" -", a.name)

# 3. Buscar filhos recursivamente
todos: list[Path] = folder_method_buscar_filhos(pasta=pasta_base)
print("\n[Todos os itens recursivamente]:")
for t in todos:
    print(" -", t)

# 4. Buscar por prefixo/sufixo
print("\n[Arquivos começando com 'fo' ou terminando com '.md']:")
busca: list[Path] = folder_method_buscar_por_nome(pasta_base=pasta_base, prefixo="fo", sufixo=".md")
for b in busca:
    print(" -", b.name)

# 5. Buscar arquivos por extensões
print("\n[Arquivos de texto e imagens]:")
por_ext: list[Path] = folder_method_buscar_arquivos_por_extensoes(
    pasta_base=pasta_base, extensoes=["txt", "jpg", "png"]
)
for e in por_ext:
    print(" -", e.name)

# 6. Buscar arquivos por tamanho
print("\n[Arquivos maiores que 1KB]:")
por_tamanho: list[Path] = folder_method_buscar_arquivos_por_tamanho(pasta_base=pasta_base, tamanho_minimo=1024)
for t in por_tamanho:
    print(" -", t.name, f"({t.stat().st_size} bytes)")

# 7. Montar árvore da pasta
print("\n[Árvore da pasta em JSON-like]:")
arvore: dict[str, object] = folder_method_montar_arvore(pasta_base=pasta_base, profundidade_maxima=3)

print(json.dumps(arvore, indent=2, ensure_ascii=False))
